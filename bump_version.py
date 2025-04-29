"""
A command-line tool to bump the version of a Python package.

This is a simple tool to bump the version of a Python package. It takes two
arguments: the current version, and the part of the version to increment ('major',
'minor', or 'patch').

The tool will then print a new version string with the specified part
incremented.

"""


import sys

from packaging.version import Version


def next_version(current: str, part: str) -> str:
    """
    Increment a version.

    Args:
        current (str): The current version string.
        part (str): The part of the version to increment ('major', 'minor', or 'patch').

    Returns:
        str: A new version string with the specified part incremented.

    Raises:
        ValueError: If the specified part is not 'major', 'minor', or 'patch'.

    """
    v = Version(current)
    if part == "major":
        # Increment the major version and reset the minor and patch versions.
        return f"{v.major + 1}.0.0"
    elif part == "minor":
        # Increment the minor version and reset the patch version.
        return f"{v.major}.{v.minor + 1}.0"
    elif part == "patch":
        # Increment the patch version.
        return f"{v.major}.{v.minor}.{v.micro + 1}"
    else:
        raise ValueError("Specify 'major', 'minor', or 'patch'.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python setup.py <current_version> <major|minor|patch>")
        sys.exit(1)
    current_version, part = sys.argv[1], sys.argv[2]
    try:
        print(next_version(current_version, part))
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
