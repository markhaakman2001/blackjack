import numpy as np
import random
from enum import Enum, auto
from src.baccarat.baccarat_cards import Shoe, Card


class PlayerType(Enum):
    PLAYER = "Player"
    BANKER = "Banker"



class PlayerBanker:

    def __init__(self, type : PlayerType):
        self.playertype : PlayerType = type
        self.cards_list : list[Card] = []
        self.total_value : int       = 0
    
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
        else:
            self.total_value -= 10
            self.CalculatePoints()


class BaccaratTable:

    def __init__(self):
        self.shoe         = Shoe(ndecks=8)
        self.player       = PlayerBanker(PlayerType.PLAYER)
        self.banker       = PlayerBanker(PlayerType.BANKER)

        self.player_cards : list[Card] = self.player.cards_list
        self.banker_cards : list[Card] = self.banker.cards_list
    
    def PlayOneRound(self) -> tuple[list[Card], list[Card]]:
        
        new_cards : list[Card] = self.shoe.getcard(n_cards=4)

        for i, card in enumerate(new_cards):
            if i in [0, 2]:
                self.player.AddCard(card)
                print(card._get_CardName(), card._get_value())
            else:
                self.banker.AddCard(card)
                print(card._get_CardName(), card._get_value())
        
        return self.player_cards, self.banker_cards


if __name__ == "__main__":

    table = BaccaratTable()
    results = table.PlayOneRound()
    print(results)


