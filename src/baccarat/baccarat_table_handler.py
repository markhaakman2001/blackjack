import numpy as np
import random
from enum import Enum, auto
from src.extrafiles.labels import Shoe, DeckOfCards


class PlayerType(Enum):
    PLAYER = "player"
    BANKER = "banker"



class Player:

    def __init__(self, type:PlayerType):
        self.playertype = type
        self.cards      = []
        self.card_total = 0
    
    def AddCard(self, card):
        self.cards.append(card)
    
    def CalculateHandValue(self):
        



class Table:

    def __init__(self):
        self.player       = Player(PlayerType.PLAYER)
        self.banker       = Player(PlayerType.BANKER)
        self.player_cards = []
        self.banker_cards = []
        self.shoe         = Shoe(ndecks=8)
        

