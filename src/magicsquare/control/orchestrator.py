"""Verification orchestrator (Control)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from magicsquare.boundary.validation import ValidationFailure

ValidateFn = Callable[[Any | None], ValidationFailure]
ResolveFn = Callable[[Any], Any]


def _default_validate(grid: Any | None) -> ValidationFailure:
    from magicsquare.boundary.validation import validate_grid_input

    return validate_grid_input(grid)


def _default_resolve(grid: Any) -> Any:
    from magicsquare.entity.resolver import resolve

    return resolve(grid)


def verify_magic_square(
    grid: Any | None,
    *,
    validate: ValidateFn | None = None,
    resolve: ResolveFn | None = None,
) -> ValidationFailure:
    """Run boundary validation then domain resolve when input is valid.

    Args:
        grid: Raw grid from boundary adapter.
        validate: Boundary validation (injected for tests / composition root).
        resolve: Domain entry point (injected for tests).

    Returns:
        ValidationFailure when input is rejected at boundary.

    Raises:
        NotImplementedError: For inputs outside the current green slice.
    """
    validate_fn = validate if validate is not None else _default_validate

    if grid is None or isinstance(grid, list):
        return validate_fn(grid)

    raise NotImplementedError(
        "GREEN partial: only None and list grid inputs implemented (AC-FR-01-01)"
    )
