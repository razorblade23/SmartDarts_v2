from flask import Blueprint

from .game import game_router

api_router = Blueprint("api", __name__)

api_router.register_blueprint(game_router, url_prefix="/game")
