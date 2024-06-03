from pydantic import BaseModel


class PredictionInput(BaseModel):
    available_bikes: int
    temperature: float
    relative_humidity: float
    dew_point: float
    apparent_temperature: float
    precipitation_probability: float
    rain: float
    surface_pressure: float


class PredictionMultipleOutput(BaseModel):
    date: str
    prediction: int
