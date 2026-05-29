from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from magicsquare.entity.user import User


def test_user_create_valid() -> None:
    """TC: creating a valid user should succeed."""
    # Arrange
    user_id = "u-001"
    display_name = "Alice"

    # Act
    user = User.create(user_id=user_id, display_name=display_name)

    # Assert
    assert user.user_id == "u-001"
    assert user.display_name == "Alice"


@pytest.mark.parametrize(
    "user_id",
    [
        "",
        "   ",
    ],
)
def test_user_create_rejects_blank_user_id(user_id: str) -> None:
    """TC: blank user_id is invalid."""
    # Arrange
    display_name = "Alice"

    # Act / Assert
    with pytest.raises(ValueError, match="user_id must be a non-empty string"):
        User.create(user_id=user_id, display_name=display_name)


@pytest.mark.parametrize(
    "display_name",
    [
        "",
        "   ",
    ],
)
def test_user_create_rejects_blank_display_name(display_name: str) -> None:
    """TC: blank display_name is invalid."""
    # Arrange
    user_id = "u-001"

    # Act / Assert
    with pytest.raises(ValueError, match="display_name must be a non-empty string"):
        User.create(user_id=user_id, display_name=display_name)


def test_user_is_immutable() -> None:
    """TC: user entity should be immutable (value object-like behavior)."""
    # Arrange
    user = User.create(user_id="u-001", display_name="Alice")

    # Act / Assert
    with pytest.raises(FrozenInstanceError):
        user.display_name = "Bob"  # type: ignore[misc]
