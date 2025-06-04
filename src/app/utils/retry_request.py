"""The module provides a decorator for retrying a function if it raises an
exception.

The decorator `retry_request` retries a given function if it raises an exception.
It waits for a specified delay in seconds between retries, and attempts up to
a maximum number of times. If the function still raises an exception after the
maximum number of retries, it raises that exception.
"""

import time
from collections.abc import Callable
from typing import Any

from app.utils.setup_logger import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)


def retry_request(
    func: Callable[[], Any], *, max_retries: int = 3, delay_seconds: int = 5
) -> Any | None:
    """Retries a given function if it raises an exception.
    
    The function is retried up to a maximum number of times. Between each retry,
    the function waits for a specified delay in seconds. If the function still
    raises an exception after the maximum number of retries, it raises that
    exception.

    :param func: The function to be retried.
    :param max_retries: The maximum number of retry attempts. Defaults to 3.
    :param delay_seconds: The delay in seconds between retries. Defaults to 5.
    :param func: Callable[[]:
    :param Any: param *:
    :param max_retries: int:  (Default value = 3)
    :param delay_seconds: int:  (Default value = 5)
    :param func: Callable[[]:
    :param Any: param *:
    :param max_retries: int:  (Default value = 3)
    :param delay_seconds: int:  (Default value = 5)
    :param func: Callable[[]: 
    :param Any]: 
    :param *: 
    :param max_retries: int:  (Default value = 3)
    :param delay_seconds: int:  (Default value = 5)
    :returns: The result of the function if successful, or None if all retries fail.
    :raises ValueError: If the function to be retried is None.
    :raises Exception: The last exception encountered if all retries fail.

    """
    # Validate the function to be retried
    if func is None:
        raise ValueError("The function to be retried cannot be None")

    last_exception = None  # To store the last exception encountered

    # Attempt to execute the function up to max_retries times
    for attempt in range(1, max_retries + 1):
        try:
            # Call the function and return its result if successful
            logger.debug(f"Attempt {attempt} of {max_retries}.")
            return func()
        except Exception as exception:
            last_exception = exception  # Store the exception
            logger.warning(
                f"Attempt {attempt} failed with error: {exception}. "
                f"{'Retrying...' if attempt < max_retries else 'No more retries.'}"
            )
            # Delay before retrying, if more retries are available
            if attempt < max_retries:
                time.sleep(delay_seconds)

    # Log the final failure and raise the last exception encountered
    logger.error(f"All {max_retries} attempts failed. Last error: {last_exception}")
    if last_exception is not None:
        raise last_exception
    raise RuntimeError("All retries failed but no exception was captured.")
