from datetime import datetime

from pydantic import BaseModel


class Production(BaseModel):
    time: datetime
    power: float
