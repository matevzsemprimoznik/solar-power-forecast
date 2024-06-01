import shutil

import numpy as np

from src.config.constants import SOLAR_RADIATION_MODEL_NAME
from src.models.common.mlflow_config import MlflowConfig
from src.models.common.model_evaluation import evaluate_model_performance
from src.models.common.model_registry import download_artifact, get_artifact
from src.models.solar_radiation_model.prepare_data import prepare_solar_radiation_model_data


def evaluate_solar_radiation_model():
    client = MlflowConfig().get_client()

    model = get_artifact(SOLAR_RADIATION_MODEL_NAME, "production")

    _, X_test, __, y_test = prepare_solar_radiation_model_data()

    model_predictions = model.run(None, {'input': X_test.values.astype(np.float32)})[0]

    mse_production, mae_production, evs_production = evaluate_model_performance(y_test, model_predictions)

    print(f"Production model performance:")
    print(f"MSE: {mse_production}")
    print(f"MAE: {mae_production}")
    print(f"EVS: {evs_production}")

    shutil.rmtree(f"models/temp/", ignore_errors=True)