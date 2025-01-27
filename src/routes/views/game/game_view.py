from flask import Blueprint, redirect, render_template, request, session, url_for

from ....game_logic.enums import GameType
from ....game_logic.game_engine import DartGameEngine, DartgameManager

game_view = Blueprint(
    "game_view", __name__, template_folder="templates", static_folder="static"
)


@game_view.route("/new_game/<game_type>")
def new_game(game_type: str):
    gametype = GameType(game_type.title())

    match gametype:
        case GameType.X01:
            session["game_type"] = gametype.value
            return render_template("x01/new_game.html")


@game_view.post("/add_player")
def add_player():
    player_name = request.form.get("playerName")
    return render_template("_player_ready.html", player_name=player_name)


@game_view.post("/start")
def start_game():
    data = request.get_json()

    gametype = session.get("game_type")
    game_mode = data.get("game_mode")
    starting_score = data.get("starting_score")
    players = data.get("players")

    print(f"{gametype=} {game_mode=} {starting_score=} {players=}", flush=True)

    game_id = DartgameManager().create_game(
        gametype=GameType(gametype.title()), starting_score=int(starting_score)
    )
    session["gameID"] = game_id
    game: DartGameEngine | None = DartgameManager().get_game(game_id)
    if not game:
        raise RuntimeError("No game set")

    for player in players:
        game.add_player(player)

    game.start_game()

    return redirect(url_for(".playfield", game_id=game_id))


@game_view.route("/playfield")
def playfield():
    game_id = request.args.get("game_id")
    game = DartgameManager().get_game(game_id)
    return render_template(
        "x01/playfield.html", game_id=game_id, players=game.game.players
    )
