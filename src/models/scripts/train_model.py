import mlflow
import onnxmltools
from mlflow import MlflowClient
from onnxconverter_common import FloatTensorType
from onnxmltools import convert_sklearn, convert_xgboost
from skl2onnx import to_onnx, update_registered_converter
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from mlflow.onnx import log_model as log_onnx_model
from src.config.constants import SEED, POWER_PRODUCTION_MODEL_NAME
from src.models.mlflow_config import mlflow_config
from src.models.model import prepare_data, evaluate_model_performance


def main():
    client = mlflow_config()

    mlflow.start_run(run_name=POWER_PRODUCTION_MODEL_NAME, nested=True)

    mlflow.autolog()

    X_train, X_test, y_train, y_test = prepare_data()

    X_train.columns = [f'f{i}' for i in range(X_train.shape[1])]

    model = XGBRegressor(random_state=SEED)
    model.fit(X_train, y_train)

    onnx_model = onnxmltools.convert_xgboost(model, initial_types=[('input', FloatTensorType([None, X_train.shape[1]]))])

    log_onnx_model(onnx_model=onnx_model,
                   artifact_path=POWER_PRODUCTION_MODEL_NAME,
                   registered_model_name=POWER_PRODUCTION_MODEL_NAME)

    model_version = client.get_latest_versions(POWER_PRODUCTION_MODEL_NAME)[0]
    print(model_version.version)
    client.set_registered_model_alias(POWER_PRODUCTION_MODEL_NAME, "production", model_version.version)

    X_test.columns = [f'f{i}' for i in range(X_test.shape[1])]

    model_predictions = model.predict(X_test)

    mse_production, mae_production, evs_production = evaluate_model_performance(y_test, model_predictions)

    mlflow.log_metric("Mean Squared Error", mse_production)
    mlflow.log_metric("Mean Absolute Error", mae_production)
    mlflow.log_metric("Explained Variance Score", evs_production)

    mlflow.end_run()


if __name__ == "__main__":
    main()
