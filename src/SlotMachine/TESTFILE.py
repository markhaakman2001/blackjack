from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup
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
        self.start_btn.pos = QPoint(250, 625)
        self.start_btn.move(self.start_btn.pos)
        self.start_btn.resize(QSize(400, 50))
        self.start_btn.clicked.connect(self.displayreel)

        self.playingfield = PlayingField()
        self.animationgroup = QParallelAnimationGroup()
        
    
    def displayreel(self):
        
        self.playingfield.generate_field()
        for i, reel in enumerate(self.playingfield.reels):
            text = reel.reel_disp
            x = 200 + i * 50
            self.textinwindow(text, x)
            


    
    def textinwindow(self, text, xpos):
        
        self.labels = []
        self.anims = []
        

        for i, letter in enumerate(text):
            ypos = i*75
            label = QtWidgets.QLabel(letter)
            label.setParent(self.central_widget)

            label.pos = QPoint(xpos, ypos)
            label.move(label.pos)
            label.setStyleSheet('background-color:#304; font-size:20px; font-weight:bold; color:#fff;')
            label.show()
            self.labels.append(label)
            anim = QPropertyAnimation(label, b"pos")
            anim.setStartValue(QPoint(xpos, 0))
            anim.setEndValue(QPoint(xpos, ypos))
            anim.setDuration(500 + 2 * xpos)
            self.anims.append(anim)
            self.animationgroup.addAnimation(anim)
            self.animationgroup.start()

    

    def startanimationgroup(self):
        self.animationgroup.start()


app = QtWidgets.QApplication(sys.argv)
ui = TestWindow()
ui.show()
app.exec()