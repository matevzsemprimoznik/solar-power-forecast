from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.apps.api.routers.health import health_router
from src.apps.api.routers.predictions import predictions_router

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
app.include_router(predictions_router)