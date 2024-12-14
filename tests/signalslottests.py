from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation, Signal, Slot, QObject
from src.SlotMachine.slot_generator import Reels, PlayingField, BankAccount
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from math import *
import numpy as np
import random
import sys


def signalchanged(func):
    def ischanged(*args, **kwargs):
        print("signal change test begin")
        result = func(*args, **kwargs)
    return ischanged



class TestWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_Widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_Widget)
        self.resize(1000, 700)
        self.testlabel = QtWidgets.QLabel(text="TEST!")
        self.testlabel.resize(QSize(100, 100))
        self.testlabel.move(QPoint(150, 150))
        self.testlabel.setParent(self)
        self.testlabel.show()


        self.pushbutton = QtWidgets.QPushButton()
        self.pushbutton.setParent(self)
        self.pushbutton.show()
        self.pushbutton.clicked.connect(self.changebank)

        self.testbank = TestBank()
        self.testbank.testsignal.connect(self.bankchangeevent)

    @Slot(int)
    def bankchangeevent(self, sig):
        if sig == 5:
            self.testlabel.clear()
            self.testlabel.setText("DONE!!!! WHOOOO")
            self.testlabel.update()
    
    @Slot()
    def changebank(self):
        self.testbank.changevalue()


        




class TestBank(QObject):

    testsignal = Signal(int, name="test1")
    testsignal2 = Signal(name="test2")

    def __init__(self):
        super().__init__()
        self.this_value = 0
        self.that_value = 10
    
    def changevalue(self):
        self.this_value += 1
        self.testsignal.emit(5)

    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui =  TestWindow()
    ui.show()
    app.exec()