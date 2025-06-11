"""Perform a GET request with timeout and JSON validation.

This module provides a function to safely request JSON data from a URL
with a configurable timeout. It handles exceptions, validates the
response content type, and logs errors appropriately.
"""

from typing import Any, cast

import requests

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def request_with_timeout(url: str, timeout: int = 10) -> dict[str, Any] | None:
    """Perform a GET request to the specified URL with a timeout.

    Parameters
    ----------
    url : str
        The URL to request.
    timeout : int, optional
        The timeout in seconds. Defaults to 10.

    Returns
    -------
    dict[str, Any] | None
        Parsed JSON response if valid and successful, otherwise None.

    Raises
    ------
    ValueError
        If the URL is empty.

    """
    if not url:
        logger.error("URL cannot be empty.")
        return None

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type")
        if content_type is None or "application/json" not in content_type:
            logger.error(f"Expected JSON response from {url}, but got {content_type}.")
            return None

        json_response = cast(dict[str, Any], response.json())
        if json_response is None:
            logger.error("Received empty JSON response.")
            return None

        return json_response

    except requests.exceptions.Timeout:
        logger.error(f"Timeout occurred while requesting {url}.")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred while requesting {url}: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception occurred: {e}")
    except ValueError as e:
        logger.error(f"Error decoding JSON response from {url}: {e}")

    return None
