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
