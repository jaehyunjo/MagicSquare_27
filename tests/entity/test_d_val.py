"""Track B — D-VAL-01~06 magic square validator RED skeleton (Report/09).

Domain Mock 금지 — is_magic_square must not be patched in these tests.
"""

from __future__ import annotations

import pytest

# from entity.validator import is_magic_square


class TestDVal01Through06:
    """FR-04 is_magic_square — skeleton only."""

    def test_d_val_01_g0_complete_magic_returns_true(self) -> None:
        """D-VAL-01 | G0 complete → true."""
        # Given — G0 Dürer grid
        # When — is_magic_square(matrix)
        pytest.fail("RED: D-VAL-01 — G0 complete grid must return true")

    def test_d_val_02_row_sum_mismatch_returns_false(self) -> None:
        """D-VAL-02 | G0 R0 broken (16→15 at (1,1)) → false."""
        # Given — G0 variant row-0 sum mismatch
        # When — is_magic_square(matrix)
        pytest.fail("RED: D-VAL-02 — row sum mismatch must return false")

    def test_d_val_03_col_sum_mismatch_returns_false(self) -> None:
        """D-VAL-03 | G0 C1 broken (swap (4,2)/(4,3)) → false."""
        # Given — G0 variant col-1 sum mismatch
        # When — is_magic_square(matrix)
        pytest.fail("RED: D-VAL-03 — column sum mismatch must return false")

    def test_d_val_04_diagonal_mismatch_returns_false(self) -> None:
        """D-VAL-04 | G0 anti-diagonal broken → false."""
        # Given — G0 variant D_ANTI: (1,4) 13→14
        # When — is_magic_square(matrix)
        pytest.fail("RED: D-VAL-04 — diagonal sum mismatch must return false")

    def test_d_val_05a_out_of_range_returns_false(self) -> None:
        """D-VAL-05a | G0 with 17 at (4,4) → false."""
        # Given — G0 + 17
        # When — is_magic_square(matrix)
        pytest.fail("RED: D-VAL-05a — value 17 must return false")

    def test_d_val_05b_duplicate_returns_false(self) -> None:
        """D-VAL-05b | G0 duplicate 7 → false."""
        # Given — G0 duplicate at (2,2)
        # When — is_magic_square(matrix)
        pytest.fail("RED: D-VAL-05b — duplicate value must return false")

    def test_d_val_06_zero_in_complete_grid_returns_false(self) -> None:
        """D-VAL-06 | G0 with 0 in filled grid → false."""
        # Given — G0, (2,2) 7→0
        # When — is_magic_square(matrix)
        pytest.fail("RED: D-VAL-06 — zero in complete grid must return false")
