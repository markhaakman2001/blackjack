from enum import Enum, auto

class GameState(Enum):

    INACTIVE = 0
    ACTIVE   = 1

class GameType(Enum):

    BLACKJACK   = "blackjack"
    BACCARAT    = "baccarat"
    SLOTMACHINE = "slotmachine"
    MINES       = "mines"