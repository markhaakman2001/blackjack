from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup
from src.SlotMachine.slot_generator import Reels, PlayingField
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
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
        self.start_btn.clicked.connect(self.showpicturetest)

        self.playingfield = PlayingField()
        self.animationgroup = QParallelAnimationGroup()
        self.imagereader = QImageReader()

        self.pixmap = QPixmap()
        self.pixmap.load("acecard.jpg")
        
        
        # self.picture = self.pixmap.toImage()
        self.image = QImage()
        self.imagereader.setFileName("src.SlotMachine.images.acecard.jpg")

        
    def showpicturetest(self):
        # img = self.image.load("src.SlotMachine.images.acecard.jpg")
        
        piclabel = QtWidgets.QLabel()
        piclabel.pos = QPoint(100, 100)
        piclabel.move(piclabel.pos)

        
        piclabel.setParent(self.central_widget)
        piclabel.setPixmap(self.pixmap)
        piclabel.setScaledContents(True)
        piclabel.show()
        
        
    
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
            label.setStyleSheet('background-color:#204; font-size:20px; font-weight:bold; color:#fff;')
            label.show()
            self.labels.append(label)
            anim = QPropertyAnimation(label, b"pos")
            anim.setStartValue(QPoint(xpos, 0))
            anim.setEndValue(QPoint(xpos, ypos))
            anim.setDuration(100 + 2 * xpos)
            self.anims.append(anim)
            self.animationgroup.addAnimation(anim)
            self.animationgroup.start()

    

    def startanimationgroup(self):
        self.animationgroup.start()



class CustomLabels(QtWidgets.QLabel):

    def __init__(self):

        super().__init__()

        self.pathname = "src/SlotMachine/images/"
        self.pixmap1 = QPixmap()
        self.width = 50
        self.height = 60
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
    

    def setnewimage(self, filename):

        choices = {
            "ace":"acecard.jpg",
            "k": "kheart.jpg",
            "q": "Qheart.jpg",
            "j": "jhearts.jpg",
            "10":"10heart.jpg",
        }

        self.pixmap1.load(f"{self.pathname}" + choices.get(filename))
        self.pixmap = self.pixmap1
        self.setPixmap(self.pixmap1)
        self.setScaledContents(True)




app = QtWidgets.QApplication(sys.argv)
ui = TestWindow()
ui.show()
app.exec()