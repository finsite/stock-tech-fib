"""Thread-safe rate limiter using the token bucket algorithm.

Includes Prometheus metrics and context hashing for structured logs.
"""

import hashlib
import re
import threading
import time

from prometheus_client import Counter, Gauge

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)

# Prometheus metrics
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


def _sanitize_context(context: str) -> str:
    """
    Sanitize a context string for use in Prometheus metric labels.

    Replaces unsafe characters and truncates the string.

    Args:
        context (str): Original context string.

    Returns:
        str: Sanitized context label.
    """
    return re.sub(r"[^\w\-:.]", "_", context)[:64]


def _hash_context(context: str) -> str:
    """
    Hash the context string to produce a short identifier for logs.

    Args:
        context (str): Original context string.

    Returns:
        str: Short SHA-256 hash.
    """
    return hashlib.sha256(context.encode()).hexdigest()[:8]


class RateLimiter:
    """
    Thread-safe token bucket rate limiter with Prometheus integration.

    Allows a maximum number of requests in a defined time window.
    """

    def __init__(self, max_requests: int, time_window: float) -> None:
        """
        Initialize a new RateLimiter instance.

        Args:
            max_requests (int): Maximum number of requests allowed.
            time_window (float): Time window in seconds.

        Raises:
            ValueError: If max_requests or time_window is non-positive.
        """
        if max_requests <= 0:
            raise ValueError("max_requests must be greater than 0")
        if time_window <= 0:
            raise ValueError("time_window must be greater than 0")

        self._max_requests = max_requests
        self._time_window = time_window
        self._tokens: float = float(max_requests)
        self._last_check: float = time.time()
        self._lock = threading.Lock()

    def acquire(self, context: str = "RateLimiter") -> None:
        """
        Acquire a token, blocking if rate limit is exceeded.

        Replenishes tokens based on elapsed time. Updates Prometheus metrics
        and logs token state per context.

        Args:
            context (str): Label for Prometheus/logging context.

        Returns:
            None
        """
        context_label = _sanitize_context(context)
        context_id = _hash_context(context)

        with self._lock:
            current_time = time.time()
            elapsed = current_time - self._last_check
            self._last_check = current_time

            # Replenish tokens based on elapsed time
            refill_rate = self._max_requests / self._time_window
            tokens_to_add = elapsed * refill_rate
            self._tokens = min(self._max_requests, self._tokens + tokens_to_add)

            rate_limiter_tokens_remaining.labels(context=context_label).set(self._tokens)
            logger.debug(
                f"[ctx:{context_id}] Replenished {tokens_to_add:.2f} tokens. "
                f"Available: {self._tokens:.2f}"
            )

            # If no tokens available, sleep and refill one
            if self._tokens < 1:
                sleep_time = (1 - self._tokens) / refill_rate
                sleep_time = min(sleep_time, self._time_window)

                logger.info(
                    f"[ctx:{context_id}] Rate limit hit. Sleeping for {sleep_time:.2f} seconds."
                )
                rate_limiter_blocked_total.labels(context=context_label).inc()
                time.sleep(sleep_time)
                self._tokens = 1.0  # Ensure 1 token is available after sleep

            # Consume a token
            self._tokens -= 1
            rate_limiter_tokens_remaining.labels(context=context_label).set(self._tokens)
            logger.debug(f"[ctx:{context_id}] Token consumed. Remaining: {self._tokens:.2f}")
