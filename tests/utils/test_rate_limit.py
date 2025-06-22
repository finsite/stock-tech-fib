import time
from app.utils.rate_limit import RateLimiter

def test_rate_limiter_allows():
    limiter = RateLimiter(5, 1)
    for _ in range(5):
        limiter.acquire()
