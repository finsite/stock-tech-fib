"""Shared Prometheus metric definitions for all pollers and processors.

Exports counters and histograms for:
- Polling operations
- HTTP requests
- Output handling
- Message processing
- Paper trading
- Rate limiting
- Optional sinks: REST, S3, database
"""

import re

from prometheus_client import REGISTRY, Counter, Gauge, Histogram, generate_latest


def get_prometheus_metrics() -> str:
    """Return all registered Prometheus metrics as a text payload."""
    return generate_latest(REGISTRY).decode("utf-8")


def _sanitize_label(value: str) -> str:
    """Sanitize a string to be Prometheus-compatible label.

    Args:
        value (str): The input string to sanitize.

    Returns:
        str: Sanitized label safe for Prometheus use.

    """
    return re.sub(r"[^\w\-:.]", "_", value)[:64]


# -----------------------------
# Output Metrics
# -----------------------------
output_counter = Counter(
    "output_messages_total",
    "Total number of messages successfully sent to each output mode.",
    ["mode"],
)

output_failures = Counter(
    "output_failures_total",
    "Total number of output failures by mode.",
    ["mode"],
)

output_duration = Histogram(
    "output_duration_seconds",
    "Time taken to send output messages by mode.",
    ["mode"],
    buckets=[0.01, 0.1, 0.5, 1, 2, 5],
)


def record_output_metrics(mode: str, success: bool, duration_sec: float) -> None:
    mode = _sanitize_label(mode)
    if success:
        output_counter.labels(mode=mode).inc()
    else:
        output_failures.labels(mode=mode).inc()
    output_duration.labels(mode=mode).observe(duration_sec)


# -----------------------------
# Polling Metrics
# -----------------------------
poll_counter = Counter(
    "poll_cycles_total",
    "Total number of polling cycles by poller.",
    ["poller"],
)

poll_errors = Counter(
    "poll_errors_total",
    "Total number of poller errors by poller.",
    ["poller"],
)

poll_duration = Histogram(
    "poll_duration_seconds",
    "Duration of polling cycles by poller.",
    ["poller"],
    buckets=[0.01, 0.1, 0.5, 1, 2, 5, 10],
)


def record_poll_metrics(poller: str, error: bool, duration_sec: float) -> None:
    poller = _sanitize_label(poller)
    poll_counter.labels(poller=poller).inc()
    if error:
        poll_errors.labels(poller=poller).inc()
    poll_duration.labels(poller=poller).observe(duration_sec)


# -----------------------------
# HTTP Request Metrics
# -----------------------------
http_request_counter = Counter(
    "http_requests_total",
    "Total number of HTTP requests by service and method.",
    ["service", "method", "status"],
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "Duration of HTTP requests by service and method.",
    ["service", "method"],
    buckets=[0.01, 0.1, 0.5, 1, 2, 5],
)


def record_http_metrics(service: str, method: str, status: str, duration_sec: float) -> None:
    service = _sanitize_label(service)
    method = _sanitize_label(method)
    status = _sanitize_label(status)
    http_request_counter.labels(service=service, method=method, status=status).inc()
    http_request_duration.labels(service=service, method=method).observe(duration_sec)


# -----------------------------
# Message Processing Metrics
# -----------------------------
process_success = Counter(
    "message_processing_success_total",
    "Number of messages processed successfully.",
    ["processor"],
)

process_failure = Counter(
    "message_processing_failure_total",
    "Number of failed message processing attempts.",
    ["processor"],
)

process_duration = Histogram(
    "message_processing_duration_seconds",
    "Time taken to process messages.",
    ["processor"],
    buckets=[0.001, 0.01, 0.1, 0.5, 1, 5],
)

validation_failures = Counter(
    "message_validation_failures_total",
    "Number of failed message validation attempts.",
    ["processor"],
)

validation_duration = Histogram(
    "message_validation_duration_seconds",
    "Duration of validation checks per message.",
    ["processor"],
    buckets=[0.001, 0.01, 0.1, 0.5],
)


def record_processing_metrics(processor: str, success: bool, duration_sec: float) -> None:
    processor = _sanitize_label(processor)
    if success:
        process_success.labels(processor=processor).inc()
    else:
        process_failure.labels(processor=processor).inc()
    process_duration.labels(processor=processor).observe(duration_sec)


def record_validation_metrics(processor: str, duration_sec: float, failed: bool = False) -> None:
    processor = _sanitize_label(processor)
    if failed:
        validation_failures.labels(processor=processor).inc()
    validation_duration.labels(processor=processor).observe(duration_sec)


# -----------------------------
# Paper Trading Metrics
# -----------------------------
paper_trade_counter = Counter(
    "paper_trades_total",
    "Number of simulated paper trades executed.",
    ["destination"],
)

paper_trade_failures = Counter(
    "paper_trade_failures_total",
    "Number of failed paper trade dispatches.",
    ["destination"],
)

paper_trade_duration = Histogram(
    "paper_trade_duration_seconds",
    "Time taken to dispatch paper trade messages.",
    ["destination"],
    buckets=[0.01, 0.1, 0.5, 1, 2, 5],
)


def record_paper_trade_metrics(destination: str, success: bool, duration_sec: float) -> None:
    destination = _sanitize_label(destination)
    if success:
        paper_trade_counter.labels(destination=destination).inc()
    else:
        paper_trade_failures.labels(destination=destination).inc()
    paper_trade_duration.labels(destination=destination).observe(duration_sec)


# -----------------------------
# Rate Limiting Metrics
# -----------------------------
rate_limiter_blocked_total = Counter(
    "rate_limiter_blocked_total",
    "Total number of times the rate limiter blocked",
    ["context"],
)

rate_limiter_tokens_remaining = Gauge(
    "rate_limiter_tokens_remaining",
    "Current number of available tokens in the rate limiter",
    ["context"],
)


def record_rate_limit_metrics(context: str, blocked: bool, tokens_remaining: float) -> None:
    context = _sanitize_label(context)
    if blocked:
        rate_limiter_blocked_total.labels(context=context).inc()
    rate_limiter_tokens_remaining.labels(context=context).set(tokens_remaining)


# -----------------------------
# Optional Sink Metrics
# -----------------------------
rest_dispatch_counter = Counter(
    "rest_dispatch_total",
    "Total number of REST output dispatch attempts.",
    ["status"],
)

s3_dispatch_counter = Counter(
    "s3_dispatch_total",
    "Total number of S3 output dispatch attempts.",
    ["status"],
)

db_dispatch_counter = Counter(
    "database_dispatch_total",
    "Total number of database output dispatch attempts.",
    ["status"],
)

rest_dispatch_failures = Counter(
    "rest_dispatch_failures_total",
    "Number of failed REST output dispatch attempts.",
    ["status"],
)

s3_dispatch_failures = Counter(
    "s3_dispatch_failures_total",
    "Number of failed S3 output dispatch attempts.",
    ["status"],
)

db_dispatch_failures = Counter(
    "database_dispatch_failures_total",
    "Number of failed database output dispatch attempts.",
    ["status"],
)

rest_dispatch_duration = Histogram(
    "rest_dispatch_duration_seconds",
    "Time taken to dispatch data to REST endpoint.",
    ["status"],
    buckets=[0.01, 0.1, 0.5, 1, 2, 5],
)

s3_dispatch_duration = Histogram(
    "s3_dispatch_duration_seconds",
    "Time taken to dispatch data to S3.",
    ["status"],
    buckets=[0.01, 0.1, 0.5, 1, 2, 5],
)

db_dispatch_duration = Histogram(
    "database_dispatch_duration_seconds",
    "Time taken to dispatch data to database.",
    ["status"],
    buckets=[0.01, 0.1, 0.5, 1, 2, 5],
)


def record_sink_metrics(sink: str, status: str, duration_sec: float, failed: bool = False) -> None:
    status = _sanitize_label(status)
    if sink == "rest":
        rest_dispatch_counter.labels(status=status).inc()
        rest_dispatch_duration.labels(status=status).observe(duration_sec)
        if failed:
            rest_dispatch_failures.labels(status=status).inc()
    elif sink == "s3":
        s3_dispatch_counter.labels(status=status).inc()
        s3_dispatch_duration.labels(status=status).observe(duration_sec)
        if failed:
            s3_dispatch_failures.labels(status=status).inc()
    elif sink == "db":
        db_dispatch_counter.labels(status=status).inc()
        db_dispatch_duration.labels(status=status).observe(duration_sec)
        if failed:
            db_dispatch_failures.labels(status=status).inc()


# -----------------------------
# Queue Publishing Metrics
# -----------------------------
queue_publish_counter = Counter(
    "queue_publish_total",
    "Total number of messages published to queues by type and status.",
    ["queue_type", "status"],
)

queue_publish_latency = Histogram(
    "queue_publish_duration_seconds",
    "Time taken to publish messages to queues.",
    ["queue_type", "status"],
    buckets=[0.01, 0.1, 0.5, 1, 2, 5],
)


def record_queue_metrics(queue_type: str, status: str, duration_sec: float) -> None:
    """Record metrics for queue publishing operations.

    Args:
        queue_type (str): Type of the queue system (e.g., "rabbitmq", "sqs").
        status (str): Publishing status (e.g., "success", "failure", "exception").
        duration_sec (float): Time taken to publish the message.

    """
    queue_type = _sanitize_label(queue_type)
    status = _sanitize_label(status)
    queue_publish_counter.labels(queue_type=queue_type, status=status).inc()
    queue_publish_latency.labels(queue_type=queue_type, status=status).observe(duration_sec)
