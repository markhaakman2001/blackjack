from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle, QGraphicsRotation
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from src.SlotMachine.slot_generator import Reels, PlayingField, BankAccount
from src.extrafiles.backgroundwidget import BackGroundWidget
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture, QPainter
from math import *
import numpy as np
import random
import sys



class TestWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.centralwidget = BackGroundWidget()
        self.setCentralWidget(self.centralwidget)
        
        #self.label = EasyCardLabels()
        self.vbox = QtWidgets.QVBoxLayout()
        
        #self.vbox.addWidget(self.label)
        self.deck = DeckOfCards()
        
        self.testbtn = QtWidgets.QPushButton()
        self.testbtn.setParent(self.centralwidget)
        self.testbtn.pos = QPoint(100, 100)
        self.testbtn.move(self.testbtn.pos)
        self.testbtn.clicked.connect(self.PickCardandShow)

    def PickCardandShow(self):
        
        self.label = EasyCardLabels()
        randomcard = self.deck.pickacard()
        self.label.setnewimage(cardname=randomcard)
        self.label.setParent(self.centralwidget)
        self.label.show()



class Shoe:

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

    Args:
        QtWidgets (_type_): _description_
    """    


    def __init__(self):
        

        super().__init__()

        self.rotation     =   QGraphicsRotation(self)
        self.animated     =   False
        self.pathname     =   "src/extrafiles/images/"
        self.pixmap1      =   QPixmap()
        self.animation    =   QPropertyAnimation(self, b"pos", self)
        self.animation2   =   QPropertyAnimation(self, b"geometry", self)
        self.width        =   60
        self.height       =   72

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
    def currentpos(self):
        return self.currentposition
    
    @Property(QPoint)
    def shiftedpos(self):
        return self.shiftedposition
    
    
    def setpos(self, pos:QPoint):
        self.currentposition = pos

    def setshiftpos(self, shiftpos:QPoint):
        self.shiftedposition = shiftpos
    

    def setnewimage(self, cardname: str):
        """Used set a different image on the label.

        Args:
            filename (str): The dictionary key for the images.
        """        
        
        self.pixmap1 = QPixmap()
        self.pixmap1.load(f"{self.pathname}" + f"{cardname}.jpg")
        self.pixmap  = self.pixmap1
        self.setPixmap(self.pixmap1)
        self.setScaledContents(True)
    
    def rotatelabel(self, x_index=0):
        self.rotation.setAngle(45)
        self.rotation.setParent(self)
        self.updateGeometry()
        self.update()
    




def main():
    app  = QtWidgets.QApplication(sys.argv)
    ui   = TestWindow()
    shoe = Shoe(4)
    ui.show()
    app.exec()

if __name__ == "__main__":
    main()
