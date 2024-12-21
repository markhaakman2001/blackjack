from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture, QIcon
import numpy as np
import random
import sys



class BaccaratFiche(QtWidgets.QPushButton):

    def __init__(self):
        super().__init__()
        self._pixmap = QPixmap()
        self._pixmap.load("tests/testimages/casinochip.jpg")

        self._icon = QIcon(self._pixmap)
        self.icon = self._icon
        self.setIcon(self.icon)
        self.setIconSize(QSize(100, 100))