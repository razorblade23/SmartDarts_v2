import json
from logging import getLogger

from quart import Blueprint, render_template, request, session

from ...dartboard.config import DartboardConfig, DartboardConfigurator
from ...SBC.gpio_handlers.mock_handler import MockGPIOHandler

configurator_router = Blueprint("configurator", __name__)

LOG = getLogger(__name__)


@configurator_router.before_request
def load_session_configurator():
    """Load configurator from session before each request."""
    global configurator
    configurator = DartboardConfigurator(MockGPIOHandler())
    LOG.debug("Loaded configurator")
    config_data = session.get("dartboard_config")
    if config_data:
        config = DartboardConfig(**config_data)
        configurator.set_dartboard_config(dartboard_config=config)
        LOG.debug("Loaded configurator dartboard configuration data from session")


@configurator_router.route("/")
async def configurator_index():
    if configurator.config:
        dartboard_name = configurator.config.name
        configurator_status = "Not configured"
    else:
        dartboard_name = "Not configured"
        configurator_status = "Not configured"
    return await render_template(
        "dartboard_index.html",
        dartboard_name=dartboard_name,
        configurator_status=configurator_status,
    )


@configurator_router.post("/load_configurator")
async def load_configurator():
    form_data: dict = await request.json
    print(type(form_data), form_data)
    dartboard_name = form_data.get("dartboardName")
    dartboard_columns = form_data.get("columns")
    dartboard_rows = form_data.get("rows")

    # Check to see if all the paramethers are there
    if any([not dartboard_name, not dartboard_columns, not dartboard_rows]):
        return json.dumps(
            {
                "status": "failed",
                "dartboard_name": dartboard_name,
                "reason": "Wrong paramethers",
            }
        )

    LOG.debug("Resseting DartboardConfigurator")
    configurator = DartboardConfigurator(MockGPIOHandler())
    session["dartboard_config"] = None

    # Set up configurator
    config = DartboardConfig(
        name=dartboard_name, rows=dartboard_rows, cols=dartboard_columns
    )
    configurator.set_dartboard_config(config)
    configurator.save_configuration_to_session(session=session)
    return json.dumps({"status": "started", "dartboard_name": dartboard_name})


@configurator_router.route("/calibrate")
def calibrate_step():
    result = configurator.calibrate_step()
    configurator.save_configuration_to_session(session)
    if result is None:
        return json.dumps({"status": "complete"})
    return json.dumps(result)
