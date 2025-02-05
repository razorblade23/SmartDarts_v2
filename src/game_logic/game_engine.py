from queue import Queue
from typing import Any
from uuid import uuid4

from .enums import GameType, OutRule
from .game_modes import CricketGame, Dart, X01Game


class DartGameEngine:
    """Manages dart game sessions."""

    def __init__(self, game_type: GameType, **kwargs):
        self.events = Queue()
        self.game_started = False

        match game_type:
            case GameType.X01:
                starting_score = kwargs.get("starting_score", 501)
                out_rule = kwargs.get("out_rule", OutRule.SINGLE_OUT)

                self.game = X01Game(
                    starting_score=starting_score,
                    out_rule=OutRule(out_rule),
                )
            case GameType.CRICKET:
                self.game = CricketGame()

        # Future games can be added easily here

    def start_game(self):
        self.game_started = True

    def get_game_state(self) -> list[dict[str, Any]]:
        return self.game.get_stats()

    def throw_dart(self, dart: dict[str, int]):
        """Handles a turn by passing responsibility to the game mode."""
        event = self.game.throw_dart(Dart(**dart))
        self.events.put(event)

    def get_player_score(self, player_name: str) -> int:
        for player in self.game.players:
            if player.name == player_name:
                return player.score

    def add_player(self, name: str):
        """Registers a new player to the game."""
        self.game.add_player(name)

    def is_game_over(self):
        """Checks if the game has ended."""
        return self.game.winner is not None

    @property
    def winner(self):
        """Returns the winner's name."""
        return self.game.winner


class DartgameManager:
    _instance = None
    games: dict[str, DartGameEngine] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DartgameManager, cls).__new__(cls)
            cls._instance.games = {}
        return cls._instance

    def create_game(self, gametype: GameType, **kwargs) -> str:
        game_id = str(uuid4())
        self.games[game_id] = DartGameEngine(game_type=gametype, **kwargs)
        return game_id

    def get_game(self, game_id: str) -> DartGameEngine | None:
        return self.games.get(game_id)
