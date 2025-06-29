"""Configuration utility functions for environment variable retrieval.

Provides memoized access to string and boolean configuration values,
with safe fallbacks and support for caching via functools.lru_cache.
"""

import os
from functools import lru_cache


@lru_cache
def get_config_value(key: str, default: str = "") -> str:
    """Retrieve a configuration value from the environment.

    Args:
        key (str): The name of the environment variable.
        default (str): The fallback value if the environment variable is not set.

    Returns:
        str: The value of the environment variable or the default.

    """
    return os.getenv(key, default)


@lru_cache
def get_config_bool(key: str, default: bool = False) -> bool:
    """Retrieve a boolean configuration value from the environment.

    Args:
        key (str): The name of the environment variable.
        default (bool): The fallback value if the environment variable is not set.

    Returns:
        bool: The parsed boolean value.

    """
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")
