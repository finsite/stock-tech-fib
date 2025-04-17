from typing import Any  # ✅ Fixes the error


def add_numbers(a: int | float, b: int | float) -> int | float:
    """
    Adds two numbers and returns the result.

    Args:
        a (Union[int, float]): The first number.
        b (Union[int, float]): The second number.

    Returns:
        Union[int, float]: The sum of the two numbers.
    """
    return a + b


class ExampleClass:
    """A simple example class."""

    def __init__(self, value: Any):
        """
        Initializes ExampleClass.

        Args:
            value (Any): The value to store.
        """
        self.value = value

    def get_value(self) -> Any:
        """
        Retrieve the value assigned to the object.

        Returns:
            Any: The stored value.
        """
        return self.value
