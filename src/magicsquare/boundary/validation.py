"""Grid input validation (Boundary). RED stub — green phase implements AC-FR-01-01."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class ValidationFailure(BaseModel):
    """Structured input rejection for AC-FR-01-01 / PRD §8.1 INVALID_SIZE."""

    model_config = ConfigDict(frozen=True)

    code: str
    message: str


_INVALID_SIZE_CODE = "INVALID_SIZE"
_INVALID_SIZE_MESSAGE = "Grid must be 4x4."


def validate_grid_input(grid: Any | None) -> ValidationFailure:
    """Validate raw grid input; return INVALID_SIZE failure or raise until green.

    Args:
        grid: External grid representation (None, nested lists, etc.).

    Returns:
        ValidationFailure when input cannot form a 4×4 canonical grid.

    Raises:
        NotImplementedError: For inputs outside the current green slice.
    """
    if grid is None:
        return ValidationFailure(
            code=_INVALID_SIZE_CODE,
            message=_INVALID_SIZE_MESSAGE,
        )
    raise NotImplementedError(
        "GREEN partial: only grid=None implemented (AC-FR-01-01)"
    )
