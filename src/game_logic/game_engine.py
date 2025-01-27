from queue import Queue
from typing import Any
from uuid import uuid4

from .enums import GameType, OutRule
from .game_modes import CricketGame, Dart, X01Game


class DartGameEngine:
    """Manages dart game sessions."""

    def __init__(self, game_type: GameType, **kwargs):
        self.game_type = game_type
        self.events = Queue()
        self.game_started = False

        print(f"{self.game_type=}")
        match self.game_type:
            case GameType.X01:
                self.game = X01Game(
                    starting_score=kwargs.get("starting_score", 501),
                    out_rule=kwargs.get("out_rule", OutRule.SINGLE_OUT),
                )
            case GameType.CRICKET:
                self.game = CricketGame()
        print(f"Created {self.game=}")

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

    ## TODO We will deal with databases later
    # def save_to_database(self, db_session):
    #     """Saves game results to the database once the game ends."""
    #     if not self.is_game_over():
    #         return

    #     from models import GameSession, Player, Turn  # Import models dynamically

    #     game_session = GameSession(
    #         game_mode_id=1,  # Placeholder, should be dynamic
    #         status="completed",
    #     )
    #     db_session.add(game_session)
    #     db_session.commit()

    #     for player in self.game.players:
    #         db_player = db_session.query(Player).filter_by(name=player.name).first()
    #         if not db_player:
    #             db_player = Player(name=player.name)
    #             db_session.add(db_player)
    #             db_session.commit()

    #         for turn in player.turns:
    #             turn_entry = Turn(
    #                 session_id=game_session.id,
    #                 player_id=db_player.id,
    #                 score_before=turn["score_before"],
    #                 score_after=turn["score_after"],
    #                 darts_hit=turn["darts"],
    #             )
    #             db_session.add(turn_entry)

    #     db_session.commit()


class DartgameManager:
    _instance = None
    games: dict = {}

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
