import onnxmltools
from mlflow import MlflowClient
from onnxconverter_common import FloatTensorType
from xgboost import XGBRegressor
from mlflow.onnx import log_model as log_onnx_model
from src.config.constants import SEED, POWER_PRODUCTION_MODEL_NAME
from src.models.mlflow_config import mlflow_config
from src.models.model import prepare_data


def main():
    client = mlflow_config()

    X_train, X_test, y_train, y_test = prepare_data()

    X_train.columns = [f'f{i}' for i in range(X_train.shape[1])]

    model = XGBRegressor(random_state=SEED)
    model.fit(X_train, y_train)

    input_signature = [('input', FloatTensorType([None, len(X_train.columns)]))]

    onnx_model = onnxmltools.convert_xgboost(model, initial_types=input_signature)

    log_onnx_model(onnx_model=onnx_model,
                   artifact_path=POWER_PRODUCTION_MODEL_NAME,
                   registered_model_name=POWER_PRODUCTION_MODEL_NAME)

    model_version = client.get_latest_versions(POWER_PRODUCTION_MODEL_NAME)[0]
    print(model_version.version)
    client.set_registered_model_alias(POWER_PRODUCTION_MODEL_NAME, "production", model_version.version)


if __name__ == "__main__":
    main()
