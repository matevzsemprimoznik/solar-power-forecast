import os
import mlflow
from mlflow.onnx import load_model as load_onnx
from src.models.common.mlflow_config import MlflowConfig
import onnxruntime as ort


def get_artifact(name: str, alias: str):
    try:
        client = MlflowConfig().get_client()
        model_version = client.get_model_version_by_alias(name, alias)
        artifact_proto = load_onnx(model_version.source)

        return {
            "model": ort.InferenceSession(artifact_proto.SerializeToString()),
            "metadata": artifact_proto.metadata_props
        }
    except IndexError:
        print(f"Model with name {name} and alias {alias} not found")
        return None


def download_artifact(name: str, alias: str, output_path: str):
    client = MlflowConfig().get_client()
    artifact_path = f"{output_path}/model"

    model_version = client.get_model_version_by_alias(name, alias)
    model = load_onnx(model_version.source)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    mlflow.onnx.save_model(model, artifact_path)

    print(f"Artifact has been downloaded to {output_path}.")

    return f"{artifact_path}/model.onnx"
