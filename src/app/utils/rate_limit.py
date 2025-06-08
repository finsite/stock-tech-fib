"""The module implements a rate limiter for API requests.

The `RateLimiter` class uses the token bucket algorithm to manage the request rate.
It is thread-safe and can be used to limit the request rate for a single API or
multiple APIs.
"""

import threading
import time

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


class RateLimiter:
    """A rate limiter based on the token bucket algorithm.

    Allows a specified number of requests within a time window.

    Parameters
    ----------
    max_requests : int
        Maximum allowed requests in the time window.
    time_window : float
        Duration of the window in seconds.

    """

    def __init__(self, max_requests: int, time_window: float) -> None:
        """Initialize the RateLimiter.

        This sets up a token bucket to control the number of allowed requests.

        Parameters
        ----------
        max_requests : int
            Maximum number of requests allowed in the time window.
        time_window : float
            Duration of the time window in seconds.

        """
        self._max_requests = max_requests
        self._time_window = time_window
        self._tokens: float = float(max_requests)
        self._lock = threading.Lock()
        self._last_check = time.time()

    def acquire(self, context: str = "RateLimiter") -> None:
        """Acquire permission to proceed with a request.

        Blocks the caller if the rate limit is exceeded until a token is available.

        Parameters
        ----------
        context : str, optional
            Optional context for logging (e.g., poller type). Defaults to "RateLimiter".

        """
        with self._lock:
            current_time: float = time.time()
            elapsed: float = current_time - self._last_check

            tokens_to_add: float = elapsed * (self._max_requests / self._time_window)
            self._tokens = min(self._max_requests, self._tokens + tokens_to_add)
            self._last_check = current_time

            logger.debug(
                f"[{context}] Replenished {tokens_to_add:.2f} tokens. "
                f"Available tokens: {self._tokens:.2f}"
            )

            if self._tokens < 1:
                sleep_time: float = (1 - self._tokens) * (self._time_window / self._max_requests)
                logger.info(
                    f"[{context}] Rate limit reached. Sleeping for {sleep_time:.2f} seconds."
                )
                time.sleep(sleep_time)
                self._tokens = 1

            self._tokens -= 1
            logger.debug(f"[{context}] Consumed a token. Remaining tokens: {self._tokens:.2f}")
