import os
import pytest
from app.utils.validate_environment_variables import validate_environment_variables

def test_validate_environment_variables_success(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "value")
    validate_environment_variables(["TEST_VAR"])

def test_validate_environment_variables_failure(monkeypatch):
    monkeypatch.delenv("MISSING_VAR", raising=False)
    with pytest.raises(OSError):
        validate_environment_variables(["MISSING_VAR"])
