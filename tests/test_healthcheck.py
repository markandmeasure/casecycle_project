import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import main
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


def test_healthcheck_success():
    client = TestClient(main.app)
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_healthcheck_db_failure(monkeypatch):
    class FailingSession:
        def execute(self, *args, **kwargs):
            raise SQLAlchemyError()

        def close(self):
            pass

    monkeypatch.setattr(main, "SessionLocal", lambda: FailingSession())
    client = TestClient(main.app)
    response = client.get("/healthcheck")
    assert response.status_code == 503
    assert response.json()["detail"] == "Database unavailable"
