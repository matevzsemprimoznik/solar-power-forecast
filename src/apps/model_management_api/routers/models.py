from fastapi import APIRouter

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


@models_router.post("/production/name/{name}/version/{version}")
def move_to_production(name: str, version: int):
    return models_service.move_to_production(name, version)

