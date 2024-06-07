from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POWER_PLANT_API_URI: str
    WEATHER_API_URI: str
    TIME_API_URI: str
    MLFLOW_TRACKING_URI: str
    MLFLOW_TRACKING_USERNAME: str
    MLFLOW_TRACKING_PASSWORD: str
    DAGSHUB_TOKEN: str
    MONGO_URI: str
    PRODUCTION_API_URI: str
    PUSHER_APP_ID: str
    PUSHER_APP_KEY: str
    PUSHER_APP_SECRET: str
    PUSHER_APP_CLUSTER: str
    DAGSHUB_REPO_URI: str
    DAGSHUB_ACCESS_KEY_ID: str
    DAGSHUB_ACCESS_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
