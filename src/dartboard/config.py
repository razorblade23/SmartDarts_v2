import json


class DartboardConfigurator:
    """
    Configurator for GPIO scanning and mapping dartboard with actuall pins
    """

    def __init__(self, gpio_interface):
        self.gpio = gpio_interface
        self.columns = None
        self.rows = None
        self.matrix = {}

    def configure_gpio_pins(self, columns: list[int], rows: list[int]):
        pass

    def calibrate(self):
        print("Starting calibration mode. Follow the instructions.")
        dartboard_positions = [
            "D20",
            "S20",
            "T20",
            "D1",
            "S1",
            "T1",  # Example positions
        ]
        for position in dartboard_positions:
            print(f"Please hit the {position} on the dartboard.")
            input("Press Enter after hitting the dartboard...")

            # Detect the active column and row
            active_col = None
            active_row = None
            for col in self.columns:
                self.gpio.output(col, 1)
                for row in self.rows:
                    if self.gpio.input(row) == 1:
                        active_col = col
                        active_row = row
                        break
                self.gpio.output(col, 0)
                if active_col and active_row:
                    break

            if active_col is None or active_row is None:
                print(f"Failed to detect {position}. Try again.")
            else:
                print(f"Registered {position} at Col: {active_col}, Row: {active_row}")
                self.matrix[position] = {"col": active_col, "row": active_row}

    def save_configuration(self, filename: str):
        config = {"columns": self.columns, "rows": self.rows, "matrix": self.matrix}
        with open(filename, "w") as f:
            json.dump(config, f, indent=4)
        print(f"Configuration saved to {filename}")

    def load_configuration(self, filename: str):
        with open(filename, "r") as f:
            config = json.load(f)
        self.columns = config["columns"]
        self.rows = config["rows"]
        self.matrix = config["matrix"]
        print("Configuration loaded successfully.")


class Chinese7x10Config:
    """
    Configuration for a Chinese dartboard
    found at local sport shop (7x10 matrix).
    """

    @property
    def matrix(self) -> list[list[int]]:
        return [
            [7, 19, 3, 17, 15, 16, 8, 11, 14, 2],
            [1, 18, 4, 13, 10, 20, 5, 12, 9, 6],
            [7, 19, 3, 17, 15, 16, 8, 11, 14, 2],
            [1, 18, 4, 13, 10, 20, 5, 12, 9, 6],
            [7, 19, 3, 17, 15, 16, 8, 11, 14, 2],
            [1, 18, 4, 13, 10, 20, 5, 12, 9, 6],
            [7, 19, 3, 17, 15, 16, 8, 11, 14, 2],
        ]

    @property
    def col_pins(self) -> list[int]:
        return [5, 22, 10, 17, 9, 27, 11]

    @property
    def row_pins(self) -> list[int]:
        return [14, 15, 18, 23, 25, 8, 7, 12, 16, 24]

    @property
    def multiplier_pins(self) -> dict[int, list[int]]:
        return {1: [9, 22], 2: [11, 27], 3: [5, 17]}
