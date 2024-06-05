from fastapi import APIRouter, BackgroundTasks

from src.apps.model_management_api.services.models import ModelsService

models_router = APIRouter(
    prefix="/models",
    tags=["models"],
)

models_service = ModelsService()


@models_router.get("/name/{name}/alias/{alias}")
def get_model_version_by_alias(name: str, alias: str):
    return models_service.get_model_version_by_alias(name, alias)


@models_router.get("")
def get_models():
    return models_service.get_models()


@models_router.get("/{id}")
def get_model(id: str):
    return models_service.get_model(id)


@models_router.post("/production/name/{name}/version/{version}")
def move_to_production(name: str, version: int, background_task: BackgroundTasks):
    background_task.add_task(models_service.move_to_production, name, version)
    return "Model moved to production"


@models_router.post("/train/{name}")
def train_model(name: str, background_task: BackgroundTasks):
    background_task.add_task(models_service.train_model, name)
    return "Model training started"
