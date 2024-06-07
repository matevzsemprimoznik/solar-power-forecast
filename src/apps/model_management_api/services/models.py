import base64
import io
import os
import shutil

import mlflow
import requests
from src.models.power_production_model.model import train_power_production_model
from src.models.solar_radiation_model.model import train_solar_radiation_model
from src.apps.model_management_api.config.pusher import pusher_client
from src.apps.model_management_api.utils.load_data import download_data_for_model_train
from src.config.settings import settings
from src.models.common.mlflow_config import MlflowConfig
from PIL import Image

class ModelsService:
    def __init__(self):
        self.mlflow_client = MlflowConfig().get_client()

    def get_model_version_by_alias(self, name: str, alias: str):
        print(name, alias)
        res = self.mlflow_client.get_model_version_by_alias(name, alias)

        return_dict = {}
        for key, value in res.__dict__.items():
            key = key.strip("_")
            return_dict[key] = value

        return_dict["aliases"] = list(return_dict.get("aliases"))

        return return_dict

    def get_models(self):
        models = self.mlflow_client.search_model_versions()
        registered_models = self.mlflow_client.search_registered_models()

        run_ids_filter = ",".join([f"'{model.run_id}'" for model in models])
        runs = mlflow.search_runs(search_all_experiments=True, filter_string=f"attributes.run_id IN ({run_ids_filter})")

        models_with_aliases = []
        for model in models:
            properties = model.__dict__
            properties = {key.strip("_"): value for key, value in properties.items()}
            properties['aliases'] = []
            run = runs[runs['run_id'] == model.run_id]
            properties['metrics'] = {
                'mse': run['metrics.Mean Squared Error'].values[0],
                'mae': run['metrics.Mean Absolute Error'].values[0],
                'evs': run['metrics.Explained Variance Score'].values[0]
            }
            properties['id'] = model.name + '-' + str(model.version)
            models_with_aliases.append(properties)

        for model in models_with_aliases:
            for registered_model in registered_models:
                if model.get('name') == registered_model.name:
                    aliases = registered_model.aliases
                    for key, value in aliases.items():
                        if value == model.get('version'):
                            model['aliases'].append(key)

        return models_with_aliases

    def move_to_production(self, name: str, version: int):
        production_model = self.get_model_version_by_alias(name, 'production')

        if production_model:
            self.mlflow_client.delete_registered_model_alias(production_model.get('name'), 'production')

        self.mlflow_client.set_registered_model_alias(name, 'production', str(version))

        requests.put(f"{settings.PRODUCTION_API_URI}/production/update-models")
        pusher_client.trigger('solar-power-model-management-api', 'model-moved-to-production-successfully', {'message': 'Model moved to production successfully!'})

        return 'Model moved to production successfully!'

    def get_model(self, id: str):
        [name, version] = id.split('-')
        res = self.mlflow_client.get_model_version(name, version)

        return_dict = {}
        return_dict['id'] = res.name + '-' + str(res.version)
        for key, value in res.__dict__.items():
            key = key.strip("_")
            return_dict[key] = value

        return_dict["aliases"] = list(return_dict.get("aliases"))

        if not os.path.exists('images'):
            os.makedirs('images')

        artifacts = self.mlflow_client.list_artifacts(run_id=return_dict.get("run_id"))
        return_artifacts = {}
        for artifact in artifacts:
            if artifact.path == 'shap_beeswarm.png' or artifact.path == 'shap_bar.png':
                path = self.mlflow_client.download_artifacts(return_dict.get("run_id"), artifact.path, 'images')
                with Image.open(path) as image:
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    return_artifacts[artifact.path.replace('.png', '')] = img_str

        return_dict['artifacts'] = return_artifacts
        shutil.rmtree('images')
        return return_dict

    def train_model(self, model_name: str):
        if model_name == 'power_production_model':
            download_data_for_model_train()
            train_power_production_model()
        elif model_name == 'solar_radiation_model':
            download_data_for_model_train()
            train_solar_radiation_model()
        else:
            return 'Model not found!'
        print('Model training successful!')
        pusher_client.trigger('solar-power-model-management-api', 'model-trained-successfully', {'message': 'Model trained successfully!'})

        return 'Model training started!'



