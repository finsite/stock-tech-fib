"""Processor for calculating Fibonacci retracement and extension levels.

Provides `analyze()` as the main entrypoint for queue-based analysis workflows.
"""

from typing import Any, Literal

import pandas as pd

from app.logger import setup_logger

logger = setup_logger(__name__)

RETRACEMENT_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786]
EXTENSION_LEVELS = [1.272, 1.618, 2.0, 2.618]


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    """Main processor entrypoint for Fibonacci analysis.

    Args:
    ----
        data (dict): Message containing 'symbol', 'timestamp', and OHLC history.

    Returns:
    -------
        dict: Analysis results including retracement and extension levels.

    """
    try:
        df = pd.DataFrame(data.get("history", []))
        symbol = data.get("symbol", "N/A")
        timestamp = data.get("timestamp", "N/A")

        if df.empty or not {"High", "Low"}.issubset(df.columns):
            logger.warning("Missing or invalid history data for symbol: %s", symbol)
            return {
                "symbol": symbol,
                "timestamp": timestamp,
                "error": "Missing or invalid history data",
            }

        retracement, swing_high, swing_low = calculate_fibonacci_levels(df, method="retracement")
        extension, _, _ = calculate_fibonacci_levels(
            df, method="extension", swing_high=swing_high, swing_low=swing_low
        )

        result = {
            "symbol": symbol,
            "timestamp": timestamp,
            "fibonacci": {
                "swing_high": swing_high,
                "swing_low": swing_low,
                "retracement": retracement,
                "extension": extension,
            },
        }

        logger.info("Processed Fibonacci analysis for %s at %s", symbol, timestamp)
        return result

    except Exception as e:
        logger.error("Fibonacci analysis failed: %s", e)
        return {
            "symbol": data.get("symbol", "N/A"),
            "timestamp": data.get("timestamp", "N/A"),
            "error": str(e),
        }


def calculate_fibonacci_levels(
    data: pd.DataFrame,
    method: Literal["retracement", "extension"] = "retracement",
    swing_high: float | None = None,
    swing_low: float | None = None,
) -> tuple[dict[str, float], float | None, float | None]:
    """Calculate Fibonacci retracement or extension levels.

    Args:
    ----
        data (pd.DataFrame): Historical OHLC stock data.
        method (str): 'retracement' or 'extension'.
        swing_high (float, optional): Manual high override.
        swing_low (float, optional): Manual low override.

    Returns:
    -------
        tuple: (level map, swing_high, swing_low)

    """
    try:
        if swing_high is None:
            swing_high = float(data.get("High", pd.Series(dtype=float)).max())
        if swing_low is None:
            swing_low = float(data.get("Low", pd.Series(dtype=float)).min())

        if pd.isna(swing_high) or pd.isna(swing_low):
            logger.error("Invalid swing points detected.")
            return {}, None, None

        levels = {}
        if method == "retracement":
            for level in RETRACEMENT_LEVELS:
                price = swing_high - (swing_high - swing_low) * level
                levels[f"{int(level * 100)}%"] = round(price, 2)
        elif method == "extension":
            for level in EXTENSION_LEVELS:
                price = swing_high + (swing_high - swing_low) * (level - 1)
                levels[f"{level:.3f}x"] = round(price, 2)

        return levels, swing_high, swing_low

    except Exception as e:
        logger.error("Error in Fibonacci %s level calculation: %s", method, e)
        return {}, None, None
