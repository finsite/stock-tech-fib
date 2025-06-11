"""
Unit tests for vault_client.py
"""

import os
import pytest
from unittest.mock import patch

from app.utils.vault_client import get_secret_from_vault


@patch("app.utils.vault_client.requests.get")
@patch.dict(os.environ, {"VAULT_ADDR": "http://vault:8200", "VAULT_TOKEN": "dummy-token"})
def test_get_secret_from_vault_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": {"data": {"API_KEY": "123"}}}

    secret = get_secret_from_vault("my/path")
    assert secret["API_KEY"] == "123"


@patch("app.utils.vault_client.requests.get")
@patch.dict(os.environ, {"VAULT_ADDR": "http://vault:8200", "VAULT_TOKEN": "dummy-token"})
def test_get_secret_from_vault_non_200(mock_get):
    mock_get.return_value.status_code = 403
    mock_get.return_value.text = "Forbidden"

    with pytest.raises(RuntimeError, match="Vault request failed"):
        get_secret_from_vault("my/path")


@patch("app.utils.vault_client.requests.get")
@patch.dict(os.environ, {"VAULT_ADDR": "http://vault:8200", "VAULT_TOKEN": "dummy-token"})
def test_get_secret_from_vault_invalid_json(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = ValueError("Invalid JSON")

    with pytest.raises(ValueError):
        get_secret_from_vault("my/path")


@patch("app.utils.vault_client.requests.get", side_effect=Exception("Connection error"))
@patch.dict(os.environ, {"VAULT_ADDR": "http://vault:8200", "VAULT_TOKEN": "dummy-token"})
def test_get_secret_from_vault_request_exception(mock_get):
    with pytest.raises(Exception, match="Connection error"):
        get_secret_from_vault("my/path")
