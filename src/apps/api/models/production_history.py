from datetime import datetime

from pydantic import BaseModel, Field


class ProductionHistoryData(BaseModel):
    date: datetime
    prediction: float
    real: float
