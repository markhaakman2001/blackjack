from src.blackjack.gui_shoehand import Shoe, Hand, Bank

class Player:

    def __init__(self, hands=1):
        """init

        Args:
            hands (int, optional): amount of hands. Defaults to 1.
        """        
        self.hands = []
        self.bank = Bank(hands)
        for x in range(hands):
            self.hands.append(Hand())
    
    def get_cards(self, cards, cardsymbols):
        """add cards to the players hands

        Args:
            cards (_type_): the cards to be added
        """        
        for i, hand in enumerate(self.hands):
            hand.addcard(cards[i], cardsymbols[i])


    def print_hands(self):
        
        for hand in self.hands:
            print(f"Your cards are {hand.cards}, total is {hand.handtotal(hand.softhand())}")
            
    
    def reset(self):
        self.__init__()

class Dealer:

    def __init__(self):
        self.hand = Hand()
    
    def dealerupcard(self):
        upcard = self.hand.cards[0]
        return upcard
    
    def dealerplay(self, card, card_symbol):
        
        self.hand.addcard(card, card_symbol)
        return f"Dealer pulls {card}, cards are {self.hand.cards}, total is {self.hand.handtotal(self.hand.softhand())}"
    
    def reset(self):
        self.__init__()