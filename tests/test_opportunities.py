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


def test_update_opportunity():
    client = TestClient(app)
    payload = {
        "title": "Original Title",
        "market_description": "Description",
        "tam_estimate": 1000.0,
        "growth_rate": 5.0,
        "consumer_insight": "Insight",
        "hypothesis": "Hypothesis",
    }
    create_response = client.post("/opportunities/", json=payload)
    opportunity_id = create_response.json()["id"]

    update_payload = {"title": "Updated Title", "tam_estimate": 2000.0}
    response = client.patch(f"/opportunities/{opportunity_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["tam_estimate"] == 2000.0

    get_response = client.get(f"/opportunities/{opportunity_id}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["title"] == "Updated Title"


def test_delete_opportunity():
    client = TestClient(app)
    payload = {"title": "To Delete"}
    create_response = client.post("/opportunities/", json=payload)
    opportunity_id = create_response.json()["id"]

    response = client.delete(f"/opportunities/{opportunity_id}")
    assert response.status_code == 204

    get_response = client.get(f"/opportunities/{opportunity_id}")
    assert get_response.status_code == 404

    list_response = client.get("/opportunities/")
    assert list_response.status_code == 200
    assert list_response.json() == []


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
