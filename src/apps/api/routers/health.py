from fastapi import APIRouter
from datetime import datetime

health_router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@health_router.get("")
def health_check():
    date = datetime.now()
    return {"status": "ok", "date": date}
