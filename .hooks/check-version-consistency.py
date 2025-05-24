#!/usr/bin/env python

"""Check that the version in pyproject.toml matches the version in __init__.py."""

import re
import sys
from pathlib import Path

PYPROJECT = Path("pyproject.toml")
INIT = Path("src/app/__init__.py")


def extract_version_from_pyproject(pyproject_path: Path) -> str | None:
    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r"^version\s*=\s*[\"'](.+?)[\"']", content, flags=re.MULTILINE)
    return match.group(1) if match else None


def extract_version_from_init(init_path: Path) -> str | None:
    content = init_path.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*[\'"](.+?)[\'"]', content)
    return match.group(1) if match else None


def main() -> int:
    if not PYPROJECT.exists() or not INIT.exists():
        print("Missing pyproject.toml or __init__.py")
        return 1

    pyproject_version = extract_version_from_pyproject(PYPROJECT)
    init_version = extract_version_from_init(INIT)

    if pyproject_version is None or init_version is None:
        print("Could not extract version from one or both files.")
        return 1

    if pyproject_version != init_version:
        print(f"Version mismatch: pyproject.toml={pyproject_version}, __init__.py={init_version}")
        return 1

    print(f"Version match: {pyproject_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
