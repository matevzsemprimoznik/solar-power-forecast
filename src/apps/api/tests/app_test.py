from starlette.testclient import TestClient
from src.apps.api.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert "date" in response.json()
    assert response.json()["status"] == "ok"


def test_success_prediction():
    response = client.get("/predict")
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert isinstance(response.json()["prediction"], int)
    assert response.json()["prediction"] >= 0
    assert response.json()["prediction"] <= 100