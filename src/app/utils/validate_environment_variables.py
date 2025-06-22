"""Validate required environment variables.

This module provides a function to validate that all required environment variables are set.

Functions
---------
validate_environment_variables(required_variables)
    Verifies that all required environment variables are set before continuing.
"""

import os

from app.utils.setup_logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def validate_environment_variables(required_variables: list[str]) -> None:
    """Verify that all required environment variables are set.

    Args:
        required_variables (list[str]): A list of environment variable names to validate.

    Raises:
        TypeError: If the input is not a list of strings.
        OSError: If any required variables are missing.
    """
    if not isinstance(required_variables, list) or not all(
        isinstance(var, str) for var in required_variables
    ):
        logger.error("❌ 'required_variables' must be a list of strings.")
        raise TypeError("required_variables must be a list of strings.")

    missing_variables = [var for var in required_variables if not os.getenv(var)]

    if missing_variables:
        message = (
            f"Missing required environment variables: {', '.join(missing_variables)}. "
            "Please check your environment configuration and try again."
        )
        logger.error(f"❌ {message}")
        raise OSError(message)

    logger.info("✅ All required environment variables are set.")
