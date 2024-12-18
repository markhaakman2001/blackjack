from PySide6 import QtWidgets
from PySide6.QtWidgets import QPushButton, QComboBox, QDialog, QCheckBox
from PySide6.QtWidgets import QStyleOption, QStyle, QStyleOptionButton
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation, QRectF
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture, QPainter, QBrush, QColor, Qt, QRegion
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
        self.testbutton1.show()
        self.testbutton1.clicked.connect(self.ShowPopUp)


    def ShowPopUp(self):
        self.dlg = CustomComboBox()
        self.dlg.btn1.clicked.connect(self.printiets)
        self.dlg.show()
    
    @Slot()
    def printiets(self):
        print("yo")



class CustomComboBox(QDialog):

    Signal1 = Signal(float, name="CLICK")

    def __init__(self):
        super().__init__()
        self.resize(250, 250)
        self.btn1 = QPushButton(text="1")
        self.btn2 = QPushButton(text="2")

        self.btn3 = QCheckBox(text="3")
        self.btn4 = QCheckBox(text="4")
        self.grp = QtWidgets.QButtonGroup(self)

        self.grp.addButton(self.btn3)
        self.grp.addButton(self.btn4)

        self.btn1.setParent(self)
        self.btn2.setParent(self)
        self.btn3.setParent(self)
        self.btn4.setParent(self)
        

        self.btn1.resize(QSize(125, 125))
        self.btn2.resize(QSize(125, 125))
        self.btn3.resize(QSize(125, 125))
        self.btn4.resize(QSize(125, 125))

        self.btn1.move(QPoint(0, 0))
        self.btn2.move(QPoint(125, 0))
        self.btn3.move(QPoint(0, 125))
        self.btn4.move(QPoint(125,125))



def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = TestUI()
    ui.show()
    app.exec()
    


if __name__ == "__main__":
    main()