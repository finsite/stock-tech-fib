#!/usr/bin/env python

"""Ensure version consistency across pyproject.toml, __init__.py, and CHANGELOG.md."""

import re
import sys
from pathlib import Path

PYPROJECT = Path("pyproject.toml")
INIT = Path("src/app/__init__.py")
CHANGELOG = Path("CHANGELOG.md")


def extract_version_from_pyproject(path: Path) -> str | None:
    content = path.read_text(encoding="utf-8")
    match = re.search(r"^version\s*=\s*[\"'](.+?)[\"']", content, flags=re.MULTILINE)
    return match.group(1) if match else None


def extract_version_from_init(path: Path) -> str | None:
    content = path.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*[\'"](.+?)[\'"]', content, flags=re.MULTILINE)
    return match.group(1) if match else None


def extract_version_from_changelog(path: Path) -> str | None:
    content = path.read_text(encoding="utf-8")
    matches = re.findall(r"^##\s*v?(\d+\.\d+\.\d+)", content, flags=re.MULTILINE)
    # Exclude early stubs like 0.0.0 or 0.1.0 if newer exist
    if matches:
        for version in matches:
            if version not in {"0.0.0", "0.1.0"}:
                return version
        return matches[0]  # fallback
    return None


def safe_print(message: str):
    """Print message with fallback for non-UTF-8 terminals (e.g., Windows cmd)."""
    try:
        print(message)
    except UnicodeEncodeError:
        # Strip emojis or non-ASCII characters
        ascii_message = message.encode("ascii", errors="ignore").decode("ascii")
        print(ascii_message)


def main() -> int:
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
