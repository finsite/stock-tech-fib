"""Unit tests for config.py."""

import unittest
from unittest.mock import patch

from app import config_shared as config


class TestConfig(unittest.TestCase):
    @patch.dict("os.environ", {"POLLING_INTERVAL": "10"})
    def test_get_polling_interval_from_env(self):
        self.assertEqual(config.get_polling_interval(), 10)

    @patch.dict("os.environ", {}, clear=True)
    def test_get_polling_interval_default(self):
        self.assertEqual(config.get_polling_interval(), 30)  # or whatever your default is


if __name__ == "__main__":
    unittest.main()
