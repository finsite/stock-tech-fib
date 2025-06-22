from app.utils.request_with_timeout import request_with_timeout

def test_request_with_invalid_url():
    assert request_with_timeout("") is None
