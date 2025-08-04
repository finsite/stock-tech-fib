import os
from unittest.mock import patch

import pytest

from app import config_shared as config


@patch.dict(os.environ, {}, clear=True)
def test_get_polling_interval_default():
    assert config.get_polling_interval() == 60


@patch.dict(os.environ, {"POLLING_INTERVAL": "10"})
def test_get_polling_interval_from_env():
    assert config.get_polling_interval() == 10
