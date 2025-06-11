"""
Unit tests for queue_handler.py
"""

import unittest
from unittest.mock import MagicMock, patch

from app.queue_handler import consume_messages


class TestQueueHandler(unittest.TestCase):
    @patch("app.queue_handler.config.get_queue_type", return_value="rabbitmq")
    @patch("app.queue_handler.pika.BlockingConnection")
    def test_consume_messages_rabbitmq(self, mock_connection, mock_get_queue_type):
        """Test that RabbitMQ consumer sets up basic_consume or basic_qos."""
        mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = mock_channel

        consume_messages(lambda batch: None)

        self.assertTrue(
            mock_channel.basic_consume.called or mock_channel.basic_qos.called,
            "Expected basic_consume or basic_qos to be called, but it wasn't.",
        )


if __name__ == "__main__":
    unittest.main()
