#!/usr/bin/env python

"""Ensure and enforce version consistency across pyproject.toml, __init__.py, and CHANGELOG.md."""

import re
import sys
from pathlib import Path

PYPROJECT = Path("pyproject.toml")
INIT = Path("src/app/__init__.py")
CHANGELOG = Path("CHANGELOG.md")


def extract_version_from_pyproject(path: Path) -> str | None:
    """Extract the version string from pyproject.toml using a regex pattern."""
    content = path.read_text(encoding="utf-8")
    match = re.search(r"^version\s*=\s*[\"'](.+?)[\"']", content, flags=re.MULTILINE)
    return match.group(1) if match else None


def extract_version_from_init(path: Path) -> str | None:
    """Extract the __version__ variable from __init__.py."""
    content = path.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*[\'"](.+?)[\'"]', content, flags=re.MULTILINE)
    return match.group(1) if match else None


def extract_version_from_changelog(path: Path) -> str | None:
    """Extract the most recent semantic version from changelog headings."""
    content = path.read_text(encoding="utf-8")
    matches = re.findall(r"^##\s*v?(\d+\.\d+\.\d+)", content, flags=re.MULTILINE)
    if matches:
        for version in matches:
            if version not in {"0.0.0", "0.1.0"}:
                return version
        return matches[0]
    return None


def update_init_version(path: Path, version: str) -> None:
    """Update the __version__ variable in __init__.py."""
    content = path.read_text(encoding="utf-8")
    content = re.sub(
        r'^__version__\s*=\s*[\'"].+?[\'"]',
        f'__version__ = "{version}"',
        content,
        flags=re.MULTILINE,
    )
    path.write_text(content, encoding="utf-8")


def update_changelog_version(path: Path, version: str) -> None:
    """Update the most recent version heading in the changelog."""
    content = path.read_text(encoding="utf-8")
    updated = re.sub(
        r"^(##\s*)v?\d+\.\d+\.\d+",
        f"\\1v{version}",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    path.write_text(updated, encoding="utf-8")


def safe_print(message: str):
    """Prints safely, falling back to ASCII if Unicode causes errors (e.g., on Windows)."""
    try:
        print(message)
    except UnicodeEncodeError:
        ascii_message = message.encode("ascii", errors="ignore").decode("ascii")
        print(ascii_message)


def main() -> int:
    """Compare versions across files and auto-correct if inconsistent."""
    pyproject_version = extract_version_from_pyproject(PYPROJECT)
    init_version = extract_version_from_init(INIT)
    changelog_version = extract_version_from_changelog(CHANGELOG)

    if not all([pyproject_version, init_version, changelog_version]):
        safe_print("❌ Could not extract version from one or more files.")
        safe_print(f"pyproject.toml: {pyproject_version}")
        safe_print(f"__init__.py:     {init_version}")
        safe_print(f"CHANGELOG.md:    {changelog_version}")
        return 1

    updated = False

    if pyproject_version != init_version:
        update_init_version(INIT, pyproject_version)
        safe_print(f"🛠 Updated __init__.py version to {pyproject_version}")
        updated = True

    if pyproject_version != changelog_version:
        update_changelog_version(CHANGELOG, pyproject_version)
        safe_print(f"🛠 Updated CHANGELOG.md version to {pyproject_version}")
        updated = True

    if updated:
        safe_print(f"✅ Versions synced to: {pyproject_version}")
        return 1  # Still return failure to trigger pre-commit attention

    safe_print(f"✅ Version match: {pyproject_version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
