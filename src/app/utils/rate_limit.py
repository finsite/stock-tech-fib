"""The module implements a rate limiter for API requests.

The `RateLimiter` class uses the token bucket algorithm to manage the request rate.
It is thread-safe and can be used to limit the request rate for a single API or
multiple APIs.
"""

import threading
import time

from app.utils.setup_logger import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)

# Constants for the rate limiter
# The `RateLimiter` class uses these constants to manage request rates


class RateLimiter:
    """A rate limiter based on the token bucket algorithm.

    Allows a specified number of requests within a time window.

    :param max_requests: Maximum allowed requests in the window.
    :type max_requests: int
    :param time_window: The duration of the window in seconds.
    :type time_window: float

    """

    def __init__(self, max_requests: int, time_window: float) -> None:
        """Initialize the RateLimiter.

        This constructor sets up a token bucket-based rate limiter
        that controls the number of requests allowed within a given
        time window.

        Args:
        ----
            max_requests (int): The maximum number of requests allowed in the time window.
            time_window (float): The duration of the time window in seconds.

        Returns:
        -------
            None

        """
        # Initialize maximum requests and time window
        self._max_requests = max_requests
        self._time_window = time_window

        # Start with a full bucket of tokens
        self._tokens: float = float(max_requests)

        # Lock to ensure thread safety
        self._lock = threading.Lock()

        # Record the last time tokens were checked
        self._last_check = time.time()

    def acquire(self, context: str = "RateLimiter") -> None:
        """Acquire permission to proceed with a request. Blocks if the rate
        limit is exceeded.

        Args:
        ----
            context (str, optional): Optional context for logging (e.g., poller type).
                Defaults to "RateLimiter".

        :param context: str:  (Default value = "RateLimiter")
        :param context: str:  (Default value = "RateLimiter")
        :param context: str:  (Default value = "RateLimiter")
        :param context: Default value = "RateLimiter")
        :type context: str :
        :param context: Default value = "RateLimiter")
        :type context: str :
        :param context: str:  (Default value = "RateLimiter")
        :param context: str:  (Default value = "RateLimiter")
        :param context: str:  (Default value = "RateLimiter")
        :param context: str:  (Default value = "RateLimiter")

        """
        with self._lock:
            current_time: float = time.time()
            elapsed: float = current_time - self._last_check

            # Calculate the number of tokens to add to the bucket
            tokens_to_add: float = elapsed * (self._max_requests / self._time_window)
            self._tokens = min(self._max_requests, self._tokens + tokens_to_add)
            self._last_check = current_time

            # Log the replenished tokens
            logger.debug(
                f"[{context}] Replenished {tokens_to_add:.2f} tokens. "
                f"Available tokens: {self._tokens:.2f}"
            )

            # If the rate limit is reached, wait for some time
            if self._tokens < 1:
                sleep_time: float = (1 - self._tokens) * (self._time_window / self._max_requests)
                logger.info(
                    f"[{context}] Rate limit reached. Sleeping for {sleep_time:.2f} seconds."
                )
                time.sleep(sleep_time)
                self._tokens = 1

            # Consume a token and log the remaining tokens
            self._tokens -= 1
            logger.debug(f"[{context}] Consumed a token. Remaining tokens: {self._tokens:.2f}")
