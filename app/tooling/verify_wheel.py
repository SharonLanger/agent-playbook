"""Verify Wheel byte identity against an independently recorded SHA-256 digest."""

import argparse
import hashlib
import hmac
from pathlib import Path


def verify_wheel(wheel: Path, expected: str) -> None:
    if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
        raise ValueError(
            "Expected SHA-256 must be 64 lowercase hexadecimal characters."
        )
    actual = hashlib.sha256(wheel.read_bytes()).hexdigest()
    if not hmac.compare_digest(actual, expected):
        raise ValueError(f"Wheel SHA-256 mismatch: expected {expected}, got {actual}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    parser.add_argument("sha256")
    args = parser.parse_args()
    try:
        verify_wheel(args.wheel, args.sha256)
    except (OSError, ValueError) as error:
        parser.exit(1, str(error) + "\n")
    print("SHA-256 verified.")


if __name__ == "__main__":
    main()
