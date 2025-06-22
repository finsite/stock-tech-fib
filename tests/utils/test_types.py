from app.utils.types import validate_dict, validate_list_of_dicts, is_valid_payload, is_valid_batch

def test_validate_dict():
    assert validate_dict({"a": 1, "b": 2}, ["a", "b"]) is True

def test_validate_list_of_dicts():
    data = [{"symbol": "AAPL", "timestamp": "2021-01-01"}]
    assert validate_list_of_dicts(data, ["symbol", "timestamp"]) is True

def test_is_valid_payload():
    assert is_valid_payload({"symbol": "AAPL", "timestamp": "2021-01-01"}) is True

def test_is_valid_batch():
    assert is_valid_batch([{"symbol": "AAPL", "timestamp": "2021-01-01"}]) is True
