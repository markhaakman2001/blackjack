from enum import Enum

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