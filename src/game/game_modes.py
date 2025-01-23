from abc import ABC, abstractmethod

from .enums import OutRule
from .players import CricketPlayer, X01Player


class GameMode(ABC):
    """Base class for all dart game modes."""

    def __init__(self, players: list):
        self.players = players
        self.current_player_idx = 0

    @abstractmethod
    def throw_darts(self, player, darts: list[dict[str, int]]):
        """Handles dart throws, must be implemented by each game type."""
        pass

    @abstractmethod
    def check_winner(self):
        """Checks if the game is over."""
        pass

    def next_turn(self):
        """Moves to the next player."""
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)


class X01Game(GameMode):
    """Handles X01 dart game logic (301, 501, etc.)."""

    def __init__(
        self,
        players: list[X01Player],
        starting_score: int = 501,
        out_rule: OutRule = OutRule.SINGLE_OUT,
    ):
        super().__init__(players)
        self.starting_score = starting_score
        self.out_rule = out_rule
        self.players = players
        for player in self.players:
            player.score = starting_score

    def add_player(self, player_name: str):
        """Adds a player to the game."""
        self.players.append(X01Player(player_name, self.starting_score))

    def check_winner(self, player: X01Player):
        """Checks if someone has closed all numbers."""
        self.winner = player.name
        ## TODO Implement rules based winner declaration (Double out, Master out, etc...)

    def throw_darts(self, player: X01Player, darts: list[dict[str, int]]):
        initial_score = player.score  # Store score before throwing

        for dart in darts:
            points = dart["score"] * dart["multiplier"]
            player.score -= points

        # BUST LOGIC: If the score goes below 0, reset it to the initial score
        if player.score < 0:
            player.score = initial_score  # Reset due to bust
            return  # Bust, so turn ends immediately

        # WIN CONDITION: Player must reach exactly 0
        if player.score == 0:
            self.check_winner(player)


class CricketGame(GameMode):
    """Handles Cricket dart game logic."""

    def __init__(self, players: list[CricketPlayer]):
        super().__init__(players)
        self.closed_numbers = {player.name: {} for player in players}  # Track hits

    def add_player(self, player_name: str):
        """Adds a player to the game."""
        self.players.append(CricketPlayer(player_name))

    def throw_darts(self, player, darts: list[dict[str, int]]):
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
