"""Module to publish processed data to RabbitMQ or AWS SQS.

This module provides a function to publish a list of processed data
dictionaries to the appropriate queue type (RabbitMQ or SQS), based on
shared configuration. Each message is retried with exponential backoff
upon failure.
"""

import json
from typing import Any

import boto3
import pika
from botocore.exceptions import BotoCoreError, NoCredentialsError
from pika.exceptions import AMQPConnectionError
from tenacity import retry, stop_after_attempt, wait_exponential

from app import config_shared
from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)

REDACT_SENSITIVE_LOGS = (
    config_shared.get_config_value("REDACT_SENSITIVE_LOGS", "true").lower() == "true"
)


def safe_log_message(data: dict[str, Any]) -> str:
    """Return redacted or full string for logging."""
    return "[REDACTED]" if REDACT_SENSITIVE_LOGS else json.dumps(data, ensure_ascii=False)


def publish_to_queue(payload: list[dict[str, Any]]) -> None:
    """Publish processed results to RabbitMQ or SQS.

    Parameters
    ----------
    payload : list[dict[str, Any]]
        A list of message payloads to publish.
    """
    if not isinstance(payload, list):
        logger.error("❌ Invalid payload type: expected list, got %s", type(payload).__name__)
        return

    queue_type = config_shared.get_queue_type().lower()

    for message in payload:
        if queue_type == "rabbitmq":
            _send_to_rabbitmq(message)
        elif queue_type == "sqs":
            _send_to_sqs(message)
        else:
            redacted_type = "[REDACTED]" if REDACT_SENSITIVE_LOGS else queue_type
            logger.error("❌ Invalid QUEUE_TYPE specified. Value may be misconfigured or missing.")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
def _send_to_rabbitmq(data: dict[str, Any]) -> None:
    """Send a single message to RabbitMQ.

    Parameters
    ----------
    data : dict[str, Any]
        The message payload to publish.

    Raises
    ------
    AMQPConnectionError
        If connection to RabbitMQ fails.
    Exception
        If message publishing fails.
    """
    try:
        credentials = pika.PlainCredentials(
            config_shared.get_rabbitmq_user(), config_shared.get_rabbitmq_password()
        )
        parameters = pika.ConnectionParameters(
            host=config_shared.get_rabbitmq_host(),
            port=config_shared.get_rabbitmq_port(),
            virtual_host=config_shared.get_rabbitmq_vhost(),
            credentials=credentials,
            blocked_connection_timeout=30,
        )

        with pika.BlockingConnection(parameters) as connection:
            channel = connection.channel()
            channel.basic_publish(
                exchange=config_shared.get_rabbitmq_exchange(),
                routing_key=config_shared.get_rabbitmq_routing_key(),
                body=json.dumps(data, ensure_ascii=False),
            )

        logger.info("✅ Published message to RabbitMQ: %s", safe_log_message(data))  # nosec

    except AMQPConnectionError as e:
        logger.exception("❌ RabbitMQ publish connection error: %s", e)
        raise
    except Exception as e:
        logger.exception("❌ Failed to publish message to RabbitMQ: %s", e)
        raise


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
def _send_to_sqs(data: dict[str, Any]) -> None:
    """Send a single message to AWS SQS.

    Parameters
    ----------
    data : dict[str, Any]
        The message payload to publish.

    Raises
    ------
    BotoCoreError
        If the boto3 client fails to initialize.
    NoCredentialsError
        If credentials are not available.
    Exception
        If message publishing fails.
    """
    sqs_url = config_shared.get_sqs_queue_url()
    region = config_shared.get_sqs_region()

    try:
        sqs_client = boto3.client("sqs", region_name=region)
        response = sqs_client.send_message(
            QueueUrl=sqs_url,
            MessageBody=json.dumps(data, ensure_ascii=False),
        )
        logger.info("✅ Published message to SQS: %s", safe_log_message(data))  # nosec

    except (BotoCoreError, NoCredentialsError) as e:
        logger.exception("❌ Failed to initialize SQS client: %s", e)
        raise
    except Exception as e:
        logger.exception("❌ Failed to publish message to SQS: %s", e)
        raise
