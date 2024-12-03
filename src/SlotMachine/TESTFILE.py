from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property
from src.SlotMachine.slot_generator import Reels, PlayingField
import time
from math import *
import random
import sys



class TestWindow(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

        self.central_widget = QtWidgets.QWidget()
        self.resize(900, 700)
        self.setCentralWidget(self.central_widget)
        self.start_btn = QtWidgets.QPushButton("Start")
        self.start_btn.setParent(self.central_widget)
        self.start_btn.clicked.connect(self.textinwindow)
    

    def textinwindow(self):
        text = ["T", "E", "S", "T"]
        for i, letter in enumerate(text):
            xpos = i * 300
            label = QtWidgets.QLabel(letter)
            label.setParent(self.central_widget)
            
            label.show()
            label.pos = QPoint(xpos, 50)
            label.resize(100, 100)
            
            
            
            
            





app = QtWidgets.QApplication(sys.argv)
ui = TestWindow()
ui.show()
app.exec()