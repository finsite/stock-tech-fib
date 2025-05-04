"""
Request data from a URL with a timeout.

The function performs a GET request to the given URL, with a specified timeout in
seconds. If the request is successful, it returns the JSON response as a dictionary. If
the request fails, it logs an error message and returns None.
"""

import requests

from app.utils.setup_logger import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)


def request_with_timeout(url: str, timeout: int = 10) -> dict | None:
    """
    Request data from a URL with a timeout.

    Args:
    ----
        url (str): The URL to request data from.
        timeout (int): The time in seconds to wait for the request to complete.

    Returns:
    -------
        Optional[dict]: The JSON response from the request, or None if the request fails.

    Args:
      url: str:
      timeout: int:  (Default value = 10)

    Returns:
    """
    # Check if the URL is empty
    if not url:
        logger.error("URL cannot be empty.")
        return None

    # Perform the GET request
    try:
        response = requests.get(url, timeout=timeout)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Check the Content-Type header
        content_type = response.headers.get("Content-Type")
        if content_type is None or "application/json" not in content_type:
            logger.error(f"Expected JSON response from {url}, but got {content_type}.")
            return None

        # Parse and return JSON data
        json_response = response.json()
        if json_response is None:
            logger.error("Received empty JSON response.")
            return None

        return json_response

    # Handle exceptions
    except requests.exceptions.Timeout:
        logger.error(f"Timeout occurred while requesting {url}.")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred while requesting {url}: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request exception occurred: {e}")
    except ValueError as e:
        logger.error(f"Error decoding JSON response from {url}: {e}")
    return None
