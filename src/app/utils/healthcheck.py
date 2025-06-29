"""Healthcheck utility module for readiness and liveness probes.

Provides application status flags and an optional HTTP server for use with
container orchestrators like Kubernetes or Docker.
"""

import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from app import config_shared

logger: logging.Logger = logging.getLogger(__name__)

# Service status flags
_readiness_flag: bool = False
_health_flag: bool = True


def is_ready() -> bool:
    """Check if the service is ready to handle requests.

    Returns:
        bool: True if the service has completed startup and is ready.

    """
    return _readiness_flag


def is_healthy() -> bool:
    """Check if the service is currently healthy.

    Returns:
        bool: True if the service is healthy and not in a failure state.

    """
    return _health_flag


def set_ready() -> None:
    """Mark the service as ready to handle traffic."""
    global _readiness_flag
    _readiness_flag = True
    logger.info("✅ Service marked as ready")


def set_unhealthy() -> None:
    """Mark the service as unhealthy (e.g., during shutdown or failure)."""
    global _health_flag
    _health_flag = False
    logger.warning("❌ Service marked as unhealthy")


class HealthHandler(BaseHTTPRequestHandler):
    """HTTP request handler for /health and /ready endpoints."""

    def do_GET(self) -> None:
        """Handle GET requests for readiness and liveness checks."""
        if self.path == "/health":
            status: int = 200 if is_healthy() else 500
            self.send_response(status)
            self.end_headers()
            self.wfile.write(b"healthy" if status == 200 else b"unhealthy")

        elif self.path == "/ready":
            status: int = 200 if is_ready() else 503
            self.send_response(status)
            self.end_headers()
            self.wfile.write(b"ready" if status == 200 else b"not ready")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")

    def log_message(self, format: str, *args: object) -> None:
        """Suppress default access log output from BaseHTTPRequestHandler."""
        pass


def start_health_server() -> None:
    """Start an HTTP server exposing /health and /ready endpoints.

    This server runs in a background thread and is intended for use with
    readiness and liveness probes in orchestration environments.
    """
    if not config_shared.get_healthcheck_enabled():
        logger.info("⚠️ Healthcheck server is disabled by configuration.")
        return

    host = config_shared.get_healthcheck_host()  # defaults to 127.0.0.1
    port = config_shared.get_healthcheck_port()  # defaults to 8081

    def serve() -> None:
        with HTTPServer((host, port), HealthHandler) as httpd:
            logger.info("📡 Healthcheck server running on %s:%d", host, port)
            httpd.serve_forever()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
