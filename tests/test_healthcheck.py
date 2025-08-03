import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import main
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Optional
from prometheus_client.parser import text_string_to_metric_families


def _get_metric_value(metrics_text: str, endpoint: str, status: str) -> Optional[float]:
    for family in text_string_to_metric_families(metrics_text):
        if family.name == "request_count":
            for sample in family.samples:
                if (
                    sample.labels.get("endpoint") == endpoint
                    and sample.labels.get("http_status") == status
                ):
                    return sample.value
    return None


def test_healthcheck_success(caplog):
    client = TestClient(main.app)
    with caplog.at_level(logging.INFO):
        response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "GET /healthcheck" in caplog.text
    metrics_resp = client.get("/metrics")
    value = _get_metric_value(metrics_resp.text, "/healthcheck", "200")
    assert value is not None and value >= 1


def test_healthcheck_db_failure(monkeypatch, caplog):
    class FailingSession:
        def execute(self, *args, **kwargs):
            raise SQLAlchemyError()

        def close(self):
            pass

    monkeypatch.setattr(main, "SessionLocal", lambda: FailingSession())
    client = TestClient(main.app)
    with caplog.at_level(logging.ERROR):
        response = client.get("/healthcheck")
    assert response.status_code == 503
    assert response.json()["detail"] == "Database unavailable"
    assert "status=503" in caplog.text
    metrics_resp = client.get("/metrics")
    value = _get_metric_value(metrics_resp.text, "/healthcheck", "503")
    assert value is not None and value >= 1
