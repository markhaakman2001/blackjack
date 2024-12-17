from enum import Enum, auto

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

class ActionTypes(Enum):
    """DRAW or STAND (True or False)

    """    
    DRAW          = True
    STAND         = False
    NATURAL_STAND = None



banker3 = {0:ActionTypes.DRAW , 1:ActionTypes.DRAW, 2:ActionTypes.DRAW, 3:ActionTypes.DRAW, 4:ActionTypes.DRAW, 5:ActionTypes.DRAW, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.DRAW }
banker4 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.DRAW, 3:ActionTypes.DRAW, 4:ActionTypes.DRAW, 5:ActionTypes.DRAW, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }
banker5 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.STAND, 3:ActionTypes.STAND, 4:ActionTypes.DRAW, 5:ActionTypes.DRAW, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }
banker6 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.STAND, 3:ActionTypes.STAND, 4:ActionTypes.STAND, 5:ActionTypes.STAND, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }
banker7 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.STAND, 3:ActionTypes.STAND, 4:ActionTypes.STAND, 5:ActionTypes.STAND, 6:ActionTypes.STAND, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }

BankerActionDict = { 3: banker3, 4:banker4, 5:banker5 , 6:banker6, 7:banker7}

if __name__ == "__main__":
    print(BankerActionDict[3][8])