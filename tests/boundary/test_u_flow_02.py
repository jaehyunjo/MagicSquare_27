"""Track A — U-FLOW-02 Domain isolation RED skeleton (Report/09 extended)."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.dual_track_red

# from unittest.mock import MagicMock
# from boundary.ui_boundary import UIBoundary
# from control.solve_partial import SolvePartialMagicSquare


class TestUFlow02Extended:
    """invalid input → SolvePartialMagicSquare.execute call_count == 0."""

    def test_u_flow_02_null_matrix_execute_zero_calls(self) -> None:
        """U-FLOW-02a | matrix=null → failure envelope, execute spy 0."""
        # Given — matrix = None
        # execute_spy = MagicMock(name="execute")
        # When — UIBoundary.solve(matrix, execute=execute_spy)
        pytest.fail("RED: U-FLOW-02 — null input must not call execute")

    def test_u_flow_02_empty_matrix_execute_zero_calls(self) -> None:
        """U-FLOW-02b | matrix=[] → failure envelope, execute spy 0."""
        # Given — matrix = []
        # execute_spy = MagicMock(name="execute")
        # When — UIBoundary.solve(matrix, execute=execute_spy)
        pytest.fail("RED: U-FLOW-02 — empty matrix must not call execute")

    def test_u_flow_02_invalid_e005_execute_zero_calls(self) -> None:
        """U-FLOW-02c | E005 duplicate input → execute spy 0."""
        # Given — G1 with duplicate non-zero (U-IN-08 grid)
        # execute_spy = MagicMock(name="execute")
        # When — UIBoundary.solve(matrix, execute=execute_spy)
        pytest.fail("RED: U-FLOW-02 — E005 path must not call execute")
