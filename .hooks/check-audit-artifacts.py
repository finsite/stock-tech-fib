#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path


def check_file_exists(path: str, label: str) -> bool:
    file = Path(path)
    if not file.is_file():
        print(f"[ERROR] Missing {label} ({path})")
        return False
    print(f"[OK] Found {label} ({path})")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check for required audit artifacts.")
    parser.add_argument(
        "--sbom",
        default="bom.json",
        help="Path to SBOM file (default: bom.json)",
    )
    parser.add_argument(
        "--vuln",
        default="pip-audit.json",
        help="Path to pip-audit vulnerability report (default: pip-audit.json)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    print("[INFO] Checking required audit artifacts...\n")

    all_ok = True
    all_ok &= check_file_exists(args.sbom, "SBOM")
    all_ok &= check_file_exists(args.vuln, "Vulnerability Report")

    if not all_ok:
        print("\n[FAIL] Audit checks failed. Please regenerate the required files.")
        return 1

    print("\n[SUCCESS] All audit artifacts present and accounted for.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
