from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from src.SlotMachine.slot_generator import Reels, PlayingField, BankAccount
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from math import *
import numpy as np
import random
from src.SlotMachine.TESTFILE import CustomLabels
import sys






class BaccaratGui(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        pass




def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = BaccaratGui()
    ui.show()
    app.exec()


if __name__ == "__main__":
    main()

    