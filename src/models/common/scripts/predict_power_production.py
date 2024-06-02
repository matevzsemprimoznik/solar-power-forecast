from datetime import datetime, timedelta

import pymongo
from starlette.testclient import TestClient

from src.apps.api.main import app
from src.config.settings import settings
from src.data.solar_production_fetcher import ProductionFetcher

if __name__ == "__main__":
    client = TestClient(app)
    response = client.get("/production/predict")

    prediction = response.json()["prediction"]

    mongo_client = pymongo.MongoClient(settings.MONGO_URI)

    database = mongo_client["solar-power-production-predictions"]
    collection = database["predictions"]

    date = datetime.strptime(prediction["date"], "%Y-%m-%dT%H:%M:%S")

    collection.insert_one({
        "date": date,
        "prediction": prediction["power"],
        "real": None
    })

    previous_date = date - timedelta(hours=1)

    previous = collection.find_one({"date": previous_date})

    solar_production_fetcher = ProductionFetcher()

    solar_power_production = solar_production_fetcher.fetch_n_last(1)[0]

    collection.update_one({"date": previous_date}, {"$set": {"real": solar_power_production.power}})




