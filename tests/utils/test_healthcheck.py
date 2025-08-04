import pytest

from app.utils import healthcheck


def test_health_flag_behavior():
    healthcheck.mark_healthy()
    assert healthcheck.is_healthy() is True


def test_ready_endpoint():
    healthcheck.mark_unready()
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    @app.get("/ready")
    def ready():
        return (
            {"status": "ok"} if healthcheck.is_healthy() else {"status": "not ready"},
            200 if healthcheck.is_healthy() else 503,
        )

    client = TestClient(app)
    response = client.get("/ready")
    assert response.status_code == 503
