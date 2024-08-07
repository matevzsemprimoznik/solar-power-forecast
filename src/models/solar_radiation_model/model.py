import mlflow
import onnxmltools
from onnxconverter_common import FloatTensorType
from xgboost import XGBRegressor
from mlflow.onnx import log_model as log_onnx_model
from src.config.constants import SEED, SOLAR_RADIATION_MODEL_NAME
from src.models.common.mlflow_config import MlflowConfig
from src.models.common.model import save_onnx_metadata
from src.models.common.model_evaluation import evaluate_model_performance
from src.models.solar_radiation_model.prepare_data import prepare_solar_radiation_model_data


def train_solar_radiation_model():
    client = MlflowConfig().get_client()

    mlflow.start_run(run_name=SOLAR_RADIATION_MODEL_NAME, nested=True)

    mlflow.autolog()

    X_train, X_test, y_train, y_test, column_names_map = prepare_solar_radiation_model_data()

    model = XGBRegressor(random_state=SEED)
    model.fit(X_train, y_train)

    onnx_model = onnxmltools.convert_xgboost(model,
                                             initial_types=[('input', FloatTensorType([None, X_train.shape[1]]))])

    save_onnx_metadata(onnx_model, column_names_map)


    log_onnx_model(onnx_model=onnx_model,
                   artifact_path=SOLAR_RADIATION_MODEL_NAME,
                   registered_model_name=SOLAR_RADIATION_MODEL_NAME)

    model_version = client.get_latest_versions(SOLAR_RADIATION_MODEL_NAME)[0]

    client.set_registered_model_alias(SOLAR_RADIATION_MODEL_NAME, "production", model_version.version)

    model_predictions = model.predict(X_test)

    mse_production, mae_production, evs_production = evaluate_model_performance(y_test, model_predictions)

    mlflow.log_metric("Mean Squared Error", mse_production)
    mlflow.log_metric("Mean Absolute Error", mae_production)
    mlflow.log_metric("Explained Variance Score", evs_production)

    mlflow.end_run()
