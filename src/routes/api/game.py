from logging import getLogger

from flask import Blueprint, jsonify, request

from ...game_logic.enums import GameType
from ...game_logic.game_engine import DartgameManager

game_router = Blueprint(
    "game_api", __name__, template_folder="templates", static_folder="static"
)

LOG = getLogger(__name__)

games = {}


def game_id_in_games(game_id: str) -> bool:
    return game_id in games


def _no_game_id_found_error(game_id):
    return jsonify({"error": f"Game with {game_id=} not found"}), 404


@game_router.route("/create", methods=["GET", "POST"])
def new_game():
    data = request.json
    game_type = data.get("game_type")
    if not game_type:
        return jsonify({"error": "Game type missing from request"}), 403

    gametype = GameType(game_type)
    game_id = DartgameManager().create_game(gametype=gametype)

    return jsonify({"game_id": game_id, "message": "Game created successfully!"}), 201


@game_router.route("/<game_id>/add_player")
def add_player_to_game(game_id: str):
    data = request.json
    player_name = data.get("player_name")

    game = DartgameManager().get_game(game_id=game_id)
    if not game:
        LOG.error(f"No matching ID found: {game_id}")
        return _no_game_id_found_error(game_id)

    game.add_player(player_name)

    return jsonify({"message": f"Player {player_name} added to game {game_id}."}), 200


@game_router.route("/<game_id>/start", methods=["POST"])
def start_game(game_id: str):
    """Start the game."""

    game = DartgameManager().get_game(game_id=game_id)
    if not game:
        LOG.error(f"No matching ID found: {game_id}")
        return _no_game_id_found_error(game_id)

    game.start_game()

    return jsonify({"message": f"Game {game_id} started."}), 200


@game_router.route("/<game_id>/throw", methods=["POST"])
def throw_darts(game_id: str):
    """Handle dart throws."""
    data = request.json
    dart = data.get("dart")  # Example: {"score": 20, "multiplier": 2}
    LOG.debug(f"Throwing dart: {dart=}")

    game = DartgameManager().get_game(game_id=game_id)
    if not game:
        LOG.error(f"No matching ID found: {game_id}")
        return _no_game_id_found_error(game_id)

    try:
        game.throw_dart(dart)
    except Exception as e:
        LOG.error(e)
        return jsonify({"error": str(e)}), 400
    LOG.info(f"Throw {dart=} in game {game_id=}")

    current_player_stats = {
        "name": game.game.current_player.name,
        "current_score": game.game.current_player.score,
    }

    return jsonify({"status": current_player_stats}), 200


@game_router.route("/<game_id>", methods=["GET"])
def get_game_state(game_id: str):
    """Get the current state of the game."""
    game = DartgameManager().get_game(game_id=game_id)
    if not game:
        LOG.error(f"No matching ID found: {game_id}")
        return _no_game_id_found_error(game_id)

    state = game.get_game_state()
    return jsonify({"states": state}), 200
