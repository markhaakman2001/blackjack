from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from math import *
import numpy as np
import random
from src.extrafiles.labels import EasyCardLabels
from src.extrafiles.backgroundwidget import BaccaratBackground
import sys






class BaccaratGui(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        self.central_widget = BaccaratBackground()
        self.central_widget.setParent(self)
        self.resize(1200, 700)
        self.central_widget.resize(QSize(1200, 600))

        self.banker_left_xpos = 690   # LEFT BANKER CARD
        self.player_left_xpos = 328   # LEFT PLAYER CARD
        self.label_ypos       = 118   # right in the middle of the box
    






def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = BaccaratGui()
    ui.show()
    app.exec()


if __name__ == "__main__":
    main()

    