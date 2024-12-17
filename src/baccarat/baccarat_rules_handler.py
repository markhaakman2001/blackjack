import random
import numpy as np
from enum import Enum, auto


class PlayerType(Enum):
    """Defines if its a banker or player

    Args:
        Enum (_type_): _description_
    """    
    PLAYER = "Player"
    BANKER = "Banker"

class ActionState(Enum):
    """Used to track the current state of the game.
        PLAYERTURN means its the players turn to make a move
        BANKERTURN means its the bankers turn to make a move
        FINISHED means that all playertypes are done with their move.

    """    
    PLAYERTURN = auto()
    BANKERTURN = auto()
    FINISHED   = auto()
        
        

class OutComeTypes(Enum):

    BANKER = 0
    PLAYER = 1
    TIE    = 2


class ActionTypes(Enum):
    """DRAW or STAND (True or False)

    """    
    DRAW          = 0
    STAND         = 1
    NATURAL_STAND = 2


class SideBets(Enum):

    PLAYERPAIR = auto()
    BANKERPAIR = auto()






