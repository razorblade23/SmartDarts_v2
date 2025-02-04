from gevent.monkey import patch_all

patch_all()


# Turning off typechecking as it gives warning because of monkey_patch() running first
import json  # noqa: E402
import logging  # noqa: E402
from pathlib import Path  # noqa: E402
from queue import Empty  # noqa: E402

import markdown  # noqa: E402
from flask import Flask, render_template, request  # noqa: E402
from flask_sockets import Sockets  # noqa: E402
from gevent import sleep, spawn  # noqa: E402

from src.game_logic.game_engine import DartgameManager  # noqa: E402
from src.routes.api import api_router  # noqa: E402
from src.routes.views import views_router  # noqa: E402
from src.routes.views.game.game_view import (  # noqa: E402
    render_player_tile,
)

# Set up logger
logging.basicConfig(
    format="[%(levelname)s][%(name)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
    level=logging.DEBUG,
)

LOG = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "your_secret_key"
socket = Sockets(app)


app.register_blueprint(views_router)
app.register_blueprint(api_router, url_prefix="/api")


def game_event_listener(game_id: str):
    print("Started game listener")
    game = DartgameManager().get_game(game_id)
    while True:
        try:
            event = game.events.get()
        except Empty:
            sleep(2)
            continue

        game = DartgameManager().get_game(game_id=game_id)

        for player in game.game.players:
            if player.name == event.name:
                player_to_update = player

        if player_to_update:
            player_html = render_player_tile(
                app=app, player=player_to_update, player_position=event.position
            )
            print(f"Sending player HTML to frontend: [{player_html=}]")
            # Emit only the updated player's tile to HTMX
            socket.send(json.dumps({"player_id": event.position, "html": player_html}))
        sleep(2)


@app.get("/utils/start_game_listener")
def start_game_listener():
    game_id = request.args.get("game_id")
    if game_id:
        spawn(game_event_listener, game_id=game_id)
        return {"status": "running"}
    return {"status": "no game id"}


@app.get("/")
def index():
    with open(Path("./README.md"), "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    return render_template("index.html", html=html)


# <div class="col-4 text-center border border-secondary pt-2 m-1">
#     <div class="row">
#         <div class="col-12 border-end border-secondary">
#             <h6>1</h6>
#             <h6>Glavan</h6>
#         </div>
#         <div class="col-12">
#             <h1>140</h1>
#         </div>
#     </div>
# </div>
