"""Track A — U-OUT-01~03 output contract RED skeleton (Report/09)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.dual_track_red

# from boundary.ui_boundary import UIBoundary


class TestUOut01Through03:
    """FR-02 int[6] output contract — skeleton only."""

    def test_u_out_01_success_payload_length_six(self) -> None:
        """U-OUT-01 | G1 valid input → success, len(data)==6."""
        # Given — G1 partial grid (two blanks)
        # When — UIBoundary.solve(matrix)
        # boundary = UIBoundary()
        # result = boundary.solve(matrix)
        pytest.fail("RED: U-OUT-01 — success payload length must be 6")

    def test_u_out_02_success_coords_one_indexed_in_range(self) -> None:
        """U-OUT-02 | G1 → r,c coordinates in [1,4] (1-index)."""
        # Given — G1
        # When — UIBoundary.solve(matrix)
        pytest.fail("RED: U-OUT-02 — output coordinates must be 1-index in [1,4]")

    def test_u_out_03_success_values_match_g1_step_a(self) -> None:
        """U-OUT-03 | G1 → [2,2,7,3,3,10] Step A solution."""
        # Given — G1
        # When — UIBoundary.solve(matrix)
        # Then (green) — data == [2, 2, 7, 3, 3, 10]
        pytest.fail("RED: U-OUT-03 — G1 Step A expected int[6] solution")
