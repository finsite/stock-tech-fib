"""Initialize the `utils` package for shared application utilities.

Included Utilities:
- setup_logger: Configures logging with structured output.
- retry_request: Retries a function with optional delay on failure.
- request_with_timeout: Makes HTTP GET requests with timeout and validation.
- validate_data: Validates schema and batch structure of data.
- validate_environment_variables: Ensures required environment variables are set.
- track_polling_metrics: Logs success/failure of polling operations.
- track_request_metrics: Logs request-level metrics (rate limits, success, etc.).
"""

from .request_with_timeout import request_with_timeout
from .retry_request import retry_request
from .setup_logger import setup_logger
from .track_polling_metrics import track_polling_metrics
from .track_request_metrics import track_request_metrics
from .validate_data import validate_data
from .validate_environment_variables import validate_environment_variables

__all__ = [
    "setup_logger",
    "retry_request",
    "request_with_timeout",
    "validate_data",
    "validate_environment_variables",
    "track_polling_metrics",
    "track_request_metrics",
]

# Initialize package-level logger for utilities
logger = setup_logger(name="utils")
