import os

import mlflow
from mlflow.onnx import load_model as load_onnx
from onnx import ModelProto
from src.models.mlflow_config import mlflow_config


def get_artifact(name: str, alias: str) -> ModelProto:
    try:
        client = mlflow_config()
        model_version = client.get_model_version_by_alias(name, alias)
        return load_onnx(model_version.source)
    except IndexError:
        print(f"Model with name {name} and alias {alias} not found")
        return None


def download_artifact(name: str, alias: str, output_path: str):
    mlflow_config()
    artifact_path = f"{output_path}/model"

    model = get_artifact(name, alias)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    mlflow.onnx.save_model(model, artifact_path)

    print(f"Artifact has been downloaded to {output_path}.")

    return f"{artifact_path}/model.onnx"
