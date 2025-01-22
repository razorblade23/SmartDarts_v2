from .enums import CricketMode, OutRule, X01Mode
from .players import CricketPlayer, X01Player


class X01GameState:
    """Manages the state of the game (turns, players, rules)."""

    def __init__(self, game_mode: X01Mode, starting_score: int, out_rule: OutRule):
        self.players: list[X01Player] = []
        self.turn_index = 0
        self.game_mode = game_mode
        self.starting_score = starting_score
        self.out_rule = out_rule
        self.winner: str | None = None

    def add_player(self, player_name: str):
        """Adds a player to the game."""
        self.players.append(X01Player(player_name, self.starting_score))

    def next_turn(self):
        """Moves to the next player's turn."""
        self.turn_index = (self.turn_index + 1) % len(self.players)

    def check_winner(self, player: X01Player):
        """Checks if a player has won based on the game rules."""
        if player.score == 0:
            if self.out_rule == "Double Out":
                if self._is_double_out_valid(player):
                    self.winner = player.name
            else:
                self.winner = player.name

    def _is_double_out_valid(self, player: X01Player):
        """Implements the 'Double Out' rule check."""
        # In reality, we'd need to track last dart thrown, but this is a placeholder
        return True


class CricketGameState:
    """Manages the state of a Cricket game (players, turns, and rules)."""

    def __init__(self, game_mode: CricketMode):
        self.players: list[CricketPlayer] = []
        self.turn_index = 0
        self.game_mode = game_mode
        self.winner: str | None = None

    def add_player(self, player_name: str):
        """Adds a player to the game."""
        self.players.append(CricketPlayer(player_name))

    def next_turn(self):
        """Moves to the next player's turn."""
        self.turn_index = (self.turn_index + 1) % len(self.players)

    def check_winner(self):
        """Determines if a player has won."""
        for player in self.players:
            if all(player.is_closed(num) for num in range(15, 21)) and player.is_closed(
                25
            ):
                # Player must have the highest score to win
                if player.score >= max(p.score for p in self.players):
                    self.winner = player.name
