"""Module to handle output of analysis results to a chosen output target.

This implementation logs the result and prints it to stdout.
"""

import json

from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def send_to_output(data: dict[str, any]) -> None:
    """Outputs processed analysis results to the configured output.

    Currently logs the output and prints it to the console.
    This function can be extended to push to a database, file, or external service.

    Args:
    ----
        data (dict[str, any]): The processed analysis result as a dictionary.

    Returns:
    -------
        None

    """
    try:
        formatted_output: str = json.dumps(data, indent=4)

        # Log output
        logger.info("Sending data to output:\n%s", formatted_output)

        # Print output to console (placeholder for future integration)
        print(formatted_output)

    except Exception as e:
        logger.error("Failed to send output: %s", e)
