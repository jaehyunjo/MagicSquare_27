"""GM-2 Golden Master tests for Magic Square two-blank solver.

[TAG][GoldenMaster] — run: pytest -m golden_master -v

Compares API result serialization against tests/golden_master_expected.txt
using the approve pattern (create-if-missing, diff-on-mismatch).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from golden_master import (
    DEFAULT_EXPECTED_PATH,
    ERROR_DUPLICATE_NUMBER,
    ERROR_INVALID_BLANK_COUNT,
    ERROR_NO_VALID_MAGIC_SQUARE,
    SCENARIO_GRIDS,
    SCENARIO_LABELS,
    SCENARIO_ORDER,
    SolverResultDTO,
    approve_golden_master,
    assert_int6_contract,
    assert_reverse_values,
    assert_row_major_blank_order,
    assert_small_first_values,
    capture_all_scenarios,
    capture_scenario,
    parse_sections,
    read_expected_text,
    small_first_succeeds,
    solve_two_step_traced,
    unified_section_diff,
)

pytestmark = pytest.mark.golden_master

GM_TC_CASES: tuple[tuple[str, str], ...] = (
    ("GM-TC-01", "정상 조합 성공 (small-first)"),
    ("GM-TC-02", "reverse 조합 성공 (Step B fallback)"),
    ("GM-TC-03", "INVALID_BLANK_COUNT"),
    ("GM-TC-04", "DUPLICATE_NUMBER"),
    ("GM-TC-05", "NO_VALID_MAGIC_SQUARE"),
)


@pytest.fixture(scope="session")
def golden_master_path() -> Path:
    """Path to the version-controlled Golden Master baseline."""
    return DEFAULT_EXPECTED_PATH


@pytest.fixture(scope="session")
def approve_golden(request: pytest.FixtureRequest) -> bool:
    """True when --approve-golden is passed on the pytest CLI."""
    return bool(request.config.getoption("--approve-golden"))


class TestGoldenMasterMagicSquareFile:
    """Full-file approve: open(expected).read() vs actual capture."""

    def test_gm2_full_baseline_approve(
        self,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """Approve entire golden_master_expected.txt against live solver output."""
        actual = capture_all_scenarios()
        approve_golden_master(golden_master_path, actual, approve=approve_golden)


@pytest.mark.parametrize(
    ("scenario_id", "intent"),
    GM_TC_CASES,
    ids=[case[0] for case in GM_TC_CASES],
)
class TestGoldenMasterMagicSquareCases:
    """GM-TC-01 .. GM-TC-05 per-scenario baseline comparison."""

    def test_gm2_section_matches_baseline(
        self,
        scenario_id: str,
        intent: str,
        golden_master_path: Path,
        approve_golden: bool,
    ) -> None:
        """Section-level approve with unified diff on mismatch."""
        actual = capture_scenario(scenario_id)

        if approve_golden or not golden_master_path.is_file():
            sections: dict[str, str] = {}
            if golden_master_path.is_file():
                sections = parse_sections(read_expected_text(golden_master_path))
            sections[scenario_id] = actual
            merged = "\n\n".join(sections[sid] for sid in SCENARIO_ORDER if sid in sections)
            if merged:
                merged += "\n"
            approve_golden_master(golden_master_path, merged or actual + "\n", approve=True)
            return

        expected_sections = parse_sections(read_expected_text(golden_master_path))
        expected = expected_sections.get(scenario_id)
        assert expected is not None, (
            f"Missing [{scenario_id}] ({intent}) in {golden_master_path}"
        )
        if actual != expected:
            diff = unified_section_diff(scenario_id, expected, actual)
            pytest.fail(f"Golden Master mismatch [{scenario_id}] {intent}:\n\n{diff}")

    def test_gm2_input_grid_fixture(self, scenario_id: str, intent: str) -> None:
        """Each GM case references a fixed 4×4 row-major input grid."""
        grid = SCENARIO_GRIDS[scenario_id]
        assert len(grid) == 4, f"{scenario_id}: grid must have 4 rows"
        assert all(len(row) == 4 for row in grid), f"{scenario_id}: each row must have 4 cols"


@pytest.mark.parametrize(
    ("scenario_id", "intent"),
    GM_TC_CASES,
    ids=[f"contract-{case[0]}" for case in GM_TC_CASES],
)
class TestGoldenMasterMagicSquareContracts:
    """Output / strategy / error contract validation."""

    def test_gm2_solver_result_contract(
        self,
        scenario_id: str,
        intent: str,
    ) -> None:
        """Validate int[6], row-major, 1-index, strategy, and error codes."""
        grid = SCENARIO_GRIDS[scenario_id]
        result = solve_two_step_traced(grid)
        label = SCENARIO_LABELS[scenario_id]

        if scenario_id == "GM-TC-01":
            self._assert_success_contract(grid, result, step="small_first", label=label)
            assert_small_first_values(grid, result.payload)
            return

        if scenario_id == "GM-TC-02":
            assert not small_first_succeeds(grid), f"{label}: Step A must fail"
            self._assert_success_contract(grid, result, step="reverse", label=label)
            assert_reverse_values(grid, result.payload)
            return

        if scenario_id == "GM-TC-03":
            self._assert_error_contract(result, ERROR_INVALID_BLANK_COUNT, label)
            return

        if scenario_id == "GM-TC-04":
            self._assert_error_contract(result, ERROR_DUPLICATE_NUMBER, label)
            return

        if scenario_id == "GM-TC-05":
            self._assert_error_contract(result, ERROR_NO_VALID_MAGIC_SQUARE, label)
            assert result.step == "unsolvable"
            return

        pytest.fail(f"Unhandled scenario {scenario_id}")

    @staticmethod
    def _assert_success_contract(
        grid: list[list[int]],
        result: SolverResultDTO,
        *,
        step: str,
        label: str,
    ) -> None:
        assert result.kind == "success", f"{label}: expected success, got {result.kind}"
        assert result.step == step, f"{label}: expected step {step}, got {result.step}"
        assert result.payload is not None
        assert_int6_contract(result.payload)
        assert_row_major_blank_order(grid, result.payload)

    @staticmethod
    def _assert_error_contract(
        result: SolverResultDTO,
        code: str,
        label: str,
    ) -> None:
        assert result.kind == "error", f"{label}: expected error, got {result.kind}"
        assert result.error_code == code, (
            f"{label}: expected {code}, got {result.error_code}"
        )
        assert result.payload is None
