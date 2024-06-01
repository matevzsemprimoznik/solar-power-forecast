import pymongo

from src.config.settings import settings

client = pymongo.MongoClient(settings.MONGO_URI)

database = client["forecasts"]