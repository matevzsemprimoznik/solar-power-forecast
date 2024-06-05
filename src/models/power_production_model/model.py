import mlflow
import onnxmltools
from matplotlib import pyplot as plt
from onnxconverter_common import FloatTensorType
from xgboost import XGBRegressor
from mlflow.onnx import log_model as log_onnx_model
from src.config.constants import SEED, POWER_PRODUCTION_MODEL_NAME
from src.models.common.mlflow_config import MlflowConfig
from src.models.common.model import save_onnx_metadata
from src.models.power_production_model.prepare_data import prepare_power_production_model_data
from src.models.common.model_evaluation import evaluate_model_performance
import shap

def train_power_production_model():
    print("Training power production model")
    client = MlflowConfig().get_client()

    mlflow.start_run(run_name=POWER_PRODUCTION_MODEL_NAME, nested=True)

    mlflow.autolog()

    X_train, X_test, y_train, y_test, column_names_map = prepare_power_production_model_data()

    model = XGBRegressor(random_state=SEED)
    model.fit(X_train, y_train)

    onnx_model = onnxmltools.convert_xgboost(model,
                                             initial_types=[('input', FloatTensorType([None, X_train.shape[1]]))])

    save_onnx_metadata(onnx_model, column_names_map)

    log_onnx_model(onnx_model=onnx_model,
                   artifact_path=POWER_PRODUCTION_MODEL_NAME,
                   registered_model_name=POWER_PRODUCTION_MODEL_NAME)

    model_version = client.get_latest_versions(POWER_PRODUCTION_MODEL_NAME)[0]

    client.set_registered_model_alias(POWER_PRODUCTION_MODEL_NAME, "production", model_version.version)

    model_predictions = model.predict(X_test)

    mse_production, mae_production, evs_production = evaluate_model_performance(y_test, model_predictions)

    mlflow.log_metric("Mean Squared Error", mse_production)
    mlflow.log_metric("Mean Absolute Error", mae_production)
    mlflow.log_metric("Explained Variance Score", evs_production)

    # SHAP
    X_train, _, y_train, _, _ = prepare_power_production_model_data(serialize_columns=False)
    model = XGBRegressor(random_state=SEED)
    model.fit(X_train, y_train)
    explainer = shap.Explainer(model)
    shap_values = explainer(X_train, check_additivity=False)

    beeswarm_plot_path = "shap_beeswarm.png"
    plt.subplots_adjust(left=0.4)
    shap.plots.beeswarm(shap_values, show=False)
    plt.savefig(beeswarm_plot_path, bbox_inches='tight')
    plt.close()

    mlflow.log_artifact(beeswarm_plot_path)

    bar_plot_path = "shap_bar.png"
    plt.subplots_adjust(left=0.4)
    shap.plots.bar(shap_values, show=False)
    plt.savefig(bar_plot_path, bbox_inches='tight')
    plt.close()

    mlflow.log_artifact(bar_plot_path)

    mlflow.end_run()
