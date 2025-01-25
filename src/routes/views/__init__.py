from flask import Blueprint

from .dartboard_conf_view.dartboard_view import dartboard_router
from .game.game_view import game_view

views_router = Blueprint("views", __name__)

views_router.register_blueprint(dartboard_router, url_prefix="/dartboard")
views_router.register_blueprint(game_view, url_prefix="/game")
