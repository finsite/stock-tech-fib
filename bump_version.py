import sys

from packaging.version import Version


def next_version(current: str, part: str) -> str:
    """Increment a version.

    Args:
    ----
        current: The current version string.
        part: The part of the version to increment ('major', 'minor', or 'patch').

    Returns:
    -------
        A new version string with the specified part incremented.

    """
    v = Version(current)
    if part == "major":
        return f"{v.major + 1}.0.0"
    elif part == "minor":
        return f"{v.major}.{v.minor + 1}.0"
    elif part == "patch":
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
