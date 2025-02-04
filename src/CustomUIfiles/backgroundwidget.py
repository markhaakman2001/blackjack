from PySide6 import QtWidgets
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture, QPainter, QPaintEvent, QPalette, QIcon, QPaintDevice
from PySide6.QtCore import QPoint, QSize
from math import *
import numpy as np
import random
import sys





class BackGroundWidget(QtWidgets.QWidget):
    """Custom Qwidget that functions as background image for the blackjack UI.
    Inherits from QWidget.
    
    """    

    def __init__(self):
        super().__init__()
        
        self.icon1 = QIcon()
        self.pixmap = QPixmap()
        self.pixmap.load("customimages/images/blackjacktable3.jpg")
        self.label = QtWidgets.QLabel()
        self.label.setParent(self)
        self.label.pixmap = self.pixmap
        self.label.setPixmap(self.pixmap)
        
        self.label.setScaledContents(True)
        self.resize(QSize(1000, 700))
        
        self.label.size = QSize(1000, 700)
        self.label.resize(self.label.size)
        self.setMaximumSize(QSize(1000, 1000))
        self.label.setMaximumSize(QSize(1000, 700))
        
        
        self.setAutoFillBackground(True)
        
        

        self.palette = QPalette()

class BaccaratBackground(QtWidgets.QWidget):
    """Custom QWidget that functions as the background image for the Baccarat UI.
    
    Inherits from QWidget.
    """    

    def __init__(self):
        super().__init__()
        
        self.icon1 = QIcon()
        self.pixmap = QPixmap()
        self.pixmap.load("customimages/baccaratImage/baccarattable2.jpg")
        self.label = QtWidgets.QLabel()
        self.label.setParent(self)
        self.label.pixmap = self.pixmap
        self.label.setPixmap(self.pixmap)
        
        self.label.setScaledContents(True)
        self.resize(QSize(1200, 600))
        
        self.label.size = QSize(1200, 600)
        self.label.resize(self.label.size)
        self.setMaximumSize(QSize(1200, 1000))
        self.label.setMaximumSize(QSize(1200, 1000))
        
        
        self.setAutoFillBackground(True)
        
        

        self.palette = QPalette()
