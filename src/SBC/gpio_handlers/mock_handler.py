class MockGPIOHandler:
    def __init__(self):
        self.pin_states = {}
        self.input_pins = set()

    def setup_output(self, pin: int):
        self.pin_states[pin] = 0

    def setup_input(self, pin: int):
        self.input_pins.add(pin)
        self.pin_states[pin] = 0

    def set_pin_high(self, pin: int):
        self.pin_states[pin] = 1

    def set_pin_low(self, pin: int):
        self.pin_states[pin] = 0

    def read_pin(self, pin: int) -> bool:
        if pin not in self.input_pins:
            raise RuntimeError(f"Pin {pin} is not configured as input.")
        return self.pin_states[pin] == 1

    # Additional helper methods for testing
    def simulate_pin_high(self, pin: int):
        if pin not in self.input_pins:
            raise RuntimeError(
                f"Cannot simulate input on pin {pin} not configured as input."
            )
        self.pin_states[pin] = 1

    def simulate_pin_low(self, pin: int):
        if pin not in self.input_pins:
            raise RuntimeError(
                f"Cannot simulate input on pin {pin} not configured as input."
            )
        self.pin_states[pin] = 0
