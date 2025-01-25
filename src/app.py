import logging
from pathlib import Path

import markdown
from flask import Flask, render_template

from src.routes.api import api_router
from src.routes.views import views_router

# Set up logger
logging.basicConfig(
    format="[%(levelname)s][%(name)s|%(module)s|L%(lineno)d] %(asctime)s: %(message)s",
    level=logging.DEBUG,
)

LOG = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "your_secret_key"


app.register_blueprint(views_router)
app.register_blueprint(api_router, url_prefix="/api")


@app.get("/")
def index():
    with open(Path("./README.md"), "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    return render_template("index.html", html=html)
