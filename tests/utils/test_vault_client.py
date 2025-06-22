import pytest
from app.utils.vault_client import get_secret_or_env

def test_get_secret_or_env_fallback(monkeypatch):
    monkeypatch.setenv("TEST_SECRET", "fallback_value")
    assert get_secret_or_env("TEST_SECRET") == "fallback_value"
