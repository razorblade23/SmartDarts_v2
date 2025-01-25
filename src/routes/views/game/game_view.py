from flask import Blueprint

game_view = Blueprint(
    "game_view", __name__, template_folder="templates", static_folder="static"
)


@game_view.route("/new_game")
def new_game():
    return "New Game"


@game_view.route("/play")
def play_game():
    return "Play Game"
