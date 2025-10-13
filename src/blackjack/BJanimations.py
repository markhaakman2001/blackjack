from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QSize, QPoint, QSequentialAnimationGroup, QParallelAnimationGroup
import PySide6.QtCore as Core
from CustomUIfiles import EasyCardLabels
from PySide6.QtWidgets import QGraphicsRotation
from PySide6.QtCore import QPropertyAnimation, QPoint
from PySide6.QtCore import QPropertyAnimation, Property
from PySide6.QtGui import QPixmap
from baccarat.baccarat_cards import Card


class BlackJackAnimatedCard(EasyCardLabels):

    def __init__(self):
        super().__init__()
    

    def TestAnimation(self, card : Card, y_position = 350):
        cardname = card._get_CardName()
        self.setnewimage(cardname)
        self.animation.setStartValue(QPoint(0, 0))
        self.animation.setEndValue(QPoint(500, y_position))
        self.animation.setDuration(500)


    