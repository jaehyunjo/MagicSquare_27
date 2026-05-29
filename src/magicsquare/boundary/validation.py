"""Grid input validation (Boundary)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from magicsquare.entity.contracts import INVALID_SIZE

_INVALID_SIZE_MESSAGE = "Grid must be 4x4."


class ValidationFailure(BaseModel):
    """Structured input rejection for AC-FR-01-01 / PRD §8.1 INVALID_SIZE."""

    model_config = ConfigDict(frozen=True)

    code: str
    message: str


def _invalid_size_failure() -> ValidationFailure:
    return ValidationFailure(code=INVALID_SIZE, message=_INVALID_SIZE_MESSAGE)


def dimension_validation_failure(grid: Any | None) -> ValidationFailure | None:
    """Return INVALID_SIZE when dimension is invalid; None when list is 4×4 shaped.

    Args:
        grid: Raw grid (None or nested lists).

    Returns:
        ValidationFailure for null/empty/wrong shape; None if rows and cols are 4×4.
    """
    if grid is None:
        return _invalid_size_failure()
    if not isinstance(grid, list):
        return None
    if len(grid) == 0 or len(grid) != 4:
        return _invalid_size_failure()
    for row in grid:
        if not isinstance(row, list) or len(row) != 4:
            return _invalid_size_failure()
    return None


def validate_grid_input(grid: Any | None) -> ValidationFailure:
    """Validate raw grid input; return INVALID_SIZE failure or raise until green.

    Args:
        grid: External grid representation (None, nested lists, etc.).

    Returns:
        ValidationFailure when input cannot form a 4×4 canonical grid.

    Raises:
        NotImplementedError: For inputs outside the current green slice.
    """
    if grid is not None and not isinstance(grid, list):
        raise NotImplementedError(
            "GREEN partial: only grid=None and [] implemented (AC-FR-01-01)"
        )

    failure = dimension_validation_failure(grid)
    if failure is not None:
        return failure

    raise NotImplementedError(
        "GREEN partial: valid 4x4 shape not implemented (AC-FR-01-01)"
    )
