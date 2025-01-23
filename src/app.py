import logging
from pathlib import Path

import markdown
from flask import Flask, render_template

from src.blueprints.dartboard.dartboard import dartboard_router
from src.blueprints.game_routes.game import game_router

# Set up logger
logging.basicConfig(
    format="[%(levelname)s][%(name)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
    level=logging.DEBUG,
)

LOG = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "your_secret_key"


app.register_blueprint(dartboard_router, url_prefix="/dartboard")
app.register_blueprint(game_router, url_prefix="/game")


@app.get("/")
def index():
    with open(Path("./README.md"), "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    return render_template("index.html", html=html)
