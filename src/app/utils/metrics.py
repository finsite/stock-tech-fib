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


# Output Metrics
output_counter: Counter = Counter(
    "output_messages_total",
    "Total number of messages successfully sent to each output mode.",
    ["mode"],
)

output_failures: Counter = Counter(
    "output_failures_total",
    "Total number of output failures by mode.",
    ["mode"],
)

output_duration: Histogram = Histogram(
    "output_duration_seconds",
    "Time taken to send output messages by mode.",
    ["mode"],
)

# Polling Metrics
poll_counter: Counter = Counter(
    "poll_cycles_total",
    "Total number of polling cycles by poller.",
    ["poller"],
)

poll_errors: Counter = Counter(
    "poll_errors_total",
    "Total number of poller errors by poller.",
    ["poller"],
)

poll_duration: Histogram = Histogram(
    "poll_duration_seconds",
    "Duration of polling cycles by poller.",
    ["poller"],
)

# HTTP Request Metrics
http_request_counter: Counter = Counter(
    "http_requests_total",
    "Total number of HTTP requests by service and method.",
    ["service", "method", "status"],
)

http_request_duration: Histogram = Histogram(
    "http_request_duration_seconds",
    "Duration of HTTP requests by service and method.",
    ["service", "method"],
)

# Message Processing Metrics
process_success: Counter = Counter(
    "message_processing_success_total",
    "Number of messages processed successfully.",
    ["processor"],
)

process_failure: Counter = Counter(
    "message_processing_failure_total",
    "Number of failed message processing attempts.",
    ["processor"],
)

process_duration: Histogram = Histogram(
    "message_processing_duration_seconds",
    "Time taken to process messages.",
    ["processor"],
)

# Validation Failures
validation_failures: Counter = Counter(
    "message_validation_failures_total",
    "Number of failed message validation attempts.",
    ["processor"],
)

validation_duration: Histogram = Histogram(
    "message_validation_duration_seconds",
    "Duration of validation checks per message.",
    ["processor"],
)

# Paper Trading Metrics
paper_trade_counter: Counter = Counter(
    "paper_trades_total",
    "Number of simulated paper trades executed.",
    ["destination"],
)

paper_trade_failures: Counter = Counter(
    "paper_trade_failures_total",
    "Number of failed paper trade dispatches.",
    ["destination"],
)

paper_trade_duration: Histogram = Histogram(
    "paper_trade_duration_seconds",
    "Time taken to dispatch paper trade messages.",
    ["destination"],
)

# Rate Limiting Metrics
rate_limiter_blocked_total: Counter = Counter(
    "rate_limiter_blocked_total",
    "Total number of times the rate limiter blocked",
    ["context"],
)

rate_limiter_tokens_remaining: Gauge = Gauge(
    "rate_limiter_tokens_remaining",
    "Current number of available tokens in the rate limiter",
    ["context"],
)

# Optional Sink Metrics
rest_dispatch_counter: Counter = Counter(
    "rest_dispatch_total",
    "Total number of REST output dispatch attempts.",
    ["status"],
)

s3_dispatch_counter: Counter = Counter(
    "s3_dispatch_total",
    "Total number of S3 output dispatch attempts.",
    ["status"],
)

db_dispatch_counter: Counter = Counter(
    "database_dispatch_total",
    "Total number of database output dispatch attempts.",
    ["status"],
)

rest_dispatch_duration: Histogram = Histogram(
    "rest_dispatch_duration_seconds",
    "Time taken to dispatch data to REST endpoint.",
    ["status"],
)

s3_dispatch_duration: Histogram = Histogram(
    "s3_dispatch_duration_seconds",
    "Time taken to dispatch data to S3.",
    ["status"],
)

db_dispatch_duration: Histogram = Histogram(
    "database_dispatch_duration_seconds",
    "Time taken to dispatch data to database.",
    ["status"],
)

rest_dispatch_failures: Counter = Counter(
    "rest_dispatch_failures_total",
    "Number of failed REST output dispatch attempts.",
    ["status"],
)

s3_dispatch_failures: Counter = Counter(
    "s3_dispatch_failures_total",
    "Number of failed S3 output dispatch attempts.",
    ["status"],
)

db_dispatch_failures: Counter = Counter(
    "database_dispatch_failures_total",
    "Number of failed database output dispatch attempts.",
    ["status"],
)
