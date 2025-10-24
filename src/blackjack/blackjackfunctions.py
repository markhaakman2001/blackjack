from enum import Enum, auto


class UpdateType(Enum):
    POINTS     = auto()
    NEXTHAND   = auto()
    DEALERTURN = auto()