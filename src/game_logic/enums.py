from enum import Enum


class GameType(Enum):
    """Enum for different game types."""

    X01 = "X01"
    CRICKET = "Cricket"


class X01Mode(Enum):
    """Enum for different X01 game modes."""

    STANDARD = "standard"
    PARCHESSI = "parchessi"
    HIT_AND_RUN = "hit_and_run"


class OutRule(Enum):
    """Enum for X01 checkout rules."""

    SINGLE_OUT = "single_out"
    DOUBLE_OUT = "double_out"
    MASTER_OUT = "master_out"
    DOUBLE_IN = "double_in"


class CricketMode(Enum):
    """Enum for different Cricket game modes."""

    STANDARD = "standard"
    PICK_IT = "pick_it"
    RANDOM = "random"
