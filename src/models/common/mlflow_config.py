import os
import dagshub
from dagshub.data_engine.datasources import mlflow
from mlflow import MlflowClient

from src.config.settings import settings

import os
import mlflow
import dagshub
from mlflow.tracking import MlflowClient


class MlflowConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MlflowConfig, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize(self):
        if not self._initialized:
            os.environ['MLFLOW_TRACKING_URI'] = settings.MLFLOW_TRACKING_URI
            os.environ['MLFLOW_TRACKING_USERNAME'] = settings.MLFLOW_TRACKING_USERNAME
            os.environ['MLFLOW_TRACKING_PASSWORD'] = settings.MLFLOW_TRACKING_PASSWORD
            dagshub.auth.add_app_token(token=settings.DAGSHUB_TOKEN)
            dagshub.init("mbajk-forecast", "matevzsemprimoznik", mlflow=True)
            mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
            self.client = MlflowClient()
            self._initialized = True

    def get_client(self):
        if not self._initialized:
            self.initialize()
        return self.client


if __name__ == "__main__":
    MlflowConfig().get_client()
