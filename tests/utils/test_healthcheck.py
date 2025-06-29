import threading
import time
import unittest
from http.server import HTTPServer

import requests

from app.utils import healthcheck


class TestHealthcheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Reset health state
        healthcheck._readiness_flag = False
        healthcheck._health_flag = True

        # Start HTTP server
        port = 8089

        def run_server():
            server = HTTPServer(("localhost", port), healthcheck.HealthHandler)
            server.serve_forever()

        cls.thread = threading.Thread(target=run_server, daemon=True)
        cls.thread.start()
        time.sleep(0.5)

    def test_readiness_flag_behavior(self):
        self.assertFalse(healthcheck.is_ready())
        healthcheck.set_ready()
        self.assertTrue(healthcheck.is_ready())

    def test_health_flag_behavior(self):
        self.assertTrue(healthcheck.is_healthy())
        healthcheck.set_unhealthy()
        self.assertFalse(healthcheck.is_healthy())

    def test_health_endpoint(self):
        resp = requests.get("http://localhost:8089/health", timeout=5)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, "healthy")

        healthcheck.set_unhealthy()

        resp = requests.get("http://localhost:8089/health", timeout=5)
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(resp.text, "unhealthy")

    def test_ready_endpoint(self):
        resp = requests.get("http://localhost:8089/ready", timeout=5)
        self.assertEqual(resp.status_code, 503)
        self.assertEqual(resp.text, "not ready")

        healthcheck.set_ready()

        resp = requests.get("http://localhost:8089/ready", timeout=5)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.text, "ready")

    def test_unknown_endpoint(self):
        resp = requests.get("http://localhost:8089/unknown", timeout=5)
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.text, "not found")


if __name__ == "__main__":
    unittest.main()
