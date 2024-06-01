from fastapi import APIRouter

from src.apps.api.services.predictions import PredictionsService

predictions_router = APIRouter(
    prefix="/predict",
    tags=["predict"],
)

prediction_service = PredictionsService()


@predictions_router.get("")
def predict():
    return {
        "prediction": prediction_service.predict()
    }


@predictions_router.get("/next/{n_next}")
def predict(n_next: int):
    return {
        "prediction": prediction_service.predict_n_next(n_next)
    }