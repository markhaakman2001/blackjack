from src.extrafiles.labels import EasyCardLabels
from src.baccarat.baccarat_cards import Card
from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from src.baccarat.baccarat_table_handler import PlayerType


class BaccaratCard(EasyCardLabels):

    def __init__(self):
        super().__init__()

    def CreateAnimation(self, playertype : PlayerType):
        ypos = 118
        if playertype == PlayerType.PLAYER:
            xpos = [328, 388]
        else:
            xpos = [690, 750]

        
