from pydantic import BaseModel, Field
from logging import getLogger
from ..SBC._protocol import GPIOInterface


LOG = getLogger(__name__)

class DartboardConfig(BaseModel):
    name: str
    matrix: dict[int, dict[str, int]] = Field(default_factory=dict)
    rows: list[int] = Field(default_factory=list)
    cols: list[int] = Field(default_factory=list)


def new_board_config(name: str, cols: list[int], rows: list[int]) -> DartboardConfig:
    config = DartboardConfig(name=name, rows=rows, cols=cols)
    return config


class DartboardConfigurator:
    """
    Configurator for GPIO scanning and mapping dartboard with actual pins
    """

    def __init__(self, gpio_interface: GPIOInterface) -> None:
        self.gpio: GPIOInterface = gpio_interface
        self.config = None
        self.current_position_index = 0

    def set_dartboard_config(self, dartboard_config: DartboardConfig) -> None:
        self.config = dartboard_config
        self._setup_pins()
        LOG.debug("Setup pins complete")

    def _setup_pins(self) -> None:
        for col in self.config.cols:
            self.gpio.setup_output(col)
        for row in self.config.rows:
            self.gpio.setup_input(row)

    def calibrate_step(self) -> dict[str, str | int] | None:
        if self.current_position_index >= len(self._dartboard_positions):
            return None  # Calibration complete

        active_col, active_row = self._detect_position()

        if active_col is None or active_row is None:
            return {"status": "failed", "position": self._current_position}
        else:
            self.config.matrix[self._current_position] = {
                "col": active_col,
                "row": active_row,
            }
            self.current_position_index += 1
            return {
                "status": "success",
                "position": self._current_position,
                "col": active_col,
                "row": active_row,
            }

    @property
    def _dartboard_positions(self) -> list[int]:
        return [x for x in range(1, 21)] + [25]

    @property
    def _current_position(self) -> int:
        if self.current_position_index < len(self._dartboard_positions):
            return self._dartboard_positions[self.current_position_index]
        return None  # Prevent out-of-range errors

    def _detect_position(self) -> tuple[int | None, int | None]:
        active_col = None
        active_row = None
        for col in self.config.cols:
            self.gpio.set_pin_high(col)
            for row in self.config.rows:

                if self.gpio.read_pin(row):
                    active_col = col
                    active_row = row
                    break
            self.gpio.set_pin_low(col)
            if active_col and active_row:
                break
        return active_col, active_row

    def save_configuration_to_session(self, session: dict) -> None:
        session["dartboard_config"] = self.config.model_dump()
        session["dartboard_config"]["current_position_index"] = (
            self.current_position_index
        )

    def load_from_session(self, session: dict):
        config = session.get("dartboard_config", None)
        if config:
            conf = DartboardConfig(**config)
            self.config = conf
            self.current_position_index = config["current_position_index"]

    def reset_session(self, session: dict) -> None:
        session["dartboard_config"] = None
