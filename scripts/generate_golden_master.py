"""Generate tests/golden_master_expected.txt from live solver output.

Usage:
    python scripts/generate_golden_master.py
    python scripts/generate_golden_master.py --output tests/golden_master_expected.txt
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from golden_master import DEFAULT_EXPECTED_PATH, write_expected_file

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for Golden Master baseline generation."""
    parser = argparse.ArgumentParser(
        description="Generate Golden Master expected output for Magic Square solver.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_EXPECTED_PATH,
        help="Path to write the baseline file (default: tests/golden_master_expected.txt)",
    )
    args = parser.parse_args(argv)

    target = write_expected_file(args.output)
    logger.info("Wrote Golden Master baseline: %s", target)
    return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    sys.exit(main())
