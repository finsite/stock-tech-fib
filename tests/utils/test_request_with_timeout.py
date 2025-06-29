import unittest

from app.utils.request_with_timeout import request_with_timeout


class TestRequestWithTimeout(unittest.TestCase):
    def test_request_with_invalid_url(self):
        self.assertIsNone(request_with_timeout(""))


if __name__ == "__main__":
    unittest.main()
