"""Demo two-blank 4×4 solver for GUI (scripts only — not production Track B)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

MAGIC_CONSTANT = 34

G0_DURER: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

G1_PARTIAL: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

G1_SOLUTION: list[int] = [2, 2, 7, 3, 3, 10]

_MAGIC_LINES: tuple[tuple[tuple[int, int], ...], ...] = (
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((1, 0), (1, 1), (1, 2), (1, 3)),
    ((2, 0), (2, 1), (2, 2), (2, 3)),
    ((3, 0), (3, 1), (3, 2), (3, 3)),
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 1), (1, 1), (2, 1), (3, 1)),
    ((0, 2), (1, 2), (2, 2), (3, 2)),
    ((0, 3), (1, 3), (2, 3), (3, 3)),
    ((0, 0), (1, 1), (2, 2), (3, 3)),
    ((0, 3), (1, 2), (2, 1), (3, 0)),
)


@dataclass(frozen=True)
class SolveSuccess:
    """Successful two-cell solve payload (1-index coords)."""

    payload: list[int]
    filled_grid: list[list[int]]


@dataclass(frozen=True)
class SolveError:
    """Solver rejection with user-facing message."""

    message: str


def _line_sum(grid: list[list[int]], cells: tuple[tuple[int, int], ...]) -> int:
    return sum(grid[r][c] for r, c in cells)


def is_complete_magic(grid: list[list[int]]) -> bool:
    return _is_complete_magic(grid)


@dataclass(frozen=True)
class VerifySuccess:
    """GUI verify pass."""

    message: str = "Verify: SUCCESS - valid 4x4 magic square (M=34)."


@dataclass(frozen=True)
class VerifyError:
    """GUI verify failure."""

    message: str


def verify_grid(grid: list[list[int]]) -> VerifySuccess | VerifyError:
    """Verify 4×4 size (GREEN boundary) and complete magic square."""
    if len(grid) != 4 or any(not isinstance(row, list) or len(row) != 4 for row in grid):
        return VerifyError("Grid must be 4×4.")

    used: set[int] = set()
    for r in range(4):
        for c in range(4):
            value = grid[r][c]
            if not isinstance(value, int):
                return VerifyError(f"Cell ({r + 1},{c + 1}) must be an integer.")
            if value < 1 or value > 16:
                return VerifyError(
                    f"Cell ({r + 1},{c + 1}) must be 1..16 (complete grid)."
                )
            if value in used:
                return VerifyError(f"Duplicate value {value}.")
            used.add(value)

    if len(used) != 16:
        return VerifyError("Complete grid must contain 1..16 exactly once.")

    if not _is_complete_magic(grid):
        return VerifyError("Magic line sums are not all 34.")

    return VerifySuccess()


def _is_complete_magic(grid: list[list[int]]) -> bool:
    return all(_line_sum(grid, line) == MAGIC_CONSTANT for line in _MAGIC_LINES)


def grid_key(grid: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(row) for row in grid)


def _parse_partial_grid(
    grid: list[list[int]],
) -> tuple[list[tuple[int, int]], list[int]] | SolveError:
    """Return blank cells and missing numbers, or validation error."""
    if len(grid) != 4 or any(not isinstance(row, list) or len(row) != 4 for row in grid):
        return SolveError("Grid must be 4×4.")

    blanks: list[tuple[int, int]] = []
    used: set[int] = set()
    for r in range(4):
        for c in range(4):
            value = grid[r][c]
            if value == 0:
                blanks.append((r, c))
                continue
            if not isinstance(value, int) or value < 1 or value > 16:
                return SolveError(f"Cell ({r + 1},{c + 1}) must be 0 or 1..16.")
            if value in used:
                return SolveError(f"Duplicate non-zero value {value}.")
            used.add(value)

    if len(blanks) != 2:
        return SolveError(f"Exactly two empty cells (0) required; found {len(blanks)}.")

    missing = [n for n in range(1, 17) if n not in used]
    if len(missing) != 2:
        return SolveError("Cannot determine two missing numbers from the grid.")

    return blanks, missing


def find_all_solutions(grid: list[list[int]]) -> list[SolveSuccess] | SolveError:
    """Enumerate every distinct magic completion for two blanks."""
    parsed = _parse_partial_grid(grid)
    if isinstance(parsed, SolveError):
        return parsed

    blanks, missing = parsed
    (r1, c1), (r2, c2) = blanks

    seen_payload: set[tuple[int, ...]] = set()
    solutions: list[SolveSuccess] = []

    for n1 in missing:
        for n2 in missing:
            if n1 == n2:
                continue
            for a, b in ((n1, n2), (n2, n1)):
                trial = [row[:] for row in grid]
                trial[r1][c1] = a
                trial[r2][c2] = b
                if not _is_complete_magic(trial):
                    continue
                payload = [r1 + 1, c1 + 1, a, r2 + 1, c2 + 1, b]
                key = tuple(payload)
                if key in seen_payload:
                    continue
                seen_payload.add(key)
                solutions.append(
                    SolveSuccess(payload=payload, filled_grid=trial),
                )

    solutions.sort(key=lambda s: tuple(s.payload))
    return solutions


def solve_partial_grid(grid: list[list[int]]) -> SolveSuccess | SolveError:
    """Return the first magic completion (smallest payload sort order)."""
    all_solutions = find_all_solutions(grid)
    if isinstance(all_solutions, SolveError):
        return all_solutions
    if not all_solutions:
        return SolveError("No magic square completion for the two blanks (unsolvable).")
    return all_solutions[0]


def format_solve_result(
    grid: Any,
    outcome: SolveSuccess | SolveError,
) -> str:
    """Format a single solve outcome for GUI display."""
    if isinstance(outcome, SolveError):
        return f"Input:\n{grid!r}\n\nSolve: FAILED\n{outcome.message}"

    payload = outcome.payload
    lines = [
        "Input:",
        repr(grid),
        "",
        "Solve: SUCCESS",
        f"payload (int[6]): {payload}",
        f"  blank 1 → row={payload[0]}, col={payload[1]}, value={payload[2]}",
        f"  blank 2 → row={payload[3]}, col={payload[4]}, value={payload[5]}",
        "",
        "Completed 4×4 grid:",
    ]
    for row in outcome.filled_grid:
        lines.append("  " + " ".join(f"{v:2d}" for v in row))
    lines.append("")
    lines.append(f"All magic lines sum to {MAGIC_CONSTANT}.")
    return "\n".join(lines)


def format_solution_iteration(
    grid: Any,
    solutions: list[SolveSuccess],
    index: int,
) -> str:
    """Format one solution with iteration header (1-based index)."""
    total = len(solutions)
    pos = index % total
    outcome = solutions[pos]
    header = [
        f"답안 {pos + 1} / {total}  (버튼을 누를 때마다 다음 답안)",
        "=" * 48,
        "",
    ]
    body = format_solve_result(grid, outcome)
    return "\n".join(header) + body


def grid_literal(grid: list[list[int]]) -> str:
    """Pretty Python literal for filled grid."""
    rows = ", ".join("[" + ", ".join(str(v) for v in row) + "]" for row in grid)
    return f"[{rows}]"
