import pytest
import sys
import os

# Add app directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_predict_positive(client):
    response = client.post("/predict", json={"a": 1, "b": 1, "c": 1})
    assert response.status_code == 200
    assert response.get_json()["prediction"] == "positive"


def test_predict_negative(client):
    response = client.post("/predict", json={"a": 0, "b": 0, "c": 1})
    assert response.status_code == 200
    assert response.get_json()["prediction"] == "negative"
