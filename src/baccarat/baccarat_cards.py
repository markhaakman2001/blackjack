import random
from enum import Enum, auto


class Color(Enum):

    RED   = auto()
    BLACK = auto()

class Kind(Enum):

    HEART   = "hearts"
    CLOVER  = "clover"
    DIAMOND = "diamond"
    SPADES  = "spades"

    def getcolor(self) -> Color:
        if self.value == "hearts" or self.value == "diamond":
            return Color.RED
        else:
            return Color.BLACK


class CardSymbol(Enum):

    TWO     = (2, "2")
    THREE   = (3, "3")
    FOUR    = (4, "4")
    FIVE    = (5, "5")
    SIX     = (6, "6")
    SEVEN   = (7, "7")
    EIGHT   = (8, "8")
    NINE    = (9, "9")
    TEN     = (10, "10")
    JACK    = (10, "j")
    QUEEN   = (10, "q")
    KING    = (10, "k")
    ACE     = (11, "a")

    def name(self) -> str:
        """Return the name in string format

        Returns:
            str: The name of the card in a string. so CardSymbol.ACE.name() would return "a"
        """        
        return self.value[1]
    
    def getvalue(self) -> int:
        """Return the actual face value of the symbol

        Returns:
            int: the value (e.g KING would become 10)
        """
        return self.value[0]

class Card:

    def __init__(self, type : Kind, Symbol : CardSymbol):
        self.type : Kind         = type
        self.symbol : CardSymbol = Symbol

    def _get_value(self) -> int:
        """Get the face value of the card

        Returns:
            int: the value (0, 11)
        """        
        return self.symbol.getvalue()
    
    def _get_CardName(self):
        """Get the name of the card in string format
        """        
        return self.symbol.name() + self.type.value
    
    def _get_CardColor(self):
        color : Color = self.type.getcolor()
        return color
    
    def _is_ace(self):
        if self.symbol == CardSymbol.ACE:
            return True
        else:
            return False


class Shoe:
    """Class that contains a certain amount of decks in a random order.
    """    

    def __init__(self, ndecks):
        self.singledeck = DeckOfCards()
        self.all_shoe_cards = []
        for x in range(ndecks):
            one_full_deck = self.singledeck.all_cards
            self.all_shoe_cards.extend(one_full_deck)
        random.shuffle(self.all_shoe_cards)


    def getcard(self, n_cards : int = 1) -> Card | list[Card]:
        """take the next card or cards from the shoe.

        Args:
            n (int, optional): amount of cards to be taken. Defaults to 1.

        Returns:
            int, list: The card value or card values and the cardsymbols
        """          
        if n_cards == 1:
            card = self.all_shoe_cards.pop(0)
            return card
        else:
            cards : list[Card] = []
            for x in range(n_cards):
                card = self.all_shoe_cards.pop(0)
                cards.append(card)
            return cards



class DeckOfCards:
    """This is one deck of cards
    """    

    def __init__(self):
        self.all_cards = []

        for cardtype in Kind:
            
            for card_symbol in CardSymbol:
                self.new_card = Card(type = cardtype, Symbol=card_symbol)
                self.all_cards.append(self.new_card)



if __name__ == "__main__":
    mycard = Card(Kind.HEART, CardSymbol.TWO)
    
    print(mycard._get_value())
    print(mycard._get_CardName())
    shoe = Shoe(ndecks=8)
    print(len(shoe.all_shoe_cards))
    





