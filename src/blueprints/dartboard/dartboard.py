from logging import getLogger

from quart import Blueprint

from .configurator import configurator_router

LOG = getLogger(__name__)

dartboard_router = Blueprint(
    "dartboard", __name__, template_folder="templates", static_folder="static"
)

dartboard_router.register_blueprint(configurator_router, url_prefix="/configurator")
