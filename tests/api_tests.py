import requests
from src.config.settings import settings


def test_bike_api():
    response = requests.get(settings.POWER_PLANT_API_URI)
    assert response.status_code == 200


def test_weather_api():
    response = requests.get(settings.WEATHER_API_URI)
    assert response.status_code == 200


def test_time_api():
    response = requests.get(settings.TIME_API_URI)
    assert response.status_code == 200
