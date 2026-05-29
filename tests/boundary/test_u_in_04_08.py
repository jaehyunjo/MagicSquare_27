"""Track A — U-IN-04~08 input validation RED skeleton (Report/09).

U-IN-01~03: Report/08 Full RED — tests/unit/boundary/test_ac_fr_01_01_*.py (do not duplicate).
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.dual_track_red

# from boundary.input_validator import InputValidator


class TestUIn04Through08:
    """FR-01 Failure envelope E002/E004/E005 — skeleton only."""

    def test_u_in_04_zero_empty_cells_returns_e002(self) -> None:
        """U-IN-04 | G0 complete grid (no zeros) → E002."""
        # Given — G0: [[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]
        # matrix = ...
        # When — InputValidator.validate(matrix)
        # validator = InputValidator()
        # result = validator.validate(matrix)
        pytest.fail("RED: U-IN-04 — G0 with zero blanks → E002 envelope")

    def test_u_in_05_three_blanks_returns_e002(self) -> None:
        """U-IN-05 | G1 + extra zero (three blanks) → E002."""
        # Given — G1 with third blank at (1,1) 0-index
        # When — InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-05 — three empty cells → E002 envelope")

    def test_u_in_06_negative_value_returns_e004(self) -> None:
        """U-IN-06 | G1 with (1,1)=-1 → E004."""
        # Given — G1, cell (1,1) = -1
        # When — InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-06 — value -1 → E004 range envelope")

    def test_u_in_07_value_17_returns_e004(self) -> None:
        """U-IN-07 | G1 with (4,4)=17 → E004."""
        # Given — G1, cell (4,4) = 17
        # When — InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-07 — value 17 → E004 range envelope")

    def test_u_in_08_duplicate_nonzero_returns_e005(self) -> None:
        """U-IN-08 | G1 with duplicate 5 at (2,4) → E005."""
        # Given — G1, (2,4) = 5 duplicates (2,1)
        # When — InputValidator.validate(matrix)
        pytest.fail("RED: U-IN-08 — non-zero duplicate → E005 envelope")
