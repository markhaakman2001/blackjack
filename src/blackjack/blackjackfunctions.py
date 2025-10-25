from enum import Enum, auto


class UpdateType(Enum):
    POINTS     = auto()
    NEXTHAND   = auto()
    DEALERTURN = auto()
    RESULT     = auto()

class WinFunctions:

    def __init__(self, function):
        self.function = function
    
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

class WinType(Enum):

    BLACKJACK = WinFunctions(lambda x: x * 2.5)
    LOSE      = WinFunctions(lambda x: x * 0  )
    PUSH      = WinFunctions(lambda x: x * 1  )
    WIN       = WinFunctions(lambda x: x * 2  )