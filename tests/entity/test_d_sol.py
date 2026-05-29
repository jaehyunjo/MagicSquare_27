"""Track B — D-SOL-01~04 solver RED skeleton (Report/09).

Domain Mock 금지 — solution / is_magic_square must not be mocked.
"""

from __future__ import annotations

import pytest

# from control.solver import solution


class TestDSol01Through04:
    """FR-05 TwoCellSolver use case — skeleton only."""

    def test_d_sol_01_g1_step_a_success_returns_int6(self) -> None:
        """D-SOL-01 | G1 Step A → [2,2,7,3,3,10]."""
        # Given — G1
        # When — solution(matrix)  # small-first
        pytest.fail("RED: D-SOL-01 — G1 Step A solution [2,2,7,3,3,10]")

    def test_d_sol_02_g2_step_b_success(self) -> None:
        """D-SOL-02 | G2 Step A fail, Step B → [3,3,6,4,4,1]."""
        # Given — G2 (TBD)
        pytest.fail("RED: D-SOL-02 — G2 TBD")

    def test_d_sol_03_g3_both_steps_fail_unsolvable(self) -> None:
        """D-SOL-03 | G3 both fail → UnsolvableDomainError."""
        # Given — G3 (TBD)
        # When — solution(matrix)
        pytest.fail("RED: D-SOL-03 — G3 TBD unsolvable domain error")

    def test_d_sol_04_g1_output_contract_length_and_index(self) -> None:
        """D-SOL-04 | G1 success → len 6, 1-index coords, values in 1..16."""
        # Given — G1
        # When — solution(matrix)
        pytest.fail("RED: D-SOL-04 — output contract len/coords/values")
