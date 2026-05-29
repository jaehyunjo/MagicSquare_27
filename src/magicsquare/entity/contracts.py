"""PRD verdict / violation code names (SSOT for future green — no runtime use in S0)."""

from __future__ import annotations

# DEF-005: align tests with these in a future green slice (TC-008~011,016).
INPUT_DIMENSION_MISMATCH: str = "INPUT_DIMENSION_MISMATCH"
INCOMPLETE_GRID: str = "INCOMPLETE_GRID"
INPUT_NON_INTEGER: str = "INPUT_NON_INTEGER"

# AC-FR-01-01 current green slice (alias until DEF-005 closed).
INVALID_SIZE: str = "INVALID_SIZE"
