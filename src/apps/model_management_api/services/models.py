import requests
from src.config.settings import settings
from src.models.common.mlflow_config import MlflowConfig


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

        models_with_aliases = []
        for model in models:
            properties = model.__dict__
            properties = {key.strip("_"): value for key, value in properties.items()}
            properties['aliases'] = []
            properties['metrics'] = self.mlflow_client.get_run(model.run_id).data.metrics
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
        print('production_model')
        print(production_model)
        if production_model:
            self.mlflow_client.delete_registered_model_alias(production_model.get('name'), 'production')

        self.mlflow_client.set_registered_model_alias(name, 'production', str(version))

        requests.put(f"{settings.PRODUCTION_API_URI}/production/update-models")

        return 'Model moved to production successfully!'
