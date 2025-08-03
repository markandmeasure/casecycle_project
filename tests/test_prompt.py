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


def create_user_and_token(client, username="user"):
    user_resp = client.post("/users/", json={"name": username})
    user_id = user_resp.json()["id"]
    token_resp = client.post(
        "/token", data={"username": username, "password": "password"}
    )
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers, user_id


def test_generate_prompt():
    client = TestClient(app)
    headers, user_id = create_user_and_token(client, "Dana")
    payload = {
        "title": "AI Widget",
        "market_description": "Widgets for AI",
        "tam_estimate": 5000.0,
        "growth_rate": 12.5,
        "consumer_insight": "Automation is valued",
        "hypothesis": "AI widgets save time",
        "user_id": user_id,
    }
    create_resp = client.post("/opportunities/", json=payload, headers=headers)
    assert create_resp.status_code == 200
    opp_id = create_resp.json()["id"]

    resp = client.get(f"/prompt/{opp_id}")
    assert resp.status_code == 200
    prompt = resp.json()["prompt"]
    assert f"Opportunity Title: {payload['title']}" in prompt
    assert f"Market Description: {payload['market_description']}" in prompt
    assert f"TAM Estimate: {payload['tam_estimate']}" in prompt
    assert f"Growth Rate: {payload['growth_rate']}" in prompt
    assert f"Consumer Insight: {payload['consumer_insight']}" in prompt
    assert f"Hypothesis: {payload['hypothesis']}" in prompt
