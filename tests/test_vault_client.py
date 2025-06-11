"""
Unit tests for vault_client.py
"""

import unittest
from unittest.mock import patch

from app.utils.vault_client import get_secret_from_vault


class TestVaultClient(unittest.TestCase):
    @patch("app.utils.vault_client.requests.get")
    def test_get_secret_from_vault_success(self, mock_get):
        """Test successful Vault secret retrieval."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "data": {"data": {"API_KEY": "123"}}
        }

        secret = get_secret_from_vault("my/path")
        self.assertEqual(secret["API_KEY"], "123")


if __name__ == "__main__":
    unittest.main()
