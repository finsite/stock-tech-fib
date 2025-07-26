# src/app/utils/redactor.py

"""Utility for redacting sensitive fields from dictionaries before logging.

This module is used to ensure that no passwords, tokens, or other secrets
are ever written to logs in clear-text.
"""

from typing import Any

# Fields that should never appear in logs
SENSITIVE_KEYS = {
    "password",
    "secret",
    "token",
    "api_key",
    "authorization",
    "access_token",
}


def redact_dict(obj: Any) -> Any:
    """Recursively redacts sensitive keys in a dictionary.

    Args:
        obj (Any): The input data (typically a dict or list of dicts).

    Returns:
        Any: The redacted version of the input, preserving structure.

    """
    if isinstance(obj, dict):
        return {
            k: "***REDACTED***" if k.lower() in SENSITIVE_KEYS else redact_dict(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [redact_dict(item) for item in obj]
    else:
        return obj
