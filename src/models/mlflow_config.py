import os
import dagshub
from dagshub.data_engine.datasources import mlflow
from mlflow import MlflowClient

from src.config.settings import settings


def mlflow_config():
    os.environ['MLFLOW_TRACKING_URI'] = settings.MLFLOW_TRACKING_URI
    os.environ['MLFLOW_TRACKING_USERNAME'] = settings.MLFLOW_TRACKING_USERNAME
    os.environ['MLFLOW_TRACKING_PASSWORD'] = settings.MLFLOW_TRACKING_PASSWORD
    dagshub.auth.add_app_token(token=settings.DAGSHUB_TOKEN)
    dagshub.init("mbajk-forecast", "matevzsemprimoznik", mlflow=True)
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

    return MlflowClient()


if __name__ == "__main__":
    mlflow_config()
