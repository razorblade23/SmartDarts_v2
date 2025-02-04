try:
    import RPi.GPIO as GPIO
except ImportError:
    pass


class RPiGPIOHandler:
    DEBOUNCE_TIME = 0.7

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def setup_output(self, pin: int):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

    def setup_input(self, pin: int):
        GPIO.setup(pin, GPIO.IN)

    def set_pin_high(self, pin: int):
        GPIO.output(pin, 1)

    def set_pin_low(self, pin: int):
        GPIO.output(pin, 0)

    def is_pin_high(self, pin: int) -> bool:
        return GPIO.input(pin) == GPIO.HIGH
