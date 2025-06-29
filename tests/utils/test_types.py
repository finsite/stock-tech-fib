import unittest

from app.utils.types import (
    is_valid_batch,
    is_valid_payload,
    is_valid_trade_event,
    validate_dict,
    validate_list_of_dicts,
)


class TestTypes(unittest.TestCase):
    def test_validate_dict(self):
        self.assertTrue(validate_dict({"a": 1, "b": 2}, ["a", "b"]))
        self.assertFalse(validate_dict({"a": 1}, ["a", "b"]))

    def test_validate_list_of_dicts(self):
        valid = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
        invalid = [{"a": 1}, "not a dict"]
        self.assertTrue(validate_list_of_dicts(valid, ["a", "b"]))
        self.assertFalse(validate_list_of_dicts(invalid, ["a"]))

    def test_is_valid_payload(self):
        self.assertTrue(is_valid_payload({"symbol": "AAPL", "timestamp": "2023-01-01T00:00:00Z"}))
        self.assertFalse(is_valid_payload({"symbol": "AAPL"}))

    def test_is_valid_batch(self):
        valid = [{"symbol": "AAPL", "timestamp": "2023-01-01T00:00:00Z"}]
        invalid = [{"symbol": "AAPL"}]
        self.assertTrue(is_valid_batch(valid))
        self.assertFalse(is_valid_batch(invalid))

    def test_is_valid_trade_event(self):
        valid = {
            "symbol": "AAPL",
            "action": "BUY",
            "quantity": 10,
            "price": 150.0,
            "timestamp": "2023-01-01T00:00:00Z",
        }
        invalid = {"symbol": "AAPL", "action": "HOLD"}
        self.assertTrue(is_valid_trade_event(valid))
        self.assertFalse(is_valid_trade_event(invalid))


if __name__ == "__main__":
    unittest.main()
