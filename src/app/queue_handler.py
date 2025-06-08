"""Generic queue handler for RabbitMQ or SQS with batching and retries."""

import json
import signal
import threading
import time

import boto3
import pika
from botocore.exceptions import BotoCoreError, NoCredentialsError
from tenacity import retry, stop_after_attempt, wait_exponential

import app.config_shared as config
from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)
shutdown_event = threading.Event()


def consume_messages(callback):
    """Start the queue listener for the configured queue type.

    Registers signal handlers for graceful shutdown and delegates
    to either RabbitMQ or SQS listener based on configuration.
    """
    signal.signal(signal.SIGINT, _graceful_shutdown)
    signal.signal(signal.SIGTERM, _graceful_shutdown)

    queue_type = config.get_queue_type().lower()
    if queue_type == "rabbitmq":
        _start_rabbitmq_listener(callback)
    elif queue_type == "sqs":
        _start_sqs_listener(callback)
    else:
        raise ValueError(f"Unsupported QUEUE_TYPE: {queue_type}")


def _graceful_shutdown(signum, frame):
    """Handle shutdown signals to terminate listeners cleanly."""
    logger.info("🛑 Shutdown signal received, stopping listener...")
    shutdown_event.set()


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def _start_rabbitmq_listener(callback):
    """Connect to RabbitMQ and start consuming messages.

    Messages are passed to the callback in a consistent list format.
    Acknowledge successful messages and reject failures.
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=config.get_rabbitmq_host(),
            port=config.get_rabbitmq_port(),
            virtual_host=config.get_rabbitmq_vhost(),
            credentials=pika.PlainCredentials(
                config.get_rabbitmq_user(), config.get_rabbitmq_password()
            ),
        )
    )

    channel = connection.channel()
    queue_name = config.get_rabbitmq_queue()
    channel.queue_declare(queue=queue_name, durable=True)

    def on_message(channel, method, properties, body):
        try:
            data = json.loads(body)
            callback([data])  # single message wrapped in list for consistency
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"❌ Error processing RabbitMQ message: {e}")
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    channel.basic_consume(queue=queue_name, on_message_callback=on_message)

    logger.info("🚀 Consuming RabbitMQ messages from queue: %s", queue_name)
    while not shutdown_event.is_set():
        connection.process_data_events(time_limit=1)

    connection.close()
    logger.info("🛑 RabbitMQ listener stopped.")


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def _start_sqs_listener(callback):
    """Connect to AWS SQS and start polling messages.

    Polls the configured SQS queue in batches and deletes messages after processing.
    """
    sqs = boto3.client("sqs", region_name=config.get_sqs_region())
    queue_url = config.get_sqs_queue_url()

    logger.info("🚀 Polling SQS queue: %s", queue_url)
    while not shutdown_event.is_set():
        try:
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=config.get_batch_size(),
                WaitTimeSeconds=10,
            )
            messages = response.get("Messages", [])
            if not messages:
                continue

            payloads = []
            receipt_handles = []

            for msg in messages:
                try:
                    payloads.append(json.loads(msg["Body"]))
                    receipt_handles.append(msg["ReceiptHandle"])
                except Exception as e:
                    logger.warning(f"⚠️ Failed to parse SQS message: {e}")

            if payloads:
                callback(payloads)
                for handle in receipt_handles:
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=handle)

        except (BotoCoreError, NoCredentialsError) as e:
            logger.error("❌ SQS error: %s", e)
            time.sleep(5)

    logger.info("🛑 SQS polling stopped.")
