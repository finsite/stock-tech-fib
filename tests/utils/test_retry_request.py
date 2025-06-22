import pytest
from app.utils.retry_request import retry_request

def test_retry_success():
    assert retry_request(lambda: 42) == 42

def test_retry_failure():
    def fail():
        raise ValueError("fail")
    with pytest.raises(ValueError):
        retry_request(fail, max_retries=2, delay_seconds=0)
