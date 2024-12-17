from src.extrafiles.labels import EasyCardLabels
from src.baccarat.baccarat_cards import Card
from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from src.baccarat.baccarat_table_handler import PlayerType
from src.baccarat.baccarat_cards import CardSymbol, Kind
import sys

class BaccaratCard(EasyCardLabels):

    def __init__(self):
        super().__init__()

    def CreateAnimation(self,xposition, card: Card):
        yposition = 118
        CardName  = card._get_CardName()
        self.setnewimage(CardName)
        self.animation.setStartValue(QPoint(0, 0))
        self.animation.setEndValue(QPoint(xposition, yposition))
        self.animation.setDuration(500)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    card = BaccaratCard()
    card1 = Card(Kind.CLOVER, CardSymbol.ACE)
    card.CreateAnimation(200, card1)