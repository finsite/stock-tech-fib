"""Shared Prometheus metric definitions for all pollers and processors.

Exports counters and histograms for:
- Polling operations
- HTTP requests
- Output handling
- Message processing
"""

from prometheus_client import Counter, Histogram

# Output Metrics
output_counter = Counter(
    "output_messages_total",
    "Total number of messages successfully sent to each output mode.",
    ["mode"],
)

output_failures = Counter(
    "output_failures_total", "Total number of output failures by mode.", ["mode"]
)

output_duration = Histogram(
    "output_duration_seconds", "Time taken to send output messages by mode.", ["mode"]
)

# Polling Metrics
poll_counter = Counter("poll_cycles_total", "Total number of polling cycles by poller.", ["poller"])

poll_errors = Counter("poll_errors_total", "Total number of poller errors by poller.", ["poller"])

poll_duration = Histogram(
    "poll_duration_seconds", "Duration of polling cycles by poller.", ["poller"]
)

# HTTP Request Metrics
http_request_counter = Counter(
    "http_requests_total",
    "Total number of HTTP requests by service and method.",
    ["service", "method", "status"],
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "Duration of HTTP requests by service and method.",
    ["service", "method"],
)

# Message Processing Metrics
process_success = Counter(
    "message_processing_success_total", "Number of messages processed successfully.", ["processor"]
)

process_failure = Counter(
    "message_processing_failure_total",
    "Number of failed message processing attempts.",
    ["processor"],
)

process_duration = Histogram(
    "message_processing_duration_seconds", "Time taken to process messages.", ["processor"]
)

# Validation Failures
validation_failures = Counter(
    "message_validation_failures_total",
    "Number of failed message validation attempts.",
    ["processor"],
)

validation_duration = Histogram(
    "message_validation_duration_seconds",
    "Duration of validation checks per message.",
    ["processor"],
)
