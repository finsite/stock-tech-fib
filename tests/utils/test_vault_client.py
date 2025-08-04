import os
from unittest.mock import patch

from app.utils.vault_client import get_config_value_cached


@patch.dict(os.environ, {"TEST_SECRET": "secret_value"})
def test_get_config_value_cached_returns_env():
    value = get_config_value_cached("TEST_SECRET")
    assert value == "secret_value"


@patch.dict(os.environ, {}, clear=True)
def test_get_config_value_cached_uses_default():
    value = get_config_value_cached("MISSING_KEY", default="default")
    assert value == "default"
