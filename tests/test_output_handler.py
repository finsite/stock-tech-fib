"""
Unit tests for output_handler.py
"""

import unittest
from unittest.mock import patch

from app.output_handler import send_to_postgres


class TestSendToPostgres(unittest.TestCase):
    @patch("app.output_handler.psycopg2.connect")
    def test_send_to_postgres(self, mock_connect):
        """Test that send_to_postgres calls execute on the database cursor."""
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        test_data = [{"symbol": "AAPL", "price": 123.45}]
        send_to_postgres(test_data)

        self.assertTrue(
            mock_cursor.execute.called,
            "Expected cursor.execute to be called, but it wasn't.",
        )


if __name__ == "__main__":
    unittest.main()
