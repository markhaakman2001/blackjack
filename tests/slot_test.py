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


        self.pixmap = QPixmap()
        self.picture = self.pixmap.load("src/SlotMachine/images/acecard.jpg")
        

        # self.label = QtWidgets.QLabel()
        # self.label.setParent(self.central_widget)
        # self.label.pos = QPoint(100, 100)
        # self.label.move(self.label.pos)
        # self.label.pixmap = self.pixmap
        
        # self.label.setPixmap(self.label.pixmap)
        # self.label.width = 50
        # self.label.height = 60
        # self.label.setFixedWidth(self.label.width)
        # self.label.setFixedHeight(self.label.height)
        # self.label.setScaledContents(True)
        self.label = CustomLabels()
        self.label.setParent(self.central_widget)
        self.label.setnewimage("k")
        self.label.show()


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