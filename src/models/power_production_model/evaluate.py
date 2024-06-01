import shutil

import numpy as np

from src.config.constants import POWER_PRODUCTION_MODEL_NAME
from src.models.common.mlflow_config import MlflowConfig
from src.models.power_production_model.prepare_data import prepare_power_production_model_data
from src.models.common.model_evaluation import evaluate_model_performance
from src.models.common.model_registry import download_artifact, get_artifact


def evaluate_power_production_model():
    client = MlflowConfig().get_client()

    model = get_artifact(POWER_PRODUCTION_MODEL_NAME, "production").get('model')

    print(get_artifact(POWER_PRODUCTION_MODEL_NAME, "production").get('metadata'))

    _, X_test, _, y_test, _ = prepare_power_production_model_data()

    model_predictions = model.run(None, {'input': X_test.values.astype(np.float32)})[0]

    mse_production, mae_production, evs_production = evaluate_model_performance(y_test, model_predictions)

    print(f"Production model performance:")
    print(f"MSE: {mse_production}")
    print(f"MAE: {mae_production}")
    print(f"EVS: {evs_production}")

    shutil.rmtree(f"models/temp/", ignore_errors=True)

