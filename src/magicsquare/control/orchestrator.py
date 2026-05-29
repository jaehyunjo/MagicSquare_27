"""Verification orchestrator (Control). RED stub."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from magicsquare.boundary.validation import ValidationFailure, validate_grid_input


def verify_magic_square(
    grid: Any | None,
    *,
    resolve: Callable[[Any], Any] | None = None,
) -> ValidationFailure:
    """Run boundary validation then domain resolve when input is valid.

    Args:
        grid: Raw grid from boundary adapter.
        resolve: Domain entry point (injected for tests).

    Returns:
        ValidationFailure when input is rejected at boundary.

    Raises:
        NotImplementedError: For inputs outside the current green slice.
    """
    if grid is None or isinstance(grid, list):
        return validate_grid_input(grid)
    raise NotImplementedError(
        "GREEN partial: only None and list grid inputs implemented (AC-FR-01-01)"
    )
