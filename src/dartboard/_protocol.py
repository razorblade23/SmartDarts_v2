from typing import Protocol


class DartboardConfig(Protocol):
    """Protocol for dartboard configurations."""

    @property
    def matrix(self) -> dict[int, dict[str, int]]:
        """The dartboard scoring matrix."""
        ...

    @property
    def col_pins(self) -> list[int]:
        """GPIO pins for the columns."""
        ...

    @property
    def row_pins(self) -> list[int]:
        """GPIO pins for the rows."""
        ...

    @property
    def multiplier_pins(self) -> dict[int, list[int]]:
        """Multiplier GPIO pins"""
        ...
