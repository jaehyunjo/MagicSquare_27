"""Pytest configuration and Dual-Track grid fixtures (placeholder).

G0~G3: Report/09 · Report/02 부록 — 수치 확정 전 주석만 유지.
"""

from __future__ import annotations

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register Golden Master approve CLI flag."""
    parser.addoption(
        "--approve-golden",
        action="store_true",
        default=False,
        help="Regenerate tests/golden_master_expected.txt from current solver output.",
    )


# --- G0: complete magic square (Dürer / TC-001) ---
# G0 = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# --- G1: partial — blanks 1-index (2,2), (3,3); missing {7, 10} ---
# G1 = [
#     [16, 3, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]

# --- G2: TBD (Report/02 부록 / SC-DOM-SOL-001) ---
# G2 = None  # placeholder — Step A fail, Step B → [3, 3, 6, 4, 4, 1]

# --- G3: TBD (both-fail → UnsolvableDomainError) ---
# G3 = None  # placeholder
