from .enums import CricketMode, GameType, OutRule, X01Mode
from .states import CricketGameState, X01GameState


class DartGameEngine:
    """Main game engine that manages the game session."""

    def __init__(self, game_type: str, **kwargs):
        """
        Initializes a game session.
        game_type: str from flasks route
        kwargs: Additional game options (mode, out rule, etc.)
        """

        self.game_type = GameType(game_type)

        match self.game_type:
            case GameType.X01:
                self.state = X01GameState(
                    game_mode=kwargs.get("game_mode", X01Mode.STANDARD),
                    starting_score=kwargs.get("starting_score", 501),
                    out_rule=kwargs.get("out_rule", OutRule.SINGLE_OUT),
                )
            case GameType.CRICKET:
                self.state = CricketGameState(
                    kwargs.get("game_mode", CricketMode.STANDARD)
                )

            # Other game types go here where we initialize the game session

    def add_player(self, name: str):
        """Registers a new player to the game."""
        self.state.add_player(name)

    def throw_darts(self, player_name: str, darts: list[dict[str, int]]):
        """
        Simulates throwing darts.
        Example: darts = [{"score": 20, "multiplier": 2}, {"score": 19, "multiplier": 3}, {"score": 25, "multiplier": 1}]
        """
        player = next(p for p in self.state.players if p.name == player_name)

        score_before = player.score
        for dart in darts:
            points = dart["score"] * dart["multiplier"]
            player.score -= points

            # Prevent negative score (bust)
            if player.score < 0:
                player.score = score_before  # Revert to previous score
                break

        player.record_turn(score_before, darts)
        self.state.check_winner(player)
        self.state.next_turn()

    def is_game_over(self):
        """Checks if the game has ended."""
        return self.state.winner is not None

    def get_winner(self):
        """Returns the winner's name."""
        return self.state.winner

    def save_to_database(self, db_session):
        """Saves game results to the database once the game ends."""
        if not self.is_game_over():
            return

        from models import GameSession, Player, Turn  # Import models dynamically

        game_session = GameSession(
            game_mode_id=1,  # Placeholder, should be dynamic
            status="completed",
        )
        db_session.add(game_session)
        db_session.commit()

        for player in self.state.players:
            db_player = db_session.query(Player).filter_by(name=player.name).first()
            if not db_player:
                db_player = Player(name=player.name)
                db_session.add(db_player)
                db_session.commit()

            for turn in player.turns:
                turn_entry = Turn(
                    session_id=game_session.id,
                    player_id=db_player.id,
                    score_before=turn["score_before"],
                    score_after=turn["score_after"],
                    darts_hit=turn["darts"],
                )
                db_session.add(turn_entry)

        db_session.commit()
