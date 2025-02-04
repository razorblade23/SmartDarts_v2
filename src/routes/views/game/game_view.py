from flask import Blueprint, Flask, redirect, render_template, request, session, url_for
from geventwebsocket.websocket import WebSocket

from ....game_logic.enums import GameType
from ....game_logic.game_engine import DartGameEngine, DartgameManager
from ....game_logic.players import Player

game_view = Blueprint(
    "game_view", __name__, template_folder="templates", static_folder="static"
)

game_view_ws = Blueprint("game_view_ws", __name__)


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


def render_player_tile(app: Flask, player: Player, player_position: int):
    with app.app_context():
        player_html = render_template(
            "x01/_player_tile.html",
            player=player,
            player_id=player_position,
        )
    return player_html


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
    print("Game started, spawning background tasks")

    return redirect(url_for(".playfield", game_id=game_id))


@game_view_ws.route("/player_update")
def socketio_send_player_update(socket: WebSocket):
    """Sends an update for a specific player's tile via WebSocket."""
    print("Sending player update")
    message = "New ws message"
    socket.send(message)
    # game_id = data["game_id"]
    # event: ThrowDartEvent = data["event"]
    # game = DartgameManager().get_game(game_id=game_id)

    # for player in game.game.players:
    #     if player.name == event.name:
    #         player_to_update = player

    # if player_to_update:
    #     player_html = render_template(
    #         "_player_tile.html", player=player_to_update, player_id=event.position
    #     )
    #     print(f"Sending player HTML to frontend: [{player_html=}]")
    #     # Emit only the updated player's tile to HTMX
    #     emit(
    #         "update_tile",
    #         {"player_id": event.position, "html": player_html},
    #         broadcast=True,
    #     )


@game_view.route("/playfield")
def playfield():
    game_id = request.args.get("game_id")
    print(f"Got {game_id=}")
    game = DartgameManager().get_game(game_id)
    print(f"Found: {game=}")
    return render_template(
        "x01/playfield.html", game_id=game_id, players=game.game.players
    )
