"""AC-FR-01-01 | PRD §8.1 INVALID_SIZE — empty or invalid-dimension grid rejection."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from magicsquare.boundary.validation import ValidationFailure, validate_grid_input
from magicsquare.control.orchestrator import verify_magic_square

# AC-FR-01-01 | PRD §8.1 INVALID_SIZE
INVALID_SIZE_CODE = "INVALID_SIZE"
PRD_SECTION_81_MESSAGE = "Grid must be 4x4."


def _assert_invalid_size_failure(result: ValidationFailure) -> None:
    assert isinstance(result, ValidationFailure)
    assert result.code == INVALID_SIZE_CODE
    assert result.message == PRD_SECTION_81_MESSAGE


class TestAcFr0101InvalidSize:
    """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — Boundary input rejection (RED)."""

    def test_none_grid_returns_invalid_size_and_message(self) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — happy path of failure."""
        # AC-FR-01-01
        # Given — grid reference absent
        grid: None = None

        # When — boundary validates raw input
        result = validate_grid_input(grid)

        # Then — structured INVALID_SIZE failure
        _assert_invalid_size_failure(result)

    def test_none_grid_exact_message_prd_section_81_wording(self) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — character-level message match."""
        # AC-FR-01-01
        # Given
        grid: None = None

        # When
        result = validate_grid_input(grid)

        # Then — PRD §8.1 wording, byte-for-byte
        assert result.message == PRD_SECTION_81_MESSAGE
        assert len(result.message) == len(PRD_SECTION_81_MESSAGE)
        assert result.message != "Grid must be 4x4"
        assert result.message != "grid must be 4x4."

    def test_none_grid_returns_validation_failure_model_type(self) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — pydantic failure DTO type."""
        # AC-FR-01-01
        # Given
        grid: None = None

        # When
        result = validate_grid_input(grid)

        # Then
        assert type(result) is ValidationFailure
        assert isinstance(result, BaseModel)
        _assert_invalid_size_failure(result)

    @pytest.mark.parametrize(
        "grid",
        [
            pytest.param([], id="empty_list"),
            pytest.param([[]] * 4, id="four_empty_rows"),
            pytest.param([[1, 2, 3, 4]] * 3, id="three_by_four"),
        ],
    )
    def test_boundary_shape_returns_invalid_size_failure(
        self, grid: list[Any]
    ) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — [] / [[]]*4 / 3×4 boundaries."""
        # AC-FR-01-01
        # Given — non-canonical 4×4 inputs
        # When
        result = validate_grid_input(grid)

        # Then
        _assert_invalid_size_failure(result)

    def test_empty_list_returns_invalid_size_code(self) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — length-zero sequence (TC-011)."""
        # AC-FR-01-01
        # Given
        grid: list[Any] = []

        # When
        result = validate_grid_input(grid)

        # Then
        assert result.code == INVALID_SIZE_CODE
        assert result.message == PRD_SECTION_81_MESSAGE

    def test_three_by_four_returns_invalid_size_code(self) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — row count ≠ 4."""
        # AC-FR-01-01
        # Given
        grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]

        # When
        result = validate_grid_input(grid)

        # Then
        _assert_invalid_size_failure(result)

    def test_none_grid_orchestrator_resolve_zero_calls(self) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — resolve() spy via control path."""
        # AC-FR-01-01
        # Given
        grid: None = None
        resolve_spy = MagicMock(name="resolve")

        # When — orchestrator must short-circuit before domain
        result = verify_magic_square(grid, resolve=resolve_spy)

        # Then
        _assert_invalid_size_failure(result)
        resolve_spy.assert_not_called()

    def test_none_grid_boundary_resolve_zero_calls(self) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — boundary path does not invoke control."""
        # AC-FR-01-01
        # Given
        grid: None = None

        # When
        result = validate_grid_input(grid)

        # Then
        _assert_invalid_size_failure(result)

    def test_none_grid_resolve_called_fails_isolation(self) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — any resolve() call is a failure."""
        # AC-FR-01-01
        # Given
        grid: None = None
        resolve_spy = MagicMock(name="resolve", return_value={"verdict": "Valid"})

        # When
        result = verify_magic_square(grid, resolve=resolve_spy)

        # Then
        assert resolve_spy.call_count == 0, "resolve() must not be called for grid=None"
        _assert_invalid_size_failure(result)

    def test_orchestrator_injected_validate_short_circuits_resolve(self) -> None:
        """Control uses injected validate; resolve must not run on boundary failure."""
        # Given
        expected = ValidationFailure(
            code=INVALID_SIZE_CODE,
            message=PRD_SECTION_81_MESSAGE,
        )
        validate_stub = MagicMock(name="validate", return_value=expected)
        resolve_spy = MagicMock(name="resolve")

        # When
        result = verify_magic_square(
            None,
            validate=validate_stub,
            resolve=resolve_spy,
        )

        # Then
        validate_stub.assert_called_once_with(None)
        resolve_spy.assert_not_called()
        assert result is expected

    def test_scope_only_invalid_size_not_other_ac_codes(self) -> None:
        """AC-FR-01-01 | PRD §8.1 INVALID_SIZE — AC-FR-01-02~05 / FR-02~05 excluded."""
        # AC-FR-01-01
        # Given — only dimension/emptiness inputs for this AC
        scoped_grids: list[Any] = [None, [], [[]] * 4, [[1, 2, 3, 4]] * 3]
        forbidden_codes = {
            "INCOMPLETE_GRID",
            "INPUT_NON_INTEGER",
            "INPUT_DIMENSION_MISMATCH",
            "I1_DUPLICATE",
            "I1_MISSING",
            "I2_LINE_SUM_MISMATCH",
        }

        # When / Then
        for grid in scoped_grids:
            result = validate_grid_input(grid)
            assert result.code == INVALID_SIZE_CODE
            assert result.code not in forbidden_codes
            assert result.message == PRD_SECTION_81_MESSAGE
