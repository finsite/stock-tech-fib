"""Message publisher module for RabbitMQ or AWS SQS.

Handles publishing of processed data to the appropriate messaging queue,
with retry logic, structured logging, redaction, and Prometheus metrics.
"""

import json
import time
from typing import Any

import boto3
import pika
from botocore.exceptions import BotoCoreError, NoCredentialsError
from pika.exceptions import AMQPConnectionError
from tenacity import retry, stop_after_attempt, wait_exponential

from app import config_shared
from app.utils.metrics import queue_publish_counter, queue_publish_latency
from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)

REDACT_SENSITIVE_LOGS = (
    config_shared.get_config_value("REDACT_SENSITIVE_LOGS", "true").lower() == "true"
)


class SQSMessageSendError(Exception):
    """Raised when SQS returns a non-200 HTTP status."""


def safe_log_message(data: dict[str, Any]) -> str:
    """Return redacted or full version of a message for logging.

    Args:
        data (dict[str, Any]): The message payload.

    Returns:
        str: JSON string or redacted placeholder.

    """
    return "[REDACTED]" if REDACT_SENSITIVE_LOGS else json.dumps(data, ensure_ascii=False)


def publish_to_queue(
    payload: list[dict[str, Any]],
    queue: str | None = None,
    exchange: str | None = None,
) -> None:
    """Publish a batch of processed messages to the configured queue.

    Args:
        payload (list[dict[str, Any]]): List of messages to send.
        queue (str | None): Optional override for queue name or routing key.
        exchange (str | None): Optional override for RabbitMQ exchange.

    """
    if not isinstance(payload, list):
        logger.error("❌ Invalid payload type: expected list, got %s", type(payload).__name__)
        return

    queue_type = config_shared.get_queue_type().lower()

    for message in payload:
        if queue_type == "rabbitmq":
            _send_to_rabbitmq(message, queue, exchange)
        elif queue_type == "sqs":
            _send_to_sqs(message, queue)
        else:
            redacted_type = "[REDACTED]" if REDACT_SENSITIVE_LOGS else queue_type
            logger.error("❌ Invalid QUEUE_TYPE: %s", redacted_type)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
def _send_to_rabbitmq(
    data: dict[str, Any],
    routing_key: str | None = None,
    exchange: str | None = None,
) -> None:
    """Send a single message to RabbitMQ.

    Args:
        data (dict[str, Any]): The message payload.
        routing_key (str | None): Optional routing key override.
        exchange (str | None): Optional exchange override.

    Raises:
        AMQPConnectionError: On RabbitMQ connection failure.
        Exception: On publish failure.

    """
    start = time.perf_counter()
    try:
        credentials = pika.PlainCredentials(
            config_shared.get_rabbitmq_user(),
            config_shared.get_rabbitmq_password(),
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
            resolved_exchange = exchange or config_shared.get_rabbitmq_exchange()
            resolved_routing_key = routing_key or config_shared.get_rabbitmq_routing_key()
            channel.basic_publish(
                exchange=resolved_exchange,
                routing_key=resolved_routing_key,
                body=json.dumps(data, ensure_ascii=False),
            )

        duration = time.perf_counter() - start
        queue_publish_counter.labels(queue_type="rabbitmq", status="success").inc()
        queue_publish_latency.labels(queue_type="rabbitmq", status="success").observe(duration)
        logger.info("✅ Published message to RabbitMQ: %s", safe_log_message(data))  # nosec

    except AMQPConnectionError as e:
        duration = time.perf_counter() - start
        queue_publish_counter.labels(queue_type="rabbitmq", status="failure").inc()
        queue_publish_latency.labels(queue_type="rabbitmq", status="failure").observe(duration)
        logger.exception("❌ RabbitMQ publish connection error: %s", e)
        raise
    except Exception as e:
        duration = time.perf_counter() - start
        queue_publish_counter.labels(queue_type="rabbitmq", status="exception").inc()
        queue_publish_latency.labels(queue_type="rabbitmq", status="exception").observe(duration)
        logger.exception("❌ Failed to publish message to RabbitMQ: %s", e)
        raise


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
def _send_to_sqs(
    data: dict[str, Any],
    queue_name: str | None = None,
) -> None:
    """Send a single message to AWS SQS.

    Args:
        data (dict[str, Any]): The message payload.
        queue_name (str | None): Optional override for SQS queue URL.

    Raises:
        BotoCoreError: On SQS client error.
        NoCredentialsError: If AWS credentials are not available.
        SQSMessageSendError: If HTTP response code is not 200.
        Exception: On publish failure.

    """
    sqs_url = queue_name or config_shared.get_sqs_queue_url()
    region = config_shared.get_sqs_region()

    start = time.perf_counter()
    try:
        sqs_client = boto3.client("sqs", region_name=region)
        response = sqs_client.send_message(
            QueueUrl=sqs_url,
            MessageBody=json.dumps(data, ensure_ascii=False),
        )

        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        duration = time.perf_counter() - start

        if status_code != 200:
            queue_publish_counter.labels(queue_type="sqs", status="failure").inc()
            queue_publish_latency.labels(queue_type="sqs", status="failure").observe(duration)
            logger.error("❌ Failed to publish message to SQS: HTTP %d", status_code)
            raise SQSMessageSendError(f"SQS returned HTTP status {status_code}")

        queue_publish_counter.labels(queue_type="sqs", status="success").inc()
        queue_publish_latency.labels(queue_type="sqs", status="success").observe(duration)
        logger.info("✅ Published message to SQS: %s", safe_log_message(data))  # nosec

    except (BotoCoreError, NoCredentialsError) as e:
        duration = time.perf_counter() - start
        queue_publish_counter.labels(queue_type="sqs", status="failure").inc()
        queue_publish_latency.labels(queue_type="sqs", status="failure").observe(duration)
        logger.exception("❌ Failed to initialize SQS client: %s", e)
        raise
    except Exception as e:
        duration = time.perf_counter() - start
        queue_publish_counter.labels(queue_type="sqs", status="exception").inc()
        queue_publish_latency.labels(queue_type="sqs", status="exception").observe(duration)
        logger.exception("❌ Failed to publish message to SQS: %s", e)
        raise
