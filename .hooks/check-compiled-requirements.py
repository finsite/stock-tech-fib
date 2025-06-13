#!/usr/bin/env python3
"""Pre-commit hook to check and auto-fix requirements.txt and requirements-dev.txt
if they are out of sync with requirements.in and requirements-dev.in.
"""

import sys
from shutil import which
from pathlib import Path
import subprocess  # nosec B404


PIP_COMPILE = which("pip-compile")
if not PIP_COMPILE:
    print("[Error] pip-compile not found in PATH.")
    sys.exit(1)


def recompile(in_file: str, out_file: str) -> bool:
    print(f"[Fix] Recompiling {in_file} -> {out_file}")
    try:
        subprocess.run(  # nosec B603
            [PIP_COMPILE, in_file, "--resolver=backtracking", "--output-file", out_file],
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Error] pip-compile failed for {in_file}: {e}")
        return False


def check_file(in_file: str, out_file: str, autofix: bool = True) -> bool:
    if not Path(in_file).exists():
        return True  # skip if .in file doesn't exist

    print(f"[Check] {in_file} -> {out_file}")
    try:
        subprocess.run(  # nosec B603
            [PIP_COMPILE, in_file, "--resolver=backtracking", "--output-file", out_file + ".tmp"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        print(f"[Error] pip-compile failed during check for {in_file}: {e}")
        return False

    expected = Path(out_file + ".tmp").read_text(encoding="utf-8")
    actual = Path(out_file).read_text(encoding="utf-8") if Path(out_file).exists() else ""

    Path(out_file + ".tmp").unlink()

    if expected != actual:
        print(f"[Mismatch] {out_file} is out of sync with {in_file}")
        if autofix:
            return recompile(in_file, out_file)
        return False

    return True


def main():
    ok1 = check_file("requirements.in", "requirements.txt", autofix=True)
    ok2 = check_file("requirements-dev.in", "requirements-dev.txt", autofix=True)

    if not (ok1 and ok2):
        print("[Error] Could not fix all mismatches. Check pip-compile output.")
        sys.exit(1)

    print("[OK] All requirements files are now up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
