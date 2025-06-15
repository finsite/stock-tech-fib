"""Thread-safe rate limiter using the token bucket algorithm."""

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
    """Sanitize context string for safe metric labeling.

    Replaces unsafe characters and truncates the string for Prometheus label compatibility.

    Args:
        context (str): Original context string.

    Returns:
        str: Sanitized and truncated context label.
    """
    return re.sub(r"[^\w\-:.]", "_", context)[:64]


def _hash_context(context: str) -> str:
    """Hash the context string to produce a short, opaque identifier for logs.

    Args:
        context (str): The original context string.

    Returns:
        str: SHA-256-based short hash of the context.
    """
    return hashlib.sha256(context.encode()).hexdigest()[:8]


class RateLimiter:
    """Token bucket rate limiter with Prometheus support."""

    def __init__(self, max_requests: int, time_window: float) -> None:
        """Initialize a new RateLimiter instance.

        Args:
            max_requests (int): Maximum number of allowed requests in the time window.
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
        self._lock = threading.Lock()
        self._last_check = time.time()

    def acquire(self, context: str = "RateLimiter") -> None:
        """Acquire a token, blocking if needed to respect rate limits.

        Replenishes tokens based on elapsed time and sleeps if tokens are unavailable.
        Also updates Prometheus metrics and logs token state.

        Args:
            context (str): An identifier for the caller (e.g., service name).

        Returns:
            None
        """
        context = _sanitize_context(context)
        context_id = _hash_context(context)

        with self._lock:
            current_time: float = time.time()
            elapsed: float = current_time - self._last_check

            tokens_to_add: float = elapsed * (self._max_requests / self._time_window)
            self._tokens = min(self._max_requests, self._tokens + tokens_to_add)
            self._last_check = current_time

            rate_limiter_tokens_remaining.labels(context=context).set(self._tokens)

            logger.debug(
                f"[ctx:{context_id}] Replenished {tokens_to_add:.2f} tokens. "
                f"Available: {self._tokens:.2f}"
            )

            if self._tokens < 1:
                sleep_time: float = (1 - self._tokens) * (self._time_window / self._max_requests)
                sleep_time = min(sleep_time, self._time_window)

                logger.info(
                    f"[ctx:{context_id}] Rate limit hit. Sleeping for {sleep_time:.2f} seconds."
                )
                rate_limiter_blocked_total.labels(context=context).inc()
                time.sleep(sleep_time)
                self._tokens = 1

            self._tokens -= 1
            rate_limiter_tokens_remaining.labels(context=context).set(self._tokens)
            logger.debug(f"[ctx:{context_id}] Token consumed. Remaining: {self._tokens:.2f}")
