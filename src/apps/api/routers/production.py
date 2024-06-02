from fastapi import APIRouter

from src.apps.api.services.production import ProductionService

production_router = APIRouter(
    prefix="/production",
    tags=["production"],
)

production_service = ProductionService()


@production_router.get("/predict")
def predict():
    return {
        "prediction": production_service.predict()
    }


@production_router.get("/predict/next/{n_next}")
def predict(n_next: int):
    return {
        "prediction": production_service.predict_n_next(n_next)
    }


@production_router.get("/history")
def history(start_date: str | None = None, end_date: str | None = None):
    return {
        "history": production_service.history(start_date, end_date)
    }