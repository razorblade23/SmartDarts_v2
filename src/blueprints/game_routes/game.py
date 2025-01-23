from uuid import uuid4

from flask import Blueprint, abort, jsonify, request

from ...game.enums import GameType
from ...game.game_engine import DartGameEngine

game_router = Blueprint(
    "game", __name__, template_folder="templates", static_folder="static"
)

games = {}


@game_router.route("/create", methods=["GET", "POST"])
def new_game():
    data = request.json
    game_type = data.get("game_type")
    if not game_type:
        abort(403)

    gametype = GameType(game_type)

    game_id = str(uuid4())
    games[game_id] = {
        "engine": DartGameEngine(game_type=gametype, players=[]),
        "players": [],
    }

    return jsonify({"game_id": game_id, "message": "Game created successfully!"}), 201


@game_router.route("/str:<game_id>/add_player")
def add_player_to_game(game_id: str):
    data = request.json
    player_name = data.get("player_name")

    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game = games[game_id]
    game["players"].append(player_name)
    game["engine"].add_player(player_name)

    return jsonify({"message": f"Player {player_name} added to game {game_id}."}), 200


@game_router.route("/str:<game_id>/start", methods=["POST"])
def start_game(game_id: str):
    """Start the game."""

    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game = games[game_id]
    game["engine"].start_game()

    return jsonify({"message": f"Game {game_id} started."}), 200


@game_router.route("/str:<game_id>/throw", methods=["POST"])
def throw_darts(game_id: str):
    """Handle dart throws."""
    data = request.json
    player_name = data.get("player_name")
    darts = data.get("darts")  # Example: [{"score": 20, "multiplier": 2}, ...]

    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game = games[game_id]

    try:
        game["engine"].throw_darts(player_name, darts)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    ## TODO Return actuall state of the game
    return jsonify(
        {"message": f"Player {player_name} threw darts.", "state": True}
    ), 200


@game_router.route("/str:<game_id>", methods=["GET"])
def get_game_state(game_id: str):
    """Get the current state of the game."""
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game = games[game_id]
    ## TODO Return actuall state of the game
    return jsonify({"state": True}), 200
