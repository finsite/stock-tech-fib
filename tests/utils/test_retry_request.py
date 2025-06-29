import unittest

from app.utils.retry_request import retry_request


class TestRetryRequest(unittest.TestCase):
    def test_retry_success(self):
        self.assertEqual(retry_request(lambda: 42), 42)

    def test_retry_failure(self):
        def fail():
            raise ValueError("fail")

        with self.assertRaises(ValueError):
            retry_request(fail, max_retries=2, delay_seconds=0)


if __name__ == "__main__":
    unittest.main()
