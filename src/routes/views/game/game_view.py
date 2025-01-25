from flask import Blueprint, render_template, request

game_view = Blueprint(
    "game_view", __name__, template_folder="templates", static_folder="static"
)


@game_view.route("/new_game/<game_type>")
def new_game(game_type: str):
    ## TODO Replace with Enum
    if game_type == "x01":
        return render_template("new_X01_game.html")


@game_view.post("/add_player")
def add_player():
    player_name = request.form.get("playerName")
    return render_template("_player_ready.html", player_name=player_name)


@game_view.route("/play")
def play_game():
    return "Play Game"
