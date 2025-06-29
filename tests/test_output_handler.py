"""Unit tests for output_handler.py"""

import unittest
from unittest.mock import patch, MagicMock

from app.output_handler import send_to_output, output_handler


class TestSendToOutput(unittest.TestCase):
    @patch("app.output_handler.publish_to_queue")
    @patch("app.output_handler.get_config_value", return_value="queue")
    @patch("app.output_handler.config_shared.get_output_modes", return_value=["queue"])
    def test_send_to_output_queue(
        self, mock_modes, mock_get_config_value, mock_publish
    ):
        data = [{"text": "test message"}]
        send_to_output(data)
        mock_publish.assert_called_once_with(data)

    @patch("app.output_handler.config_shared.get_output_modes", return_value=["log"])
    def test_send_to_output_log(self, mock_modes):
        data = [{"text": "log message"}]
        with patch("app.output_handler.logger") as mock_logger:
            send_to_output(data)
            mock_logger.info.assert_called()

    @patch("app.output_handler.config_shared.get_output_modes", return_value=["stdout"])
    def test_send_to_output_stdout(self, mock_modes):
        data = [{"text": "stdout message"}]
        with patch("builtins.print") as mock_print:
            send_to_output(data)
            mock_print.assert_called()

    @patch("app.output_handler.config_shared.get_paper_trading_enabled", return_value=True)
    @patch("app.output_handler.config_shared.get_paper_trade_mode", return_value="log")
    def test_send_paper_trade_log(self, mock_mode, mock_enabled):
        data = [{"text": "paper message"}]
        with patch("app.output_handler.logger") as mock_logger:
            send_to_output(data)
            mock_logger.info.assert_called()

    @patch("app.output_handler.config_shared.get_output_modes", return_value=["invalid"])
    def test_send_to_output_invalid_mode(self, mock_modes):
        data = [{"text": "invalid message"}]
        with patch("app.output_handler.logger") as mock_logger:
            send_to_output(data)
            mock_logger.warning.assert_called_with("⚠️ Unhandled output mode: %s", "invalid")


class TestPaperTradeMethods(unittest.TestCase):
    @patch("app.output_handler.config_shared.get_paper_trading_queue_name", return_value="paper-queue")
    @patch("app.output_handler.config_shared.get_paper_trading_exchange", return_value="paper-exchange")
    @patch("app.output_handler.publish_to_queue")
    def test_output_paper_trade_to_queue(self, mock_publish, *_):
        data = {"symbol": "AAPL", "price": 123.45}
        output_handler._output_paper_trade_to_queue(data)
        mock_publish.assert_called_once()

    def test_output_paper_trade_to_database_stub(self):
        data = {"symbol": "AAPL"}
        with patch("app.output_handler.logger") as mock_logger:
            output_handler._output_paper_trade_to_database(data)
            mock_logger.warning.assert_called_with("⚠️ Paper trading database integration not implemented.")


if __name__ == "__main__":
    unittest.main()
