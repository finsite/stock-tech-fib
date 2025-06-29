"""Generic retry mechanism for transient operations.

Retries a function call on failure with configurable retry count and delay.
"""

import time
from collections.abc import Callable
from typing import Any

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def retry_request(func: Callable[[], Any], *, max_retries: int = 3, delay_seconds: int = 5) -> Any:
    """Retry a function if it raises an exception.

    Retries a callable up to `max_retries` times, sleeping `delay_seconds`
    between attempts. Raises the last encountered exception if all retries fail.

    Args:
        func (Callable[[], Any]): The function to retry.
        max_retries (int, optional): Maximum number of attempts (default is 3).
        delay_seconds (int, optional): Seconds to wait between retries (default is 5).

    Returns:
        Any: The return value of the callable if successful.

    Raises:
        ValueError: If `func` is None.
        Exception: The last raised exception from the callable.

    """
    if func is None:
        raise ValueError("The function to be retried cannot be None.")

    last_exception: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            logger.debug(f"🔁 Attempt {attempt} of {max_retries}")
            return func()
        except Exception as exc:
            last_exception = exc
            logger.warning(
                f"⚠️ Attempt {attempt} failed: {exc}. "
                f"{'Retrying...' if attempt < max_retries else 'No more retries.'}"
            )
            if attempt < max_retries:
                time.sleep(delay_seconds)

    logger.error(f"❌ All {max_retries} attempts failed. Last error: {last_exception}")
    raise last_exception or RuntimeError("All retries failed but no exception was captured.")
