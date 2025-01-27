from abc import ABC, abstractmethod

from pydantic import BaseModel

from .enums import OutRule, ThrowDartEvent
from .players import CricketPlayer, Player, X01Player


class Dart(BaseModel):
    score: int
    multiplier: int


class GameMode(ABC):
    """Base class for all dart game modes."""

    def __init__(self):
        self.players: list[Player] = []
        self.score: int = 0

    @abstractmethod
    def throw_dart(self, dart: dict[str, int]):
        """Handles dart throws, must be implemented by each game type."""
        pass

    @abstractmethod
    def check_winner(self):
        """Checks if the game is over."""
        pass


class X01Game(GameMode):
    """Handles X01 dart game logic (301, 501, etc.)."""

    def __init__(
        self,
        starting_score: int = 501,
        darts_per_player: int = 3,
        out_rule: OutRule = OutRule.SINGLE_OUT,
    ):
        self.starting_score = starting_score
        self.darts_per_player = darts_per_player
        self.out_rule = out_rule
        self.players: list[X01Player] = []
        self.current_player: X01Player | None = None
        self.current_player_index = 0

    def add_player(self, player_name: str):
        """Adds a player to the game."""
        self.players.append(
            X01Player(
                position=len(self.players) + 1,
                name=player_name,
                starting_score=self.starting_score,
            )
        )

    def get_stats(self):
        stats = []

        for player in self.players:
            p_stats = {
                "name": player.name,
                "starting_score": player.starting_score,
                "current_score": player.score,
                "turns": player.turns,
            }
            stats.append(p_stats)
        return stats

    def check_winner(self, player: X01Player):
        """Checks if someone has closed all numbers."""
        self.winner = player.name
        ## TODO Implement rules based winner declaration (Double out, Master out, etc...)

    def return_event(self, status) -> ThrowDartEvent:
        return ThrowDartEvent(
            position=self.current_player.position,
            name=self.current_player.name,
            score=self.current_player.score,
            darts=self.current_player.turn,
            status=status,
        )

    def throw_dart(self, dart: Dart):
        self.current_player = self.players[self.current_player_index]

        self.current_player.record_turn(
            score_before=self.current_player.score,
            score=dart.score,
            score_multiplier=dart.multiplier,
        )

        initial_score = self.current_player.score  # Store score before throwing

        points = dart.score * dart.multiplier
        self.current_player.score -= points

        # BUST LOGIC: If the score goes below 0, reset it to the initial score
        if self.current_player.score < 0:
            self.current_player.score = initial_score  # Reset due to bust
            return self.return_event(status="bust")

        # WIN CONDITION: Player must reach exactly 0
        if self.current_player.score == 0:
            self.check_winner(self.current_player)
            return self.return_event(status="win")

        # END TURN: Player must throw all darts then its next players turn
        if len(self.current_player.turn) == self.darts_per_player:
            self.current_player.end_turn()
            self.current_player_index += 1
            if self.current_player_index == len(self.players):
                self.current_player_index = 0

        return self.return_event(status="ok")


class CricketGame(GameMode):
    """Handles Cricket dart game logic."""

    def __init__(self):
        self.closed_numbers = {}

    def add_player(self, player_name: str):
        """Adds a player to the game."""
        self.players.append(CricketPlayer(player_name))
        self.closed_numbers[player_name] = {}

    def get_stats(self):
        stats = []

        for player in self.players:
            p_stats = {
                "starting_score": player.starting_score,
                "current_score": player.score,
                "turns": player.turns,
            }
            stats.append(p_stats)
        return stats

    def throw_dart(self, player, darts: list[dict[str, int]]):
        for dart in darts:
            num = dart["score"]
            multiplier = dart["multiplier"]

            if num not in self.closed_numbers[player.name]:
                self.closed_numbers[player.name][num] = 0

            self.closed_numbers[player.name][num] += multiplier  # Track hits

        player.record_turn(darts)
        self.check_winner()

    def check_winner(self):
        """Checks if someone has closed all numbers."""
        for player in self.players:
            if all(value >= 3 for value in self.closed_numbers[player.name].values()):
                return player
        return None
