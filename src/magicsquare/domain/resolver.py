"""Domain resolve entry point. RED stub — must not run for grid=None (AC-FR-01-01)."""

from __future__ import annotations

from typing import Any


def resolve(grid: Any) -> Any:
    """Apply domain magic-square logic to a canonical grid.

    Raises:
        NotImplementedError: RED phase — no production logic yet.
    """
    raise NotImplementedError("RED: resolve not implemented (green phase)")
