"""Thread-safe rate limiter using the token bucket algorithm."""

import threading
import time
import re

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
    """Sanitize context string for safe logging."""
    return re.sub(r"[^\w\-:.]", "_", context)[:64]


class RateLimiter:
    """Token bucket rate limiter with Prometheus support."""

    def __init__(self, max_requests: int, time_window: float) -> None:
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
        context = _sanitize_context(context)

        with self._lock:
            current_time: float = time.time()
            elapsed: float = current_time - self._last_check

            tokens_to_add: float = elapsed * (self._max_requests / self._time_window)
            self._tokens = min(self._max_requests, self._tokens + tokens_to_add)
            self._last_check = current_time

            rate_limiter_tokens_remaining.labels(context=context).set(self._tokens)

            logger.debug(
                f"[{context}] Replenished {tokens_to_add:.2f} tokens. "
                f"Available tokens: {self._tokens:.2f}"
            )

            if self._tokens < 1:
                sleep_time: float = (1 - self._tokens) * (self._time_window / self._max_requests)
                sleep_time = min(sleep_time, self._time_window)

                logger.info(
                    f"[{context}] Rate limit reached. Sleeping for {sleep_time:.2f} seconds."
                )
                rate_limiter_blocked_total.labels(context=context).inc()
                time.sleep(sleep_time)
                self._tokens = 1

            self._tokens -= 1
            rate_limiter_tokens_remaining.labels(context=context).set(self._tokens)
            logger.debug(f"[{context}] Consumed a token. Remaining: {self._tokens:.2f}")
