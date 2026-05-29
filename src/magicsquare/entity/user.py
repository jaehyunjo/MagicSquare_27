from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    """A system user who can submit or verify grids.

    This entity is intentionally minimal. It captures identity and a display name
    and enforces basic invariants.

    Attributes:
        user_id: Stable identifier for the user.
        display_name: Human-readable name.
    """

    user_id: str
    display_name: str

    @classmethod
    def create(cls, user_id: str, display_name: str) -> User:
        """Creates a new ``User``.

        Args:
            user_id: Non-empty identifier.
            display_name: Non-empty display name.

        Returns:
            A validated ``User`` instance.

        Raises:
            ValueError: If ``user_id`` or ``display_name`` is blank.
        """

        if not isinstance(user_id, str) or user_id.strip() == "":
            raise ValueError("user_id must be a non-empty string")

        if not isinstance(display_name, str) or display_name.strip() == "":
            raise ValueError("display_name must be a non-empty string")

        return cls(user_id=user_id, display_name=display_name)
