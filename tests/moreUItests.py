from PySide6 import QtWidgets
from PySide6.QtWidgets import QPushButton, QComboBox, QDialog, QCheckBox
from PySide6.QtWidgets import QStyleOption, QStyle, QStyleOptionButton
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation, QRectF
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture, QPainter, QBrush, QColor, Qt, QRegion, QIcon
from math import *
import numpy as np
import random
import sys


class TestUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.central = QtWidgets.QWidget()
        self.central.setParent(self)
        self.resize(1200, 600)

        self.testbutton1 = QPushButton(text="clickmew")
        self.testbutton1.setParent(self)
        self.dlg = CustomComboBox()
        self.testbutton1.clicked.connect(self.ShowPopUp)
        
        self.testbutton1.show()

        self.iconbutton = CustomPushButton()
        self.iconbutton.setParent(self)
        self.iconbutton.resize(QSize(110, 110))
        self.iconbutton.show()
        self.dlg.BetSizeSignal.connect(self.printiets)


    def ShowPopUp(self):
        
        self.dlg.exec()
    
    @Slot(int, name="BetSize")
    def printiets(self, signal):
        print(f"Signal emitted BetSize changed to {signal}")



class CustomComboBox(QDialog):

    BetSizeSignal = Signal(int, name="BetSize")

    def __init__(self):
        super().__init__()
        self.resize(250, 250)
        self.one_fiche         = CustomPushButton()
        self.five_fiche        = CustomPushButton()
        self.twentyfive_fiche  = CustomPushButton()
        self.onehundred_fiche  = CustomPushButton()

        self.one_fiche.SetOneValueFiche()
        self.five_fiche.SetFiveValueFiche()
        self.twentyfive_fiche.SetTwentyFiveValueFiche()
        self.onehundred_fiche.SetOneHundredValueFiche()

        self.one_fiche.setParent(self)
        self.five_fiche.setParent(self)
        self.twentyfive_fiche.setParent(self)
        self.onehundred_fiche.setParent(self)
        

        self.one_fiche.resize(QSize(125, 125))
        self.five_fiche.resize(QSize(125, 125))
        self.twentyfive_fiche.resize(QSize(125, 125))
        self.onehundred_fiche.resize(QSize(125, 125))

        self.one_fiche.move(QPoint(0, 0))
        self.five_fiche.move(QPoint(125, 0))
        self.twentyfive_fiche.move(QPoint(0, 125))
        self.onehundred_fiche.move(QPoint(125,125))

        self.one_fiche.ButtonValue.connect(self.SendBetSignal)
        self.five_fiche.ButtonValue.connect(self.SendBetSignal)
        self.twentyfive_fiche.ButtonValue.connect(self.SendBetSignal)
        self.onehundred_fiche.ButtonValue.connect(self.SendBetSignal)

    
    @Slot(int, name="ButtonValue")
    def SendBetSignal(self, signal):
        print(f"Current Betsize: {signal}")
        self.BetSizeSignal.emit(signal)



class CustomPushButton(QtWidgets.QPushButton):

    ButtonValue = Signal(int, name="ButtonValue")

    def __init__(self):
        super().__init__()
        self._pixmap = QPixmap()
        self._path   = "tests/testimages/"
        self._value  = 0
        self.clicked.connect(self.SendCurrentvalue)
        
    
    def SetOneValueFiche(self):
        self._pixmap.load("tests/testimages/1casinochip.jpg")

        self._icon = QIcon(self._pixmap)
        self.icon = self._icon
        self.setIcon(self.icon)
        self.setIconSize(QSize(100, 100))
        self._value = 1
        self.ButtonValue.emit(self._value)
    
    def SetFiveValueFiche(self):
        self._pixmap.load("tests/testimages/5casinochip.jpg")

        self._icon = QIcon(self._pixmap)
        self.icon = self._icon
        self.setIcon(self.icon)
        self.setIconSize(QSize(100, 100))
        self._value = 5
        self.ButtonValue.emit(self._value)
    
    def SetTwentyFiveValueFiche(self):
        self._pixmap.load("tests/testimages/25casinochip.jpg")

        self._icon = QIcon(self._pixmap)
        self.icon = self._icon
        self.setIcon(self.icon)
        self.setIconSize(QSize(100, 100))
        self._value = 25
        self.ButtonValue.emit(self._value)
    
    def SetOneHundredValueFiche(self):
        self._pixmap.load("tests/testimages/100casinochip.jpg")

        self._icon = QIcon(self._pixmap)
        self.icon = self._icon
        self.setIcon(self.icon)
        self.setIconSize(QSize(100, 100))
        self._value = 100
        self.ButtonValue.emit(self._value)
    
    @Slot()
    def SendCurrentvalue(self):
        print(F"Current Value is {self._value}")
        self.ButtonValue.emit(self._value)


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = TestUI()
    ui.show()
    app.exec()
    


if __name__ == "__main__":
    main()