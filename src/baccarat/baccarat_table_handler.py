import numpy as np
import random
from enum import Enum, auto
from src.baccarat.baccarat_cards import Shoe, Card
#from src.baccarat.baccarat_rules_handler import BaccaratRules, ActionTypes
from PySide6.QtCore import Slot, Signal, QObject


class PlayerType(Enum):
    PLAYER = "Player"
    BANKER = "Banker"

class ActionState(Enum):
    PLAYERTURN = auto()
    BANKERTURN = auto()
    FINISHED   = auto()


# class ActionTypes(Enum):

#     DRAW  = True
#     STAND = False



class PlayerBanker:

    def __init__(self, type : PlayerType):
        self.playertype : PlayerType = type
        self.cards_list : list[Card] = []
        self.total_value : int       = 0
        self.total_points            = None
    
    def AddCard(self, card: Card) -> None:
        """Add a card to the player or bankers cards and update the list and total values
        
        Args:
            card (Card): The card that was dealt.
        """        
        self.cards_list.append(card)
        self.card_value = card._get_value()
        self.total_value += self.card_value
        self.CalculatePoints()

    def CalculatePoints(self):
        """Calculates the points of the player/banker based on the baccarat rules.
        """
        if self.total_value <= 9:
            self.total_points = self.total_value
            return self.total_points
        else:
            self.total_value -= 10
            self.CalculatePoints()


class BaccaratTable(QObject):

    ValuesChanged = Signal(PlayerType, name="ValuesChanged")
    PointsChanged = Signal(PlayerType, name="PointsChanged")

    def __init__(self):
        super().__init__()
        self.shoe         = Shoe(ndecks=8)
        self.player       = PlayerBanker(PlayerType.PLAYER)
        self.banker       = PlayerBanker(PlayerType.BANKER)
        self.CurrentState = ActionState.PLAYERTURN

        self.player_cards : list[Card] = self.player.cards_list
        self.banker_cards : list[Card] = self.banker.cards_list
        self.ValuesChanged.connect(self.PointsChange)
    

    @Slot(PlayerType)
    def PointsChange(self, signal):
        if signal == PlayerType.PLAYER:
            if self.player_cards[-1]._get_value() != 10:
                self.PointsChanged.emit(PlayerType.PLAYER)
        else:
            if self.banker_cards[-1]._get_value() != 10:
                self.PointsChanged.emit(PlayerType.BANKER)
    
    
    def PlaceFirstCards(self) -> tuple[list[Card], list[Card]]:
        
        new_cards : list[Card] = self.shoe.getcard(n_cards=4)

        for i, card in enumerate(new_cards):
            if i in [0, 2]:
                self.player.AddCard(card)
                print(card._get_CardName(), card._get_value())
                self.ValuesChanged.emit(PlayerType.PLAYER)
            else:
                self.banker.AddCard(card)
                print(card._get_CardName(), card._get_value())
                self.ValuesChanged.emit(PlayerType.BANKER)
        
        print(self.player.CalculatePoints())
        print(self.banker.CalculatePoints())
        self.WhatNext()
        return self.player_cards, self.banker_cards

    def WhatNext(self):
        print(BaccaratRules.NextMove(self))

class OutComeTypes(Enum):

    BANKER = 0
    PLAYER = 1
    TIE    = 2


class ActionTypes(Enum):

    DRAW  = True
    STAND = False


class SideBets(Enum):

    PLAYERPAIR = auto()
    BANKERPAIR = auto()



class BaccaratRules(BaccaratTable):

    def __init__(self):
        super().__init__()
    

    def NextMove(self):
        if self.CurrentState == ActionState.PLAYERTURN:
            points = self.player.CalculatePoints()
        return True if points <= 5 else False





if __name__ == "__main__":

    table = BaccaratTable()
    results = table.PlaceFirstCards()
    results2 = BaccaratTable.PlaceFirstCards(table)
    print(results2)
    print(results)



