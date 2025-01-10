from asyncio import Queue
from asyncio import sleep as async_sleep

from ..SBC._protocol import GPIOInterface
from ._protocol import DartboardConfig


class Dartboard:
    def __init__(self, gpio_handler: GPIOInterface, config: DartboardConfig):
        self.gpio = gpio_handler
        self.matrix = config.matrix
        self.col_pins = config.col_pins
        self.row_pins = config.row_pins
        self.multipliers = config.multiplier_pins
        self.result_queve = Queue()
        self._setup_pins()

    def _setup_pins(self):
        for col in self.col_pins:
            self.gpio.setup_output(col)
        for row in self.row_pins:
            self.gpio.setup_input(row)

    async def _scan_matrix(self) -> tuple[int, int] | None:
        for col_index, col_pin in enumerate(self.col_pins):
            self.gpio.set_pin_high(col_pin)
            for row_index, row_pin in enumerate(self.row_pins):
                if self.gpio.read_pin(row_pin):
                    hit_index = (col_index * len(self.row_pins)) + row_index
                    hit_value = self.matrix[hit_index]
                    multiplier = self.detect_multiplier()
                    if hit_value and multiplier:
                        return hit_value, multiplier
                    async_sleep(self.gpio.DEBOUNCE_TIME)
            self.gpio.set_pin_low(col_pin)
        return None

    async def run_matrix_scan_until_hit(self):
        while True:
            result = await self._scan_matrix()

            if result:
                value, multiplier = result
                self.result_queve.put({"value": value, "multiplier": multiplier})
                break

    def detect_multiplier(self) -> int:
        for multiplier, pins in self.multipliers.items():
            if any(self.gpio.read_pin(pin) for pin in pins):
                return multiplier
        return 0
