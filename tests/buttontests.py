from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle, QStyleOptionButton
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation, QRectF
from src.SlotMachine.slot_generator import Reels, PlayingField, BankAccount
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture, QPainter, QBrush, QColor, Qt, QRegion
from math import *
import numpy as np
import random
import sys


class NewWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.central_widget = QtWidgets.QWidget()
        self.resize(900, 700)
        self.setCentralWidget(self.central_widget)
        self.widget1 = BetButton()
        self.widget1.setParent(self.central_widget)




class _Round(QtWidgets.QWidget):

    clicked = Signal(Qt.MouseButton.LeftButton)

    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.signal1 = Signal()
    

    def printiets(self):
        print("YO")
    
    def mousePressEvent(self, event):
        return super().mousePressEvent(event)

    def paintEvent(self, e):
        painter = QPainter(self)
        brush = QBrush()
        style = Qt.BrushStyle.SolidPattern
        brush.setColor(QColor('black'))
        brush.setStyle(style)
        rect = QRect(0, 0, painter.device().width(), painter.device().width())
        painter.drawEllipse(rect)


class BetButton(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()
        self.resize(QSize(500, 500))
        layout = QtWidgets.QVBoxLayout(self)
        self._round1 = _Round()
        self._round2 = _Round()
        
        self.combobox = QtWidgets.QComboBox()
        self.combobox.resize(QSize(100, 100))
        layout.addWidget(self.combobox)
        self._round1.clicked.connect(self.printiets)

        self.hbox = QtWidgets.QHBoxLayout()

        layout.addLayout(self.hbox)
        self.hbox.addWidget(self._round1)
        self.hbox.addWidget(self._round2)
        self._round1.setParent(self)
        self._round2.setParent(self)
    
    def printiets(Self):
        print("yo")
        



        
        
        



def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = NewWindow()
    ui.show()
    app.exec()


if __name__ == "__main__":
    main()