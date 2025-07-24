import os
import unittest
from unittest.mock import patch

from app.utils.vault_client import get_config_value_cached


class TestVaultConfigFallback(unittest.TestCase):
    @patch.dict(os.environ, {"TEST_SECRET": "fallback_value"})
    @patch("app.utils.vault_client.VaultClient.get", return_value=None)
    def test_get_config_value_cached_returns_env(self, mock_vault_get):
        result = get_config_value_cached("TEST_SECRET", default="default_value")
        self.assertEqual(result, "fallback_value")
        mock_vault_get.assert_called_once_with("TEST_SECRET", fallback="fallback_value")

    @patch.dict(os.environ, {}, clear=True)
    @patch("app.utils.vault_client.VaultClient.get", return_value=None)
    def test_get_config_value_cached_uses_default(self, mock_vault_get):
        result = get_config_value_cached("MISSING_KEY", default="default_from_code")
        self.assertEqual(result, "default_from_code")

    @patch.dict(os.environ, {}, clear=True)
    @patch("app.utils.vault_client.VaultClient.get", return_value=None)
    def test_get_config_value_cached_raises_if_missing(self, mock_vault_get):
        with self.assertRaises(ValueError):
            get_config_value_cached("NON_EXISTENT_KEY")


if __name__ == "__main__":
    unittest.main()
