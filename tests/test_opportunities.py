import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from database import Base, engine
from main import app
import pytest


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_opportunity():
    client = TestClient(app)
    payload = {
        "title": "New Market",
        "market_description": "Description",
        "tam_estimate": 1000.0,
        "growth_rate": 5.0,
        "consumer_insight": "Insight",
        "hypothesis": "Hypothesis",
    }
    response = client.post("/opportunities/", json=payload)
    assert response.status_code == 200
    data = response.json()
    for key, value in payload.items():
        assert data[key] == value
    assert "id" in data

    # verify opportunity is persisted
    list_response = client.get("/opportunities/")
    assert list_response.status_code == 200
    opportunities = list_response.json()
    assert len(opportunities) == 1
    assert opportunities[0]["title"] == payload["title"]


@pytest.mark.parametrize("tam_estimate", [-1000.0, 0.0])
def test_create_opportunity_invalid_tam_estimate(tam_estimate):
    client = TestClient(app)
    payload = {
        "title": "Invalid TAM",
        "market_description": "Description",
        "tam_estimate": tam_estimate,
        "growth_rate": 5.0,
        "consumer_insight": "Insight",
        "hypothesis": "Hypothesis",
    }
    response = client.post("/opportunities/", json=payload)
    assert response.status_code == 422


def test_create_opportunity_invalid_growth_rate():
    client = TestClient(app)
    payload = {
        "title": "Invalid Growth",
        "market_description": "Description",
        "tam_estimate": 1000.0,
        "growth_rate": -1.0,
        "consumer_insight": "Insight",
        "hypothesis": "Hypothesis",
    }
    response = client.post("/opportunities/", json=payload)
    assert response.status_code == 422
