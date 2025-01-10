from ..dartboard.board import Dartboard


class Game:
    def __init__(self):
        self.dartboard: Dartboard
        self.number_of_players = 0
        self.players = []
        self.rules = None
        self.unique_id = None
        self.game_status = {}
        self.log_to_console = True
        self.darts = []
        self.player_approached = False
        self.await_approach = False
        self.max_number_of_players = 8
        self.darts_per_round = 3
        self.game_status_history = []
        self.playoff_history = []
        self.playoff_started = False
        self.playoff_game = None
        self.is_playoff = False
