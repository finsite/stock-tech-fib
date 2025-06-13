"""
Unit tests for output_handler.py
"""

import unittest
from unittest.mock import MagicMock, patch

from app.output_handler import send_to_output


class TestSendToOutput(unittest.TestCase):
    @patch("app.output_handler.send_to_postgres")
    def test_send_to_output_default(self, mock_send_to_postgres):
        """Test that send_to_output delegates to send_to_postgres by default."""
        test_data = [{"symbol": "AAPL", "price": 123.45}]
        send_to_output(test_data)
        mock_send_to_postgres.assert_called_once_with(test_data)

    @patch("app.output_handler.send_to_sqs")
    @patch("app.output_handler.get_config_value", return_value="sqs")
    def test_send_to_output_sqs(self, mock_config, mock_send_to_sqs):
        """Test that send_to_output delegates to send_to_sqs if configured."""
        test_data = [{"symbol": "MSFT", "price": 321.00}]
        send_to_output(test_data)
        mock_send_to_sqs.assert_called_once_with(test_data)


if __name__ == "__main__":
    unittest.main()
