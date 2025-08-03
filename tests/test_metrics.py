import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import main
from fastapi.testclient import TestClient

client = TestClient(main.app)


def _get_request_count(path: str, method: str = "GET", status: str = "404") -> float:
    value = main.PROMETHEUS_REGISTRY.get_sample_value(
        "requests_total", {"method": method, "path": path, "status_code": status}
    )
    return value or 0.0


def _get_latency_count(path: str, method: str = "GET") -> float:
    value = main.PROMETHEUS_REGISTRY.get_sample_value(
        "request_latency_seconds_count", {"method": method, "path": path}
    )
    return value or 0.0


def test_metrics_use_route_template():
    template_path = "/opportunities/{opportunity_id}"
    count_before = _get_request_count(template_path)
    latency_before = _get_latency_count(template_path)

    response = client.get("/opportunities/123")
    assert response.status_code == 404

    count_after = _get_request_count(template_path)
    latency_after = _get_latency_count(template_path)

    assert count_after == count_before + 1
    assert latency_after == latency_before + 1
    # Ensure metrics are not recorded with the concrete path
    assert _get_request_count("/opportunities/123") == 0.0
