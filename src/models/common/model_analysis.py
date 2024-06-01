import onnxmltools
from mlflow import MlflowClient
from xgboost import XGBRegressor
from src.config.constants import SEED
from mlflow.onnx import log_model as log_onnx_model
from src.models.power_production_model.prepare_data import prepare_power_production_model_data
from skl2onnx.common.data_types import FloatTensorType


def model_analysis():
    client = MlflowClient()
    print('Analyzing model')
    X_train, X_test, y_train, y_test = prepare_power_production_model_data()
    model = XGBRegressor(random_state=SEED)

    input_signature = [('input', FloatTensorType([None, X_train.shape[1]]))]

    onnx_model = onnxmltools.convert_xgboost(model, initial_types=input_signature)

    log_onnx_model(onnx_model=onnx_model,
                   artifact_path="analyzed_model",
                   registered_model_name="analyzed_model")

    model_version = client.get_latest_versions("analyzed_model", stages=["None"])[0]
    client.set_registered_model_alias("analyzed_model", "production", model_version.version)


