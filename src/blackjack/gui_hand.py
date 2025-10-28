from baccarat.baccarat_cards import Card, CardSymbol, DeckOfCards, Shoe, Kind, Color
from enum import Enum, auto
from blackjack.blackjackfunctions import WinType, WinFunctions

class Origin(Enum):

    ORIGINAL  = 0
    SPLITHAND = 1

class BlackJackHand:

    def __init__(self, hand_number):
        self.cards : list[Card] = []
        self._SoftHand          = False
        self._is_active         = True
        self.origin             = Origin.ORIGINAL
        self.hand_number        = hand_number
    
    def AddCard(self, card : Card) -> None:
        """
        Add a card to the hand

        Args:
            card (Card): The card that is added to the hand
        """        
        self.cards.append(card)

        if card._is_ace():
            self._SoftHand = True
    
    def DealerTurn(self) -> bool:
        """
        Dealer hits card if total is under 17.
        Dealer also hits on soft 17.

        Returns:
            bool: True if dealer should hit. False if dealer should stand
        """        
        total      = self._TotalValue
        if total >= 17:
            return False
        else:
            return True
    
    def final_result(self, dealer_hand : "BlackJackHand") -> WinType:

        if self._is_bust():
            return WinType.LOSE

        elif dealer_hand._is_blackjack():
            if self._is_blackjack():
                return WinType.PUSH
            else:
                return WinType.LOSE

        elif self._is_blackjack():
            return WinType.BLACKJACK
        
        else:
            dealer_total = dealer_hand._get_handtotal()
            hand_total   = self._get_handtotal()
            if dealer_total > 21:
                return WinType.WIN
            else:
                if dealer_total > hand_total:
                    return WinType.LOSE
                elif dealer_total == hand_total:
                    return WinType.PUSH
                else:
                    return WinType.WIN
            
    
    def _is_blackjack(self):
        """
        Check if hand has blackjack

        Returns:
            bool: True if the hand is a blackjack, false otherwise
        """        
        return self._BlackJack

    def _get_handtotal(self) -> int:
        """
        calculates the total point value of the hand.

        Returns:
            int: total value of the hand
        """        
        return self._TotalValue

    def _is_bust(self) -> bool:
        """
        player bust if total hand value is over 21

        Returns:
            bool: True if its a bust. False otherwise
        """        
        if self._TotalValue > 21:
            return True
        else:
            return False

    def deactivate(self):
        self._is_active = False


    # @property
    # def _split_index_(self):
    #     return self._split_number_
    
    # @_split_index_.setter
    # def _split_index_(self, num : int):
    #     self._split_number_ = num

    # @property
    # def _is_splithand_(self):
    #     return self.__split__
    
    # @_is_splithand_.setter
    # def _is_splithand_(self, split: tuple[bool, int]):
    #     self.__split__ = split[0]
    #     if split[0]:
    #         self._split_index_ = split[1]

    @property
    def origin(self):
        return self._origin_
    
    @origin.setter
    def origin(self, origin : Origin):
        self._origin_ = origin

    @property
    def _BlackJack(self):
        return (len(self.cards) == 2) and (self._TotalValue == 21)
    
    @property
    def _SoftHand(self):
        return self._SoftHand_
    
    @_SoftHand.setter
    def _SoftHand(self, soft : bool):
        self._SoftHand_ = soft
    
    @property
    def _TotalValue(self) -> int:

        self._TotalValue_ = sum([card._get_value() for card in self.cards])

        if self._SoftHand and self._TotalValue_ > 21:
            self._TotalValue_ = self._SoftTotal
        
        return self._TotalValue_
    

    @property
    def _SoftTotal(self):
        if self._SoftHand:
            self._SoftTotal_ = self._TotalValue_
            for card in self.cards:
                if card._is_ace():
                    self._SoftTotal_ -= 10
        else:
            self._SoftTotal_ = 0
        return self._SoftTotal_

    @property
    def _is_active(self):
        return self._is_active_

    @_is_active.setter
    def _is_active(self, active : bool):
        self._is_active_ = active      
    

class BlackJackSplitHand(BlackJackHand):

    def __init__(self, hand_number, card1 : Card, newcard : Card, left_hand: bool):
        super().__init__(hand_number)
        self.origin = Origin.SPLITHAND
        self.AddCard(card1)
        self.AddCard(newcard)
        if left_hand:
            self.x_shift       = -20
            self.x_label_shift = -40
        else:
            self.x_shift       = 40
            self.x_label_shift = 40



def main():
    hand1 = BlackJackHand()
    hand2 = BlackJackHand()
    shoe1 = Shoe(1)
    for x in range(2):
        hand1.AddCard(shoe1.getcard())
        hand2.AddCard(shoe1.getcard())

    print(f"hand 1 (player test): cards are {hand1.cards}, total value is {hand1._get_handtotal()} \n blackjack is {hand1._is_blackjack()}")
    print(f"Hand 2 (dealer test): cards are {hand2.cards}, total value is {hand2._get_handtotal()} \n blackjack is {hand2._is_blackjack()}. dealer should hit is {hand2.DealerTurn()} ")

if __name__ == "__main__":
    main()

