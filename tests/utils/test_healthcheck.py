import time
import threading
from http.server import HTTPServer

import pytest
import requests

from app.utils import healthcheck


def test_readiness_flag_behavior() -> None:
    # Initial state: not ready
    assert not healthcheck.is_ready()

    # Set to ready
    healthcheck.set_ready()
    assert healthcheck.is_ready()


def test_health_flag_behavior() -> None:
    # Initial state: healthy
    assert healthcheck.is_healthy()

    # Mark as unhealthy
    healthcheck.set_unhealthy()
    assert not healthcheck.is_healthy()


@pytest.fixture(scope="module")
def health_server() -> None:
    # Reset health state
    global _httpd
    healthcheck._readiness_flag = False
    healthcheck._health_flag = True

    # Start HTTP server on test port
    port = 8089

    def run_server():
        server = HTTPServer(("localhost", port), healthcheck.HealthHandler)
        server.serve_forever()

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(0.5)  # Give time for server to start


@pytest.mark.usefixtures("health_server")
def test_health_endpoint() -> None:
    resp = requests.get("http://localhost:8089/health")
    assert resp.status_code == 200
    assert resp.text == "healthy"

    healthcheck.set_unhealthy()

    resp = requests.get("http://localhost:8089/health")
    assert resp.status_code == 500
    assert resp.text == "unhealthy"


@pytest.mark.usefixtures("health_server")
def test_ready_endpoint() -> None:
    resp = requests.get("http://localhost:8089/ready")
    assert resp.status_code == 503
    assert resp.text == "not ready"

    healthcheck.set_ready()

    resp = requests.get("http://localhost:8089/ready")
    assert resp.status_code == 200
    assert resp.text == "ready"


@pytest.mark.usefixtures("health_server")
def test_unknown_endpoint() -> None:
    resp = requests.get("http://localhost:8089/unknown")
    assert resp.status_code == 404
    assert resp.text == "not found"
