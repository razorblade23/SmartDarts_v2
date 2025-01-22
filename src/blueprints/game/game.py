from flask import Blueprint, abort, request

from ...game.enums import GameType
from ...game.game_engine import DartGameEngine

game_router = Blueprint(
    "game", __name__, template_folder="templates", static_folder="static"
)


@game_router.route("/create", methods=["GET", "POST"])
def new_game():
    data = request.json
    game_type = data.get("game_type")
    if not game_type:
        abort(403)

    gametype = GameType(game_type)

    dartgame = DartGameEngine(
        game_type=gametype,
    )
