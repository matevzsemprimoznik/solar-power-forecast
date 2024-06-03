from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apps.api.routers.health import health_router
from src.apps.model_management_api.routers.models import models_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


app.include_router(health_router)
app.include_router(models_router)
