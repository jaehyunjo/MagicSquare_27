"""Domain resolve entry point (Entity). Must not run for rejected boundary input."""

from __future__ import annotations

from typing import Any


def resolve(grid: Any) -> Any:
    """Apply domain magic-square logic to a canonical grid.

    Raises:
        NotImplementedError: GREEN phase — no production logic yet.
    """
    raise NotImplementedError("RED: resolve not implemented (green phase)")
