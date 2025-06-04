"""Perform a GET request with timeout and JSON validation.

This module provides a function to safely request JSON data from a URL
with a configurable timeout. It handles exceptions, validates the response
content type, and logs errors appropriately.
"""

from typing import Any, cast

import requests

from app.utils.setup_logger import setup_logger

logger = setup_logger(__name__)


def request_with_timeout(url: str, timeout: int = 10) -> dict[str, Any] | None:
    """Makes a GET request to the specified URL with a specified timeout.

    Parameters
    ----------
    url : str
        The URL to request.
    timeout : int
        The timeout in seconds. Defaults to 10 seconds.
    url :
        str:
    timeout :
        int:  (Default value = 10)
    url :
        str:
    timeout :
        int:  (Default value = 10)
    url :
        str:
    timeout :
        int:  (Default value = 10)
    url : str :

    timeout : int :
        (Default value = 10)
    url: str :

    timeout: int :
         (Default value = 10)

    Returns
    -------


    """
    if not url:
        logger.error("URL cannot be empty.")
        return None

    try:
        # Send a GET request to the URL with the specified timeout
        response = requests.get(url, timeout=timeout)
        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Get the content type of the response
        content_type = response.headers.get("Content-Type")
        # If the content type is not JSON, log an error and return None
        if content_type is None or "application/json" not in content_type:
            logger.error(f"Expected JSON response from {url}, but got {content_type}.")
            return None

        # Get the JSON response
        json_response = cast(dict[str, Any], response.json())
        # If the JSON response is empty, log an error and return None
        if json_response is None:
            logger.error("Received empty JSON response.")
            return None

        # Return the JSON response
        return json_response

    except requests.exceptions.Timeout:
        # Log an error if the request timed out
        logger.error(f"Timeout occurred while requesting {url}.")
    except requests.exceptions.HTTPError as e:
        # Log an error if the request had an HTTP error
        logger.error(f"HTTP error occurred while requesting {url}: {e}")
    except requests.exceptions.RequestException as e:
        # Log an error if the request had any other exception
        logger.error(f"Request exception occurred: {e}")
    except ValueError as e:
        # Log an error if the JSON response was invalid
        logger.error(f"Error decoding JSON response from {url}: {e}")
    # Return None if any of the above exceptions occurred
    return None
