from typing import Literal

OutputMode = Literal["log", "queue", "stdout", "rest", "s3", "database"]

def validate_dict(data: dict, required_keys: list[str]) -> bool:
    """Check that all required keys are present in the dict."""
    return all(k in data for k in required_keys)