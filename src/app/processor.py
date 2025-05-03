# """
# Processor for calculating Fibonacci retracement and extension levels.

# This module provides utilities for analyzing stock price data using Fibonacci tools.
# """

# from typing import Literal

# import pandas as pd

# from app.logger import setup_logger

# logger = setup_logger(__name__)

# # Define the retracement and extension levels
# RETRACEMENT_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786]
# EXTENSION_LEVELS = [1.272, 1.618, 2.0, 2.618]


# def calculate_fibonacci_levels(
#     data: pd.DataFrame,
#     method: Literal["retracement", "extension"] = "retracement",
#     swing_high: float | None = None,
#     swing_low: float | None = None,
# ) -> dict[str, float]:
#     """
#     Calculate Fibonacci retracement or extension levels.

#     Args:
#     ----
#         data (pd.DataFrame): Historical OHLC stock data.
#         method (str): Type of Fibonacci levels to calculate ('retracement' or 'extension').
#         swing_high (float, optional): Manually specified swing high.
#         swing_low (float, optional): Manually specified swing low.

#     Returns:
#     -------
#         dict[str, float]: A dictionary of Fibonacci levels with corresponding prices.
#     """
#     try:
#         if swing_high is None:
#             high_raw = data["High"].max() if "High" in data else None
#             swing_high = float(high_raw) if pd.notnull(high_raw) else None

#         if swing_low is None:
#             low_raw = data["Low"].min() if "Low" in data else None
#             swing_low = float(low_raw) if pd.notnull(low_raw) else None

#         if swing_high is None or swing_low is None:
#             logger.error("Swing high or low could not be determined.")
#             return {}
#         levels = {}

#         if method == "retracement":
#             for level in RETRACEMENT_LEVELS:
#                 price = swing_high - (swing_high - swing_low) * level
#                 levels[f"{int(level * 100)}%"] = round(price, 2)
#         elif method == "extension":
#             for level in EXTENSION_LEVELS:
#                 price = swing_high + (swing_high - swing_low) * (level - 1)
#                 levels[f"{level:.3f}x"] = round(price, 2)
#         else:
#             logger.error("Invalid method for Fibonacci calculation: %s", method)
#             return {}

#         logger.info(
#             "Calculated Fibonacci %s levels (High: %.2f, Low: %.2f): %s",
#             method,
#             swing_high,
#             swing_low,
#             levels,
#         )
#         return levels

#     except Exception as e:
#         logger.error("Error calculating Fibonacci levels: %s", e)
#         return {}
"""
Processor for calculating Fibonacci retracement and extension levels.

This module provides utilities for analyzing stock price data using Fibonacci tools.
"""

from typing import Literal

import pandas as pd
from pandas import Series

from app.logger import setup_logger

logger = setup_logger(__name__)

RETRACEMENT_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786]
EXTENSION_LEVELS = [1.272, 1.618, 2.0, 2.618]


def calculate_fibonacci_levels(
    data: pd.DataFrame,
    method: Literal["retracement", "extension"] = "retracement",
    swing_high: float | None = None,
    swing_low: float | None = None,
) -> dict[str, float]:
    """Calculate Fibonacci retracement or extension levels."""
    try:
        if swing_high is None:
            high_series = data.get("High", pd.Series(dtype=float))
            if isinstance(high_series, Series):
                high_value = high_series.max()
                swing_high = float(high_value) if pd.notna(high_value) else None

        if swing_low is None:
            low_series = data.get("Low", pd.Series(dtype=float))
            if isinstance(low_series, Series):
                low_value = low_series.min()
                swing_low = float(low_value) if pd.notna(low_value) else None

        if swing_high is None or swing_low is None:
            logger.error("Swing high or low could not be determined.")
            return {}

        levels = {}
        if method == "retracement":
            for level in RETRACEMENT_LEVELS:
                price = swing_high - (swing_high - swing_low) * level
                levels[f"{int(level * 100)}%"] = round(price, 2)
        elif method == "extension":
            for level in EXTENSION_LEVELS:
                price = swing_high + (swing_high - swing_low) * (level - 1)
                levels[f"{level:.3f}x"] = round(price, 2)
        else:
            logger.error("Invalid method for Fibonacci calculation: %s", method)
            return {}

        logger.info(
            "Calculated Fibonacci %s levels (High: %.2f, Low: %.2f): %s",
            method,
            swing_high,
            swing_low,
            levels,
        )
        return levels

    except Exception as e:
        logger.error("Error calculating Fibonacci levels: %s", e)
        return {}
