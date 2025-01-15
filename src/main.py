from pathlib import Path

import markdown
from quart import Quart, jsonify, render_template

from src.dartboard.board import Dartboard
from src.dartboard.config import Chinese7x10Config
from src.SBC.gpio_handlers.mock_handler import MockGPIOHandler

dartboard = Dartboard(gpio_handler=MockGPIOHandler(), config=Chinese7x10Config())

app = Quart(__name__)


@app.get("/")
async def index():
    with open(Path("./README.md"), "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    return await render_template("index.html", html=html)


@app.get("/play")
async def play():
    """Serve the dartboard visualization."""
    return await render_template("dartboard.html")


@app.get("/hit")
async def hit():
    data = {"segment": 19}
    current_hit = {
        "segment": data.get("segment"),
        "ring": data.get("ring"),
    }
    # GET: Return the current hit data
    return await jsonify(current_hit)
