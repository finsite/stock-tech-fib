"""Prometheus metrics server starter for application-level monitoring.

This module provides a function to expose Prometheus-compatible metrics
over HTTP, typically used to allow Prometheus to scrape custom application
metrics from each running service instance.

The port and enablement flag are controlled via environment variables:
- METRICS_ENABLED (default: "true")
- METRICS_PORT (default: "8000")
"""

import os

from prometheus_client import start_http_server


def start_metrics_server() -> None:
    """Conditionally start the Prometheus metrics HTTP server.

    This starts a simple HTTP server to expose metrics from the global
    Prometheus client registry on the given port. If the environment
    variable METRICS_ENABLED is not set to a truthy value, the server
    is not started.

    Environment Variables:
        METRICS_ENABLED (str): If "true" (default), start the server.
        METRICS_PORT (str/int): Port to bind the metrics server (default: 8000).

    Raises:
        ValueError: If METRICS_PORT is not a valid integer.

    Example:
        start_metrics_server()  # Will start if METRICS_ENABLED is true

    """
    enabled = os.getenv("METRICS_ENABLED", "true").lower()
    if enabled not in ("1", "true", "yes"):
        return

    port_str = os.getenv("METRICS_PORT", "8000")

    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(f"Invalid METRICS_PORT value: {port_str}")

    start_http_server(port)
