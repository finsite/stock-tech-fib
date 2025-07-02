"""Module to handle output of analysis results to the configured target.

Supports logging, stdout, queue publishing, REST, S3, and database sinks.
Includes retry logic, validation, and optional metrics integration.
"""

import json
import time
import uuid
from collections.abc import Callable
from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential

from app import config_shared
from app.queue_sender import publish_to_queue
from app.utils.metrics import (
    record_output_metrics,
    record_paper_trade_metrics,
    record_sink_metrics,
)
from app.utils.setup_logger import setup_logger
from app.utils.types import OutputMode, validate_list_of_dicts

logger = setup_logger(__name__)


class OutputDispatcher:
    """Handles routing analysis output to different destinations (e.g., queue, REST, S3, DB)."""

    def __init__(self) -> None:
        """Initialize dispatcher with configured output modes."""
        self.output_modes = config_shared.get_output_modes()

    def send(self, data: list[dict[str, Any]]) -> None:
        """Dispatch processed analysis output to one or more configured destinations.

        Args:
            data (list[dict[str, Any]]): List of data payloads to send.

        """
        try:
            validate_list_of_dicts(data, required_keys=["text"])

            if config_shared.get_paper_trading_enabled():
                paper_mode = config_shared.get_paper_trade_mode()
                logger.debug("📄 Paper trading enabled — dispatching to %s mode", paper_mode)
                dispatch_method = self._get_dispatch_method(OutputMode(paper_mode))
                if dispatch_method:
                    dispatch_method(data)
                else:
                    logger.warning("⚠️ Invalid paper trading output mode: %s", paper_mode)
                return

            for mode in self.output_modes:
                dispatch_method = self._get_dispatch_method(mode)
                if dispatch_method:
                    dispatch_method(data)
                else:
                    logger.warning("⚠️ Unhandled output mode: %s", mode)

        except Exception as e:
            logger.error("❌ Failed to send output: %s", e)

    def send_trade_simulation(self, data: dict[str, Any]) -> None:
        """Send simulated trade data to the appropriate paper trade destination.

        Args:
            data (dict[str, Any]): Simulated trade payload.

        """
        try:
            if config_shared.get_paper_trading_database_enabled():
                self._output_paper_trade_to_database(data)
            else:
                self._output_paper_trade_to_queue(data)
        except Exception as e:
            logger.error("❌ Failed to send paper trade: %s", e)
            record_paper_trade_metrics("queue", success=False, duration_sec=0)

    def _get_dispatch_method(
        self, mode: OutputMode
    ) -> Callable[[list[dict[str, Any]]], None] | None:
        """Resolve the output dispatch method based on the mode.

        Args:
            mode (OutputMode): Output mode enum value.

        Returns:
            Callable or None: Method to handle the output.

        """
        return {
            OutputMode.LOG: self._output_to_log,
            OutputMode.STDOUT: self._output_to_stdout,
            OutputMode.QUEUE: self._output_to_queue,
            OutputMode.REST: self._output_to_rest,
            OutputMode.S3: self._output_to_s3,
            OutputMode.DATABASE: self._output_to_database,
        }.get(mode)

    def _output_to_log(self, data: list[dict[str, Any]]) -> None:
        """Log each item in the data list.

        Args:
            data (list[dict[str, Any]]): Data to log.

        """
        for item in data:
            logger.info("📝 Processed message:\n%s", json.dumps(item, indent=4))

    def _output_to_stdout(self, data: list[dict[str, Any]]) -> None:
        """Print each item in the data list to standard output.

        Args:
            data (list[dict[str, Any]]): Data to print.

        """
        for item in data:
            print(json.dumps(item, indent=4))

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def _output_to_queue(self, data: list[dict[str, Any]]) -> None:
        """Publish the data to the configured queue.

        Retries on failure using exponential backoff.

        Args:
            data (list[dict[str, Any]]): Data to publish.

        """
        publish_to_queue(data)
        logger.info("✅ Output published to queue: %d message(s)", len(data))
        record_output_metrics("queue", success=True, duration_sec=0)

    def _output_to_rest(self, data: list[dict[str, Any]]) -> None:
        """Send the data to the configured REST endpoint.

        Args:
            data (list[dict[str, Any]]): Data to post to REST API.

        """
        import requests

        url = config_shared.get_rest_output_url()
        headers = {"Content-Type": "application/json"}
        start = time.perf_counter()
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            duration = time.perf_counter() - start
            record_sink_metrics("rest", str(response.status_code), duration, failed=not response.ok)

            if response.ok:
                logger.info("🚀 Sent data to REST: HTTP %d", response.status_code)
            else:
                logger.error("❌ REST output failed: HTTP %d", response.status_code)
        except Exception as e:
            logger.error("❌ REST output error: %s", e)
            record_sink_metrics("rest", "exception", 0, failed=True)

    def _output_to_s3(self, data: list[dict[str, Any]]) -> None:
        """Upload the data as a JSON file to an S3 bucket.

        Args:
            data (list[dict[str, Any]]): Data to upload.

        """
        import boto3

        s3 = boto3.client("s3")
        bucket = config_shared.get_s3_output_bucket()
        key = f"outputs/{uuid.uuid4()}.json"
        start = time.perf_counter()
        try:
            s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data).encode("utf-8"))
            duration = time.perf_counter() - start
            record_sink_metrics("s3", "200", duration, failed=False)
            logger.info("🚚 Uploaded output to S3: %s/%s", bucket, key)
        except Exception as e:
            logger.error("❌ S3 upload failed: %s", e)
            record_sink_metrics("s3", "exception", 0, failed=True)

    def _output_to_database(self, data: list[dict[str, Any]]) -> None:
        """Write the data to the configured database using raw SQL inserts.

        Args:
            data (list[dict[str, Any]]): Data records to insert.

        """
        import sqlalchemy

        engine = sqlalchemy.create_engine(config_shared.get_database_output_url())
        start = time.perf_counter()
        try:
            with engine.begin() as conn:
                for item in data:
                    if not isinstance(item, dict):
                        logger.warning("⚠️ Invalid item in database batch: %s", item)
                        continue
                    conn.execute(sqlalchemy.text(config_shared.get_database_insert_sql()), **item)
            duration = time.perf_counter() - start
            record_sink_metrics("db", "success", duration, failed=False)
            logger.info("📊 Wrote %d records to database", len(data))
        except Exception as e:
            logger.error("❌ Database output failed: %s", e)
            record_sink_metrics("db", "exception", 0, failed=True)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def _output_paper_trade_to_queue(self, data: dict[str, Any]) -> None:
        """Send paper trade data to a paper trading queue.

        Args:
            data (dict[str, Any]): Simulated trade to queue.

        """
        queue_name = config_shared.get_paper_trading_queue_name()
        exchange = config_shared.get_paper_trading_exchange()
        publish_to_queue([data], queue=queue_name, exchange=exchange)
        logger.info("🪙 Paper trade sent to queue:\n%s", json.dumps(data, indent=4))
        record_paper_trade_metrics("queue", success=True, duration_sec=0)

    def _output_paper_trade_to_database(self, data: dict[str, Any]) -> None:
        """Placeholder for future paper trade DB integration.

        Args:
            data (dict[str, Any]): Simulated trade record.

        """
        logger.warning("⚠️ Paper trading database integration not implemented.")
        logger.info("📊 Skipped paper trade (DB output not implemented).")


output_handler = OutputDispatcher()


def send_to_output(data: list[dict[str, Any]]) -> None:
    """Send data using the default output handler instance.

    Args:
        data (list[dict[str, Any]]): List of messages to dispatch.

    """
    output_handler.send(data)


__all__ = ["send_to_output", "output_handler"]
