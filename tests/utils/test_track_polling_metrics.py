import pytest
from app.utils.track_polling_metrics import track_polling_metrics

def test_valid_status_success():
    track_polling_metrics("success", "test_source", "TEST")

def test_valid_status_failure():
    track_polling_metrics("failure", "test_source", "TEST")

def test_invalid_status():
    with pytest.raises(ValueError):
        track_polling_metrics("unknown", "test_source", "TEST")  # type: ignore[arg-type]
