from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POWER_PLANT_API_URI: str
    WEATHER_API_URI: str
    TIME_API_URI: str
    MLFLOW_TRACKING_URI: str
    MLFLOW_TRACKING_USERNAME: str
    MLFLOW_TRACKING_PASSWORD: str
    DAGSHUB_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
