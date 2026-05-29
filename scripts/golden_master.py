"""Golden Master capture for Magic Square two-blank solver (scripts only).

Serializes solver Result DTO (success payload or error code) for approval tests.
Uses demo_solver validation and magic checks with small-first → reverse strategy.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from demo_solver import SolveError, _is_complete_magic, _parse_partial_grid

ERROR_INVALID_BLANK_COUNT = "INVALID_BLANK_COUNT"
ERROR_DUPLICATE_NUMBER = "DUPLICATE_NUMBER"
ERROR_NO_VALID_MAGIC_SQUARE = "NO_VALID_MAGIC_SQUARE"

SolveStep = Literal["small_first", "reverse", "validation_error", "unsolvable"]

SCENARIO_ORDER: tuple[str, ...] = (
    "GM-TC-01",
    "GM-TC-02",
    "GM-TC-03",
    "GM-TC-04",
    "GM-TC-05",
)

SCENARIO_LABELS: dict[str, str] = {
    "GM-TC-01": "normal_success",
    "GM-TC-02": "reverse_success",
    "GM-TC-03": "invalid_blank_count",
    "GM-TC-04": "duplicate_number",
    "GM-TC-05": "no_valid_magic_square",
}

# small-first succeeds (Step A) — Dürer partial, blanks (1,3) & (3,3) 1-index
GRID_NORMAL_SUCCESS: list[list[int]] = [
    [16, 3, 0, 13],
    [5, 10, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# small-first fails, reverse succeeds (Step B) — SC-DOM-SOL-001 / G2
GRID_REVERSE_SUCCESS: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# complete grid — zero blanks
GRID_INVALID_BLANK_COUNT: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# G1 partial with duplicate 5 at (2,4) 1-index
GRID_DUPLICATE_NUMBER: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 5],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# valid 2-blank input with no magic completion
GRID_NO_VALID_MAGIC_SQUARE: list[list[int]] = [
    [8, 10, 6, 7],
    [15, 11, 13, 0],
    [0, 9, 2, 3],
    [14, 16, 5, 12],
]

SCENARIO_GRIDS: dict[str, list[list[int]]] = {
    "GM-TC-01": GRID_NORMAL_SUCCESS,
    "GM-TC-02": GRID_REVERSE_SUCCESS,
    "GM-TC-03": GRID_INVALID_BLANK_COUNT,
    "GM-TC-04": GRID_DUPLICATE_NUMBER,
    "GM-TC-05": GRID_NO_VALID_MAGIC_SQUARE,
}

DEFAULT_EXPECTED_PATH = (
    Path(__file__).resolve().parent.parent / "tests" / "golden_master_expected.txt"
)

_SECTION_HEADER = re.compile(r"^\[([A-Z0-9-]+)\]\s*$")


@dataclass(frozen=True)
class SolverResultDTO:
    """Canonical solver outcome for Golden Master comparison."""

    kind: Literal["success", "error"]
    payload: tuple[int, ...] | None = None
    error_code: str | None = None
    step: SolveStep | None = None


def _message_to_error_code(message: str) -> str:
    if "Exactly two empty cells" in message:
        return ERROR_INVALID_BLANK_COUNT
    if "Duplicate non-zero" in message:
        return ERROR_DUPLICATE_NUMBER
    if "No magic square completion" in message:
        return ERROR_NO_VALID_MAGIC_SQUARE
    return "SOLVER_ERROR"


def _attempt_assignment(
    grid: list[list[int]],
    blanks: list[tuple[int, int]],
    missing: list[int],
    *,
    small_first: bool,
) -> tuple[int, ...] | None:
    """Try one assignment strategy; return int[6] payload or None."""
    (r1, c1), (r2, c2) = blanks
    low, high = min(missing), max(missing)
    n1, n2 = (low, high) if small_first else (high, low)
    trial = [row[:] for row in grid]
    trial[r1][c1] = n1
    trial[r2][c2] = n2
    if _is_complete_magic(trial):
        return (r1 + 1, c1 + 1, n1, r2 + 1, c2 + 1, n2)
    return None


def solve_two_step(grid: list[list[int]]) -> SolverResultDTO:
    """Solve with small-first then reverse assignment (production strategy)."""
    return solve_two_step_traced(grid)


def solve_two_step_traced(grid: list[list[int]]) -> SolverResultDTO:
    """Solve and record which strategy produced the outcome."""
    parsed = _parse_partial_grid(grid)
    if isinstance(parsed, SolveError):
        return SolverResultDTO(
            kind="error",
            error_code=_message_to_error_code(parsed.message),
            step="validation_error",
        )

    blanks, missing = parsed
    payload = _attempt_assignment(grid, blanks, missing, small_first=True)
    if payload is not None:
        return SolverResultDTO(kind="success", payload=payload, step="small_first")

    payload = _attempt_assignment(grid, blanks, missing, small_first=False)
    if payload is not None:
        return SolverResultDTO(kind="success", payload=payload, step="reverse")

    return SolverResultDTO(
        kind="error",
        error_code=ERROR_NO_VALID_MAGIC_SQUARE,
        step="unsolvable",
    )


def small_first_succeeds(grid: list[list[int]]) -> bool:
    """Return True when Step A (small-first) yields a magic completion."""
    parsed = _parse_partial_grid(grid)
    if isinstance(parsed, SolveError):
        return False
    blanks, missing = parsed
    return _attempt_assignment(grid, blanks, missing, small_first=True) is not None


def format_grid_input(grid: list[list[int]]) -> str:
    """Render grid as row-major text (GUI-style)."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def format_payload(payload: tuple[int, ...]) -> str:
    """Render int[6] as compact list literal."""
    return "[" + ",".join(str(value) for value in payload) + "]"


def serialize_scenario(scenario_id: str, grid: list[list[int]], result: SolverResultDTO) -> str:
    """Serialize one scenario block (API result capture)."""
    lines = [f"[{scenario_id}]", "Input:", format_grid_input(grid), ""]
    if result.kind == "success":
        assert result.payload is not None
        lines.extend(["Output:", format_payload(result.payload)])
    else:
        assert result.error_code is not None
        lines.extend(["Error:", result.error_code])
    return "\n".join(lines)


def capture_scenario(scenario_id: str) -> str:
    """Capture one scenario block from the live solver."""
    grid = SCENARIO_GRIDS[scenario_id]
    result = solve_two_step_traced(grid)
    return serialize_scenario(scenario_id, grid, result)


def capture_all_scenarios() -> str:
    """Capture every scenario as a single Golden Master document."""
    blocks = [capture_scenario(scenario_id) for scenario_id in SCENARIO_ORDER]
    return "\n\n".join(blocks) + "\n"


def parse_sections(text: str) -> dict[str, str]:
    """Parse a Golden Master file into scenario-id → block text."""
    sections: dict[str, str] = {}
    current_id: str | None = None
    current_lines: list[str] = []

    for line in text.splitlines():
        header = _SECTION_HEADER.match(line)
        if header:
            if current_id is not None:
                sections[current_id] = "\n".join(current_lines).rstrip()
            current_id = header.group(1)
            current_lines = [line]
            continue
        if current_id is not None:
            current_lines.append(line)

    if current_id is not None:
        sections[current_id] = "\n".join(current_lines).rstrip()

    return sections


def read_expected_text(expected_path: Path) -> str:
    """Read baseline file contents (approve comparison source)."""
    with expected_path.open(encoding="utf-8") as handle:
        return handle.read()


def unified_diff_text(expected: str, actual: str, *, label: str = "golden_master") -> str:
    """Build unified diff: --- expected / +++ actual / @@ hunks @@."""
    diff_lines = difflib.unified_diff(
        expected.splitlines(),
        actual.splitlines(),
        fromfile="expected",
        tofile="actual",
        lineterm="",
    )
    body = "\n".join(diff_lines)
    if not body:
        return ""
    return f"--- [{label}] diff ---\n{body}"


def unified_section_diff(scenario_id: str, expected: str, actual: str) -> str:
    """Build unified diff for one scenario block."""
    return unified_diff_text(expected, actual, label=scenario_id)


def approve_golden_master(
    expected_path: Path,
    actual_text: str,
    *,
    approve: bool = False,
) -> None:
    """Approve pattern: create baseline or compare open(expected).read() vs actual."""
    if approve or not expected_path.is_file():
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        expected_path.write_text(actual_text, encoding="utf-8")
        return

    expected_text = read_expected_text(expected_path)
    if expected_text == actual_text:
        return

    expected_sections = parse_sections(expected_text)
    actual_sections = parse_sections(actual_text)
    diffs: list[str] = []

    for scenario_id in SCENARIO_ORDER:
        exp = expected_sections.get(scenario_id, "")
        act = actual_sections.get(scenario_id, "")
        if exp != act:
            diffs.append(unified_section_diff(scenario_id, exp, act))

    missing = [sid for sid in SCENARIO_ORDER if sid not in actual_sections]
    if missing:
        diffs.append(f"Missing scenarios in actual output: {', '.join(missing)}")

    extra = sorted(set(actual_sections) - set(SCENARIO_ORDER))
    if extra:
        diffs.append(f"Unexpected scenarios in actual output: {', '.join(extra)}")

    full_diff = unified_diff_text(expected_text, actual_text, label="full document")
    message = "Golden Master mismatch:\n\n" + full_diff + "\n\n" + "\n\n".join(diffs)
    raise AssertionError(message)


def assert_int6_contract(payload: tuple[int, ...]) -> None:
    """Validate int[6] output contract: length, 1-index coords, value range."""
    assert len(payload) == 6, f"int[6] length expected, got {len(payload)}"
    r1, c1, n1, r2, c2, n2 = payload
    for name, coord in (("r1", r1), ("c1", c1), ("r2", r2), ("c2", c2)):
        assert 1 <= coord <= 4, f"{name} must be 1-index 1..4, got {coord}"
    for name, value in (("n1", n1), ("n2", n2)):
        assert 1 <= value <= 16, f"{name} must be 1..16, got {value}"
    assert n1 != n2, "filled values must differ"


def assert_row_major_blank_order(grid: list[list[int]], payload: tuple[int, ...]) -> None:
    """First blank in payload must precede second in row-major order."""
    parsed = _parse_partial_grid(grid)
    assert not isinstance(parsed, SolveError)
    blanks, _ = parsed
    (r1, c1), (r2, c2) = blanks
    assert payload[0] == r1 + 1 and payload[1] == c1 + 1
    assert payload[3] == r2 + 1 and payload[4] == c2 + 1
    assert (r1, c1) <= (r2, c2), "blanks must be row-major ordered"


def assert_small_first_values(grid: list[list[int]], payload: tuple[int, ...]) -> None:
    """Step A places min(missing) at first blank, max at second."""
    parsed = _parse_partial_grid(grid)
    assert not isinstance(parsed, SolveError)
    _, missing = parsed
    low, high = min(missing), max(missing)
    assert payload[2] == low and payload[5] == high


def assert_reverse_values(grid: list[list[int]], payload: tuple[int, ...]) -> None:
    """Step B places max(missing) at first blank, min at second."""
    parsed = _parse_partial_grid(grid)
    assert not isinstance(parsed, SolveError)
    _, missing = parsed
    low, high = min(missing), max(missing)
    assert payload[2] == high and payload[5] == low


def write_expected_file(path: Path | None = None) -> Path:
    """Generate and write the Golden Master baseline file."""
    target = path or DEFAULT_EXPECTED_PATH
    text = capture_all_scenarios()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    return target
