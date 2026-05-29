"""Grid input validation (Boundary). RED stub — green phase implements AC-FR-01-01."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class ValidationFailure(BaseModel):
    """Structured input rejection for AC-FR-01-01 / PRD §8.1 INVALID_SIZE."""

    model_config = ConfigDict(frozen=True)

    code: str
    message: str


def validate_grid_input(grid: Any | None) -> ValidationFailure:
    """Validate raw grid input; return INVALID_SIZE failure or raise until green.

    Args:
        grid: External grid representation (None, nested lists, etc.).

    Returns:
        ValidationFailure when input cannot form a 4×4 canonical grid.

    Raises:
        NotImplementedError: RED phase — no production logic yet.
    """
    raise NotImplementedError(
        "RED: validate_grid_input not implemented (AC-FR-01-01 / green phase)"
    )
