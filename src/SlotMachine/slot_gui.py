from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QObject, Signal
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property
from src.SlotMachine.slot_generator import Reels, PlayingField
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QPropertyAnimation, QPoint, QEasingCurve
import time
from math import *
import random
import sys



class SlotGui(QtWidgets.QMainWindow):

    def __init__(self):

        self.playingfield = PlayingField()
        self.playingfield.generate_field()
        self.animations = []
        super().__init__()

        central_widget =  QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.vbox = QtWidgets.QVBoxLayout(central_widget)

        for x in range(5):
            window = Window()
            window.setdisplaytext(str(self.playingfield.full_field_disp[x]))
            self.animations.append(window)
            # self.vbox.addWidget(window)
        
        # self.frame = QtWidgets.QFrame()
        # self.vbox.addWidget(self.frame)

        self.hbox2 = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(self.hbox2)
        
        
        
        self.hbox1 = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(self.hbox1)

        self.start_btn = QtWidgets.QPushButton(text="Spin")
        self.hbox1.addWidget(self.start_btn)

        self.start_btn.clicked.connect(self.startanimation)

    def startanimation(self):
        for x in self.animations:
            
            self.vbox.addWidget(x)
            x.start()
    

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.child = QtWidgets.QTextEdit(self)
        
        # self.child.setStyleSheet("background-color:white;border-radius:30px;")
        # self.child.resize(100, 100)
        self.anim = QPropertyAnimation(self.child, b"pos")
        
        
    def start(self):
        self.anim.setStartValue(QPoint(600, 0))
        self.anim.setEndValue(QPoint(600, 600))
        self.anim.setDuration(1500)
        self.anim.start()
    
    def setdisplaytext(self, textline):
        self.child.clear()
        self.child.append(f"{textline}")

app = QtWidgets.QApplication(sys.argv)
ui = SlotGui()
ui.show()
app.exec()



