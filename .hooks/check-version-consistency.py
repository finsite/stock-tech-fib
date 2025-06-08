#!/usr/bin/env python

"""Ensure version consistency across pyproject.toml, __init__.py, and CHANGELOG.md."""

import re
import sys
from pathlib import Path

PYPROJECT = Path("pyproject.toml")
INIT = Path("src/app/__init__.py")
CHANGELOG = Path("CHANGELOG.md")


def extract_version_from_pyproject(path: Path) -> str | None:
    """Extract the version string from pyproject.toml."""
    content = path.read_text(encoding="utf-8")
    match = re.search(r"^version\s*=\s*[\"'](.+?)[\"']", content, flags=re.MULTILINE)
    return match.group(1) if match else None


def extract_version_from_init(path: Path) -> str | None:
    """Extract the __version__ value from __init__.py."""
    content = path.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*[\'"](.+?)[\'"]', content, flags=re.MULTILINE)
    return match.group(1) if match else None


def extract_version_from_changelog(path: Path) -> str | None:
    """Extract the latest semantic version from the changelog headings."""
    content = path.read_text(encoding="utf-8")
    matches = re.findall(r"^##\s*v?(\d+\.\d+\.\d+)", content, flags=re.MULTILINE)
    if matches:
        for version in matches:
            if version not in {"0.0.0", "0.1.0"}:
                return version
        return matches[0]
    return None


def safe_print(message: str):
    """Print a message safely, even on limited encodings (e.g., Windows cmd)."""
    try:
        print(message)
    except UnicodeEncodeError:
        ascii_message = message.encode("ascii", errors="ignore").decode("ascii")
        print(ascii_message)


def main() -> int:
    """Compare versions across pyproject, __init__, and changelog files."""
    pyproject_version = extract_version_from_pyproject(PYPROJECT)
    init_version = extract_version_from_init(INIT)
    changelog_version = extract_version_from_changelog(CHANGELOG)

    if not all([pyproject_version, init_version, changelog_version]):
        safe_print("❌ Could not extract version from one or more files.")
        safe_print(f"pyproject.toml: {pyproject_version}")
        safe_print(f"__init__.py:     {init_version}")
        safe_print(f"CHANGELOG.md:    {changelog_version}")
        return 1

    if pyproject_version != init_version or pyproject_version != changelog_version:
        safe_print("❌ Version mismatch:")
        safe_print(f"pyproject.toml: {pyproject_version}")
        safe_print(f"__init__.py:     {init_version}")
        safe_print(f"CHANGELOG.md:    {changelog_version}")
        return 1

    safe_print(f"✅ Version match: {pyproject_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
