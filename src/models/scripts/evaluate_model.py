import shutil

import numpy as np
from tensorflow import double

from src.config.constants import POWER_PRODUCTION_MODEL_NAME
from src.models.mlflow_config import mlflow_config
from src.models.model import prepare_data, evaluate_model_performance
from src.models.model_registry import download_artifact
import onnxruntime as ort


def main():
    client = mlflow_config()

    model_path = download_artifact(POWER_PRODUCTION_MODEL_NAME, "production", f"models/temp")

    _, X_test, __, y_test = prepare_data()

    print(X_test.shape)
    print(X_test.head())

    X_test.columns = [f'f{i}' for i in range(X_test.shape[1])]

    model = ort.InferenceSession(model_path)

    model_predictions = model.run(None, {'input': X_test.values.astype(np.float32)})[0]

    mse_production, mae_production, evs_production = evaluate_model_performance(y_test, model_predictions)

    print(f"Production model performance:")
    print(f"MSE: {mse_production}")
    print(f"MAE: {mae_production}")
    print(f"EVS: {evs_production}")

    shutil.rmtree(f"models/temp/", ignore_errors=True)


if __name__ == "__main__":
    main()