"""Verification orchestrator (Control). RED stub."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from magicsquare.boundary.validation import ValidationFailure


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
        NotImplementedError: RED phase — no production logic yet.
    """
    raise NotImplementedError(
        "RED: verify_magic_square not implemented (AC-FR-01-01 / green phase)"
    )
