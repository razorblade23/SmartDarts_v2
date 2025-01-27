from src.game_logic.enums import GameType
from src.game_logic.game_engine import DartGameEngine


def test_x01_scoring():
    """Ensure X01 scoring works properly."""
    players = [MockPlayer("Alice"), MockPlayer("Bob")]
    game = DartGameEngine(game_type=GameType.X01, starting_score=501)
    for p in players:
        game.add_player(p.name)

    # Alice throws 60 (Triple 20)
    game.throw_dart({"score": 20, "multiplier": 3})

    assert game.get_player_score("Alice") == 441  # 501 - 60


def test_x01_bust_first_dart():
    """Ensure X01 handles busts properly (score resets if over zero)."""
    players = [MockPlayer("Alice")]
    game = DartGameEngine(game_type=GameType.X01, starting_score=50)
    for p in players:
        game.add_player(p.name)

    game.throw_dart({"score": 20, "multiplier": 3})  # Over 50

    assert game.get_player_score("Alice") == 50  # Bust, score should revert


def test_x01_exact_checkout():
    """Player should win when reaching exactly zero, no bust."""
    players = [MockPlayer("Diana")]
    game = DartGameEngine(game_type=GameType.X01, starting_score=50)
    for p in players:
        game.add_player(p.name)

    game.throw_dart({"score": 20, "multiplier": 1})
    game.throw_dart({"score": 30, "multiplier": 1})

    assert game.get_player_score("Diana") == 0  # Should win
    assert game.winner == "Diana"  # Game should declare Diana as the winner


## TODO When cricket is finished, enable these tests
# def test_cricket_scoring():
#     """Ensure Cricket scoring correctly tracks hits."""
#     players = [MockPlayer("Alice")]
#     game = DartGameEngine(game_type=GameType.CRICKET, players=players)

#     game.throw_dart({"score": 20, "multiplier": 2})  # Hits 20 twice
#     game.throw_dart({"score": 20, "multiplier": 1})  # Hits 20 once

#     assert game.game.closed_numbers["Alice"][20] == 3  # ✅ 20 should be closed


# def test_cricket_closing():
#     """Ensure Cricket detects a winner when all numbers are closed."""
#     players = [MockPlayer("Alice")]
#     game = DartGameEngine(game_type=GameType.CRICKET, players=players)

#     # Alice closes all numbers
#     for num in [20, 19, 18, 17, 16, 15, 25]:  # 25 is Bullseye
#         game.throw_dart("Alice", [{"score": num, "multiplier": 3}])

#     winner = game.game.check_winner()

#     assert winner.name == "Alice"  # ✅ Alice should be the winner


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
