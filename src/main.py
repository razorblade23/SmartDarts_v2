import asyncio

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO

from dartboard.config import Chinese7x10Config
from SBC.gpio_handlers.mock_handler import MockGPIOHandler
from src.dartboard.board import Dartboard

dartboard = Dartboard(gpio_handler=MockGPIOHandler(), config=Chinese7x10Config())

app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/play")
def play():
    """Serve the dartboard visualization."""
    return render_template("dartboard.html")


@app.get("/hit")
def hit():
    data = {"segment": 20}
    current_hit = {
        "segment": data.get("segment"),
        "ring": data.get("ring"),
    }
    # GET: Return the current hit data
    return jsonify(current_hit)


if __name__ == "__main__":
    # Create asyncio event loop
    loop = asyncio.get_event_loop()
    loop.create_task(dartboard.run_matrix_scan_until_hit())
    socketio.run(app, debug=True)
