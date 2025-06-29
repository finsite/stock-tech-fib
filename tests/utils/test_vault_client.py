import os
import unittest
from unittest.mock import patch

from app.utils.vault_client import get_secret_or_env


class TestVaultClient(unittest.TestCase):
    @patch.dict(os.environ, {"TEST_SECRET": "fallback_value"})
    def test_get_secret_or_env_fallback(self):
        self.assertEqual(get_secret_or_env("TEST_SECRET"), "fallback_value")


if __name__ == "__main__":
    unittest.main()
