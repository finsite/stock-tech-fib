"""
Unit tests for vault_client.py
"""

import os
from unittest.mock import patch

import pytest

from app.utils.vault_client import get_secret_or_env


@patch.dict(os.environ, {"API_KEY": "env_value"})
def test_get_secret_or_env_env_var():
    """Returns value from environment if present."""
    assert get_secret_or_env("API_KEY") == "env_value"  # nosec


@patch.dict(os.environ, {}, clear=True)
@patch("app.utils.vault_client.VaultClient.get", return_value="vault_value")
@patch("app.utils.vault_client._vault_client", new=None)
def test_get_secret_or_env_vault_value(mock_get):
    """Returns value from Vault if not in environment."""
    with patch("app.utils.vault_client.VaultClient") as mock_class:
        mock_instance = mock_class.return_value
        mock_instance.get.return_value = "vault_value"

        result = get_secret_or_env("API_KEY")
        assert result == "vault_value"  # nosec
        mock_instance.get.assert_called_once_with("API_KEY", "")


@patch.dict(os.environ, {}, clear=True)
@patch("app.utils.vault_client.VaultClient.get", return_value=None)
@patch("app.utils.vault_client._vault_client", new=None)
def test_get_secret_or_env_default(mock_get):
    """Returns default if Vault and env both missing."""
    with patch("app.utils.vault_client.VaultClient") as mock_class:
        mock_instance = mock_class.return_value
        mock_instance.get.return_value = None

        result = get_secret_or_env("MISSING_KEY", default="fallback")
        assert result == "fallback"  # nosec
