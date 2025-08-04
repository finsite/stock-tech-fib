from unittest.mock import MagicMock, patch

import pytest

from app import output_handler


@patch("app.output_handler.logger")
@patch("app.output_handler.get_output_modes", return_value=["print"])
def test_send_print(mock_modes, mock_logger):
    with patch("builtins.print") as mock_print:
        output_handler.send({"test": "value"})
        mock_print.assert_called()


@patch("app.output_handler.logger")
@patch("app.output_handler.get_output_modes", return_value=[])
def test_send_noop(mock_modes, mock_logger):
    output_handler.send({"test": "value"})
    mock_logger.warning.assert_called()
