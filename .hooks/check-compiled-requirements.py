"""Pre-commit hook to check and auto-fix requirements.txt and requirements-dev.txt
if they are out of sync with requirements.in and requirements-dev.in.
"""

import subprocess  # nosec B404 - subprocess is used safely with controlled arguments
import sys
from pathlib import Path
from shutil import which


def get_pip_compile_path() -> str:
    """Resolve the full path to pip-compile."""
    pip_compile = which("pip-compile")
    if not pip_compile:
        print("[Error] pip-compile not found in PATH.")
        sys.exit(1)
    return pip_compile


PIP_COMPILE = get_pip_compile_path()


def recompile(in_file: str, out_file: str) -> bool:
    """Recompile the output requirements file from its corresponding .in file.

    Args:
        in_file: Path to the .in file.
        out_file: Path to the output .txt file.

    Returns:
        True if successful, False otherwise.

    """
    print(f"[Fix] Recompiling {in_file} -> {out_file}")
    try:
        subprocess.run(  # nosec B603 - fully qualified pip-compile path and safe args
            [PIP_COMPILE, in_file, "--resolver=backtracking", "--output-file", out_file],
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Error] pip-compile failed for {in_file}: {e}")
        return False


def check_file(in_file: str, out_file: str, autofix: bool = True) -> bool:
    """Check if output requirements file is in sync with its .in file and optionally fix it.

    Args:
        in_file: Path to the .in file.
        out_file: Path to the output .txt file.
        autofix: Whether to fix mismatches automatically.

    Returns:
        True if up to date or successfully fixed, False otherwise.

    """
    if not Path(in_file).exists():
        return True  # Skip if input file does not exist

    print(f"[Check] {in_file} -> {out_file}")
    tmp_out = Path(out_file + ".tmp")

    try:
        subprocess.run(  # nosec B603 - safe, static argument list
            [PIP_COMPILE, in_file, "--resolver=backtracking", "--output-file", str(tmp_out)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        print(f"[Error] pip-compile failed during check for {in_file}: {e}")
        return False

    expected = tmp_out.read_text(encoding="utf-8")
    actual = Path(out_file).read_text(encoding="utf-8") if Path(out_file).exists() else ""

    tmp_out.unlink()

    if expected != actual:
        print(f"[Mismatch] {out_file} is out of sync with {in_file}")
        return recompile(in_file, out_file) if autofix else False

    return True


def main() -> int:
    """Main entry point for the hook."""
    ok1 = check_file("requirements.in", "requirements.txt", autofix=True)
    ok2 = check_file("requirements-dev.in", "requirements-dev.txt", autofix=True)

    if not (ok1 and ok2):
        print("[Error] Could not fix all mismatches. Check pip-compile output.")
        return 1

    print("[OK] All requirements files are now up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
