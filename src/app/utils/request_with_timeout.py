"""Perform a GET request with timeout and JSON validation.

Safely requests JSON data from a URL with a configurable timeout.
Handles timeouts, HTTP errors, invalid responses, and logs failures.
"""

from typing import Any

import requests

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def request_with_timeout(url: str, timeout: int = 10) -> dict[str, Any] | None:
    """Perform a GET request to the specified URL with a timeout.

    Args:
        url (str): The URL to request.
        timeout (int, optional): Timeout in seconds (default is 10).

    Returns:
        dict[str, Any] | None: Parsed JSON response if successful, else None.

    Raises:
        ValueError: If the URL is empty.

    """
    if not url:
        logger.error("❌ URL cannot be empty.")
        return None

    try:
        logger.debug(f"🔗 Sending GET request to {url} with timeout={timeout}")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            logger.error(f"⚠️ Expected JSON response but got '{content_type}' from {url}")
            return None

        json_response = response.json()
        if not isinstance(json_response, dict):
            logger.error(f"⚠️ Invalid JSON object received from {url}")
            return None

        return json_response

    except requests.exceptions.Timeout:
        logger.error(f"⏱️ Timeout while requesting {url}")
    except requests.exceptions.HTTPError as e:
        logger.error(f"❌ HTTP error for {url}: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"⚠️ Request failed for {url}: {e}")
    except ValueError as e:
        logger.error(f"⚠️ Failed to decode JSON from {url}: {e}")

    return None
