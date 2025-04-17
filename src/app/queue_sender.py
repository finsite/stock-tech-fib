"""Module to publish messages to a message queue (RabbitMQ or SQS).
"""

import json
import os
import time
from typing import Literal

import boto3
import pika
from botocore.exceptions import BotoCoreError, NoCredentialsError

from app.logger import setup_logger

logger = setup_logger(__name__)


class QueueSender:
    """Sends messages to RabbitMQ or SQS based on configuration."""

    def __init__(
        self,
        queue_type: Literal["rabbitmq", "sqs"] = os.getenv("QUEUE_TYPE", "rabbitmq").lower(),
        rabbitmq_host: str = os.getenv("RABBITMQ_HOST", "localhost"),
        rabbitmq_exchange: str = os.getenv("RABBITMQ_EXCHANGE", "stock_analysis"),
        rabbitmq_routing_key: str = os.getenv("RABBITMQ_ROUTING_KEY", "default"),
        rabbitmq_vhost: str = os.getenv("RABBITMQ_VHOST", "/"),
        sqs_queue_url: str = os.getenv("SQS_QUEUE_URL", ""),
    ):
        self.queue_type = queue_type
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_exchange = rabbitmq_exchange
        self.rabbitmq_routing_key = rabbitmq_routing_key
        self.rabbitmq_vhost = rabbitmq_vhost
        self.sqs_queue_url = sqs_queue_url
        self.sqs_client = None
        self.connection = None
        self.channel = None

        if self.queue_type == "sqs":
            try:
                self.sqs_client = boto3.client(
                    "sqs", region_name=os.getenv("AWS_REGION", "us-east-1")
                )
                logger.info("Initialized SQS client")
            except (BotoCoreError, NoCredentialsError) as e:
                logger.error("Failed to initialize SQS client: %s", e)
                raise
        elif self.queue_type == "rabbitmq":
            self._connect_to_rabbitmq()
        else:
            raise ValueError("QUEUE_TYPE must be 'rabbitmq' or 'sqs'")

    def _connect_to_rabbitmq(self) -> None:
        """Establishes a RabbitMQ connection with retries."""
        retries = 5
        for attempt in range(1, retries + 1):
            try:
                params = pika.ConnectionParameters(
                    host=self.rabbitmq_host,
                    virtual_host=self.rabbitmq_vhost,
                    heartbeat=600,
                    blocked_connection_timeout=300,
                )
                self.connection = pika.BlockingConnection(params)
                self.channel = self.connection.channel()
                logger.info("Connected to RabbitMQ")
                return
            except Exception as e:
                logger.warning(
                    "RabbitMQ connection failed (attempt %d/%d): %s",
                    attempt,
                    retries,
                    e,
                )
                time.sleep(5)
        raise ConnectionError("Failed to connect to RabbitMQ after retries.")

    def send_message(self, message: dict) -> None:
        """Sends a message to the configured queue system."""
        payload = json.dumps(message)

        if self.queue_type == "rabbitmq":
            try:
                self.channel.basic_publish(
                    exchange=self.rabbitmq_exchange,
                    routing_key=self.rabbitmq_routing_key,
                    body=payload,
                )
                logger.info("Message sent to RabbitMQ")
            except Exception as e:
                logger.error("Failed to send message to RabbitMQ: %s", e)
                raise
        elif self.queue_type == "sqs":
            try:
                response = self.sqs_client.send_message(
                    QueueUrl=self.sqs_queue_url,
                    MessageBody=payload,
                )
                logger.info("Message sent to SQS: %s", response.get("MessageId"))
            except Exception as e:
                logger.error("Failed to send message to SQS: %s", e)
                raise

    def close(self) -> None:
        """Closes any open connections (mainly RabbitMQ)."""
        if self.connection and self.connection.is_open:
            self.connection.close()
            logger.info("RabbitMQ connection closed")

    def flush(self) -> None:
        """Placeholder for any flush behavior."""
        logger.debug("Flush called - no action taken")

    def health_check(self) -> bool:
        """Returns True if the sender is healthy."""
        if self.queue_type == "rabbitmq":
            return self.connection.is_open if self.connection else False
        if self.queue_type == "sqs":
            return self.sqs_client is not None
        return False
