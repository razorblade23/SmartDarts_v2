from typing import Protocol


class Player(Protocol):
    def record_turn(self, darts: list[dict[str, int]]): ...


class X01Player:
    """Represents a player in the game with score tracking."""

    def __init__(self, name: str, starting_score: int):
        self.name = name
        self.starting_score = starting_score
        self.score = starting_score
        self.turns = []

    def record_turn(self, score_before: int, darts: list[dict[str, int]]):
        """Records a turn where darts were thrown."""
        score_after = self.score
        self.turns.append(
            {
                "score_before": score_before,
                "score_after": score_after,
                "darts": darts,
            }
        )


class CricketPlayer:
    """Represents a player in a Cricket game."""

    def __init__(self, name: str):
        self.name = name
        self.closed_numbers = {num: 0 for num in range(15, 21)}  # 15-20 and Bullseye
        self.closed_numbers[25] = 0  # Bullseye
        self.score = 0  # Points scored if opponent hasn’t closed a number
        self.turns = []  # Stores turns taken

    def record_turn(self, darts: list[dict[str, int]]):
        """Records a player's turn (for tracking later)."""
        self.turns.append({"darts": darts, "score": self.score})

    def is_closed(self, number: int) -> bool:
        """Checks if a number is closed (3 hits)."""
        return self.closed_numbers.get(number, 0) >= 3
