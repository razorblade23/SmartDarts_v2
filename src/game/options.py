from enum import Enum, auto


class ThrowOption(Enum):
    DOUBLE_IN = auto()
    SINGLE_OUT = auto()
    DOUBLE_OUT = auto()
    MASTER_OUT = auto()


class TeamOption(Enum):
    NO_OPTION = auto()
    PAIR = auto()
    TEAM = auto()
