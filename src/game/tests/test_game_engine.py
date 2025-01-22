import pytest

from src.game.game_engine import DartGameEngine


def test_invalid_game_type():
    """Ensure unsupported game types raise a ValueError."""
    with pytest.raises(ValueError, match="'InvalidGame' is not a valid GameType"):
        DartGameEngine(game_type="InvalidGame", players=[])


def test_x01_scoring():
    """Ensure X01 scoring works properly."""
    players = [MockPlayer("Alice"), MockPlayer("Bob")]
    game = DartGameEngine(game_type="X01", players=players, starting_score=501)

    # Alice throws 60 (Triple 20)
    game.throw_darts("Alice", [{"score": 20, "multiplier": 3}])

    assert players[0].score == 441  # 501 - 60


def test_x01_bust_first_dart():
    """Ensure X01 handles busts properly (score resets if over zero)."""
    players = [MockPlayer("Alice")]
    game = DartGameEngine(game_type="X01", players=players, starting_score=50)

    game.throw_darts("Alice", [{"score": 20, "multiplier": 3}])  # Over 50

    assert players[0].score == 50  # Bust, score should revert


def test_x01_bust_second_dart():
    """Player should bust on the second dart and score should reset."""
    players = [MockPlayer("Charlie")]
    game = DartGameEngine(game_type="X01", players=players, starting_score=50)

    game.throw_darts(
        "Charlie",
        [
            {"score": 20, "multiplier": 2},  # Brings score to 30
            {"score": 25, "multiplier": 1},  # Over 50 → BUST
        ],
    )

    assert players[0].score == 50  # Should reset due to bust


def test_x01_bust_third_dart():
    """Player should bust on the second dart and score should reset."""
    players = [MockPlayer("Charlie")]
    game = DartGameEngine(game_type="X01", players=players, starting_score=50)

    game.throw_darts(
        "Charlie",
        [
            {"score": 20, "multiplier": 1},  # Brings score to 30
            {"score": 20, "multiplier": 1},  # Brings score to 10
            {"score": 20, "multiplier": 1},  # Over 50 → BUST
        ],
    )

    assert players[0].score == 50  # Should reset due to bust


def test_x01_exact_checkout():
    """Player should win when reaching exactly zero, no bust."""
    players = [MockPlayer("Diana")]
    game = DartGameEngine(game_type="X01", players=players, starting_score=50)

    game.throw_darts(
        "Diana",
        [
            {"score": 20, "multiplier": 1},  # Brings score to 30
            {"score": 30, "multiplier": 1},  # Exactly zero
        ],
    )

    assert players[0].score == 0  # Should win
    assert game.winner == "Diana"  # Game should declare Diana as the winner


def test_cricket_scoring():
    """Ensure Cricket scoring correctly tracks hits."""
    players = [MockPlayer("Alice")]
    game = DartGameEngine(game_type="Cricket", players=players)

    game.throw_darts("Alice", [{"score": 20, "multiplier": 2}])  # Hits 20 twice
    game.throw_darts("Alice", [{"score": 20, "multiplier": 1}])  # Hits 20 once

    assert game.state.closed_numbers["Alice"][20] == 3  # ✅ 20 should be closed


def test_cricket_closing():
    """Ensure Cricket detects a winner when all numbers are closed."""
    players = [MockPlayer("Alice")]
    game = DartGameEngine(game_type="Cricket", players=players)

    # Alice closes all numbers
    for num in [20, 19, 18, 17, 16, 15, 25]:  # 25 is Bullseye
        game.throw_darts("Alice", [{"score": num, "multiplier": 3}])

    winner = game.state.check_winner()

    assert winner.name == "Alice"  # ✅ Alice should be the winner


class MockPlayer:
    """Simple mock player for testing purposes."""

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hits = {}

    def record_turn(self, score_before=None, darts=None):
        """Mock method to track turns, compatible with both X01 and Cricket."""
        if darts:
            for dart in darts:
                num = dart["score"]
                if num not in self.hits:
                    self.hits[num] = 0
                self.hits[num] += dart["multiplier"]
