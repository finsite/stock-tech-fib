"""Module to publish processed analysis data to RabbitMQ or AWS SQS."""

import json

import boto3
import pika
from botocore.exceptions import BotoCoreError, NoCredentialsError

from app import config
from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def publish_to_queue(payload: list[dict]) -> None:
    """Publishes processed candlestick analysis results to RabbitMQ or SQS.

    Parameters
    ----------
    payload : list[dict]
        A list of message payloads to publish.
    payload :
        list[dict]:
    payload :
        list[dict]:
    payload :
        list[dict]:
    payload : list[dict] :

    payload: list[dict] :


    Returns
    -------


    """
    queue_type = config.get_queue_type()

    for message in payload:
        if queue_type == "rabbitmq":
            _send_to_rabbitmq(message)
        elif queue_type == "sqs":
            _send_to_sqs(message)
        else:
            logger.error("Invalid QUEUE_TYPE specified: %s", queue_type)


def _send_to_rabbitmq(data: dict) -> None:
    """Sends a single message to RabbitMQ using config-based credentials.

    Parameters
    ----------
    data : dict
        The message payload to send.
    data :
        dict:
    data :
        dict:
    data :
        dict:
    data : dict :

    data: dict :


    Returns
    -------


    """
    try:
        credentials = pika.PlainCredentials(
            config.get_rabbitmq_user(), config.get_rabbitmq_password()
        )
        parameters = pika.ConnectionParameters(
            host=config.get_rabbitmq_host(),
            port=config.get_rabbitmq_port(),
            virtual_host=config.get_rabbitmq_vhost(),
            credentials=credentials,
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.basic_publish(
            exchange=config.get_rabbitmq_exchange(),
            routing_key=config.get_rabbitmq_routing_key(),
            body=json.dumps(data),
        )
        channel.close()
        connection.close()
        logger.info("✅ Published message to RabbitMQ")
    except Exception as e:
        logger.error("❌ Failed to publish message to RabbitMQ: %s", e)


def _send_to_sqs(data: dict) -> None:
    """Sends a single message to AWS SQS using the configured queue.

    Parameters
    ----------
    data : dict
        The message payload to send.
    data :
        dict:
    data :
        dict:
    data :
        dict:
    data : dict :

    data: dict :


    Returns
    -------


    """
    sqs_url = config.get_sqs_queue_url()
    region = config.get_sqs_region()

    try:
        sqs_client = boto3.client("sqs", region_name=region)
        response = sqs_client.send_message(
            QueueUrl=sqs_url,
            MessageBody=json.dumps(data),
        )
        logger.info("✅ Published message to SQS, MessageId: %s", response["MessageId"])
    except (BotoCoreError, NoCredentialsError) as e:
        logger.error("❌ Failed to initialize SQS client: %s", e)
    except Exception as e:
        logger.error("❌ Failed to publish message to SQS: %s", e)
