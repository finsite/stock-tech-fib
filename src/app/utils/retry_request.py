"""Retry a function if it raises an exception.

The `retry_request` function retries a given function if it raises an exception.
It waits for a specified delay in seconds between retries and attempts up to
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
    """Retry a function if it raises an exception.

    This function retries a callable up to a specified number of times, with a delay
    between attempts. If all attempts fail, the last exception is raised.

    Parameters
    ----------
    func : Callable[[], Any]
        The function to be retried.
    max_retries : int, optional
        The maximum number of retry attempts (default is 3).
    delay_seconds : int, optional
        Delay in seconds between retries (default is 5).

    Returns
    -------
    Any | None
        The return value of the function if successful, or raises the last exception.

    Raises
    ------
    ValueError
        If the function passed is None.
    Exception
        If all retry attempts fail, the last exception is re-raised.

    """
    if func is None:
        raise ValueError("The function to be retried cannot be None")

    last_exception = None

    for attempt in range(1, max_retries + 1):
        try:
            logger.debug(f"Attempt {attempt} of {max_retries}.")
            return func()
        except Exception as exception:
            last_exception = exception
            logger.warning(
                f"Attempt {attempt} failed with error: {exception}. "
                f"{'Retrying...' if attempt < max_retries else 'No more retries.'}"
            )
            if attempt < max_retries:
                time.sleep(delay_seconds)

    logger.error(f"All {max_retries} attempts failed. Last error: {last_exception}")
    raise (
        last_exception
        if last_exception
        else RuntimeError("All retries failed but no exception was captured.")
    )
