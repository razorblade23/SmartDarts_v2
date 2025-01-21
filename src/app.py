import logging
from pathlib import Path

import markdown
from quart import Quart, render_template

from src.blueprints.dartboard.dartboard import dartboard_router

# Set up logger
logging.basicConfig(
    format="[%(levelname)s][%(name)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
    level=logging.DEBUG,
)

LOG = logging.getLogger(__name__)

app = Quart(__name__)

app.register_blueprint(dartboard_router, url_prefix="/dartboard")

app.secret_key = "your_secret_key"


@app.get("/")
async def index():
    with open(Path("./README.md"), "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    return await render_template("index.html", html=html)
