"""Module to publish processed analysis data to RabbitMQ or AWS SQS."""

import json
import os

import boto3
import pika
from botocore.exceptions import BotoCoreError, NoCredentialsError

from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Get queue type from environment
QUEUE_TYPE = os.getenv("QUEUE_TYPE", "rabbitmq").lower()

# RabbitMQ config
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "stock_analysis")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "candlestick")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

# SQS config
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")
SQS_REGION = os.getenv("SQS_REGION", "us-east-1")

# Initialize SQS client if needed
sqs_client = None
if QUEUE_TYPE == "sqs":
    try:
        sqs_client = boto3.client("sqs", region_name=SQS_REGION)
        logger.info(f"SQS client initialized for region {SQS_REGION}")
    except (BotoCoreError, NoCredentialsError) as e:
        logger.error("Failed to initialize SQS client: %s", e)
        sqs_client = None


def publish_to_queue(payload: list[dict]) -> None:
    """
    Publishes the processed stock analysis results to RabbitMQ or SQS.

    Args:
        payload (list[dict]): A list of dictionaries representing processed results.
    """
    for message in payload:
        if QUEUE_TYPE == "rabbitmq":
            _send_to_rabbitmq(message)
        elif QUEUE_TYPE == "sqs":
            _send_to_sqs(message)
        else:
            logger.error("Invalid QUEUE_TYPE specified. Use 'rabbitmq' or 'sqs'.")


def _send_to_rabbitmq(data: dict) -> None:
    """Helper to send a message to RabbitMQ."""
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                virtual_host=RABBITMQ_VHOST,
                credentials=credentials,
            )
        )
        channel = connection.channel()

        channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE,
            routing_key=RABBITMQ_ROUTING_KEY,
            body=json.dumps(data),
        )
        connection.close()
        logger.info("Published message to RabbitMQ")
    except Exception as e:
        logger.error("Failed to publish message to RabbitMQ: %s", e)


def _send_to_sqs(data: dict) -> None:
    """Helper to send a message to AWS SQS."""
    if not sqs_client or not SQS_QUEUE_URL:
        logger.error("SQS client is not initialized or missing SQS_QUEUE_URL")
        return

    try:
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(data),
        )
        logger.info("Published message to SQS, MessageId: %s", response["MessageId"])
    except Exception as e:
        logger.error("Failed to publish message to SQS: %s", e)
