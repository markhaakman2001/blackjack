from PySide6 import QtWidgets
from PySide6.QtWidgets import QGraphicsRotation
from PySide6.QtCore import QPropertyAnimation, QPoint
from PySide6.QtCore import QPropertyAnimation, Property
from PySide6.QtGui import QPixmap
import random




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
    


    def getcard(self, n_cards : int = 1) -> int:
        """take the next card or cards from the shoe.

        Args:
            n (int, optional): amount of cards to be taken. Defaults to 1.

        Returns:
            int, list: The card value or card values and the cardsymbols
        """          
        if n_cards == 1:
            card = self.all_shoe_cards.pop(0)
            card_value = self.singledeck.getcardvalue(card)
            return card_value, card
        else:
            cards = []
            card_vals = []
            for x in range(n_cards):
                card = self.all_shoe_cards.pop(0)
                card_value = self.singledeck.getcardvalue(card)
                cards.append(card)
                card_vals.append(card_value)
            return card_vals, cards


class DeckOfCards:

    def __init__(self):
        self.all_cards = []
        self.card_types = ["hearts", "spades", "diamond", "clover"]
        self.card_symbols = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a"]
        self.card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        self.symbol_value_dict = dict(zip(self.card_symbols, self.card_values))
        
        self.card_value_dict_list = []

        for CardType in self.card_types:
            current_cards = []

            for CardSymbol in self.card_symbols:
                specific_card = CardSymbol + CardType    
                self.all_cards.append(specific_card)
                current_cards.append(specific_card)

            current_dict = dict(zip(current_cards, self.card_values))
            self.card_value_dict_list.append(current_dict)
            
    
    def pickacard(self) -> str:
        x = random.randint(0, 51)
        card = self.all_cards[x]
        self.getcardvalue(card)
        return card
    
    def getcardvalue(self, card:str) -> int:
        if card[-1] == "d":
            value = self.symbol_value_dict.get(card[:-7])
            return value
        else:
            value = self.symbol_value_dict.get(card[:-6])
            return value





class EasyCardLabels(QtWidgets.QLabel):
    """Custom label class used for easier animations in the slot machine.
    Is a subclass of QLabel.
    """    


    def __init__(self):
        

        super().__init__()
        self._shiftedpos  = QPoint(0, 0)
        self._currentpos  = QPoint(0, 0)
        self.rotation     =   QGraphicsRotation(self)
        self.animated     =   False
        self.pathname     =   "src/extrafiles/imagesPNG/"
        self.pixmap1      =   QPixmap()
        self.animation    =   QPropertyAnimation(self, b"pos", self)
        self.animation2   =   QPropertyAnimation(self, b"geometry", self)
        self.setFixedWidth(60)
        self.setFixedHeight(72)

        self.setMaximumWidth(80)
        self.setMaximumHeight(96)
        

    @Property(bool)
    def isanimated(self):
        return self.animated
    
    def setanimated(self):
        self.animated = True

    def isnotanimated(self):
        self.animated = False
    
    @Property(str)
    def currentpicture(self):
        return self.currently
    
    @Property(QPoint)
    def currentpos(self) -> QPoint:
        return self._currentpos_
    
    @Property(QPoint)
    def shiftedpos(self):
        return self._shiftedposition
    
    @currentpos.setter
    def setcurrentpos(self, pos:QPoint):
        self._currentpos_ = pos

    @shiftedpos.setter
    def setshiftpos(self, currentpos:QPoint):
        self._shiftedposition = QPoint(currentpos.x(), currentpos.y() -35)
    

    def setnewimage(self, cardname: str):
        """Used set a different image on the label.

        Args:
            filename (str): The dictionary key for the images.
        """        
        
        self.pixmap1 = QPixmap(f"{self.pathname}" + f"{cardname}.png")
        #self.pixmap1.load(f"{self.pathname}" + f"{cardname}.jpg")
        #self.pixmap  = self.pixmap1
        self.setPixmap(self.pixmap1)
        self.setScaledContents(True)
    
    def rotatelabel(self, x_index=0):
        self.rotation.setAngle(45)
        self.rotation.setParent(self)
        self.updateGeometry()
        self.update()






def main():
    pass

if __name__ == "__main__":
    main()
