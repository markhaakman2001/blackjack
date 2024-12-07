from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup
from src.SlotMachine.slot_generator import Reels, PlayingField
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from math import *
import numpy as np
import random
import sys



class TestWindow(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

        self.central_widget = QtWidgets.QWidget()
        self.resize(900, 700)
        self.setCentralWidget(self.central_widget)

        # create start button
        self.start_btn = QtWidgets.QPushButton("Start")
        self.start_btn.setParent(self.central_widget)
        self.start_btn.pos = QPoint(250, 625)
        self.start_btn.move(self.start_btn.pos)
        self.start_btn.resize(QSize(400, 50))
        self.start_btn.clicked.connect(self.displayreel)


        # initialise the slot generator
        self.playingfield = PlayingField()
        self.animationgroup = QParallelAnimationGroup()
        # self.anim_group = QParallelAnimationGroup()
        self.fallanimationgroup = QParallelAnimationGroup()

        # Need label array to animate winning lines
        self.label_array = None
        labels = []
        self.first = True
        # Label array for reusing labels instead of making new ones
        for x in range(6):
            xpos = 200 + x * 80
            if x == 0:
                self.label_array = self.createlabelarray(xpos)
            else:
                arr = self.createlabelarray(xpos)
                self.label_array = np.column_stack((self.label_array, arr))
                
        
        self.createfallanimation()
        self.createwinanimation()
        

            

    def createlabelarray(self, xpos):
        self.labels = []
        for y in range(5):
            ypos = y * 96
            self.lbl = CustomLabels()
            self.lbl.setParent(self.central_widget)
            self.lbl.setVisible(False)
            self.lbl.setpos(QPoint(xpos, ypos))
            self.lbl.setshiftpos(QPoint(xpos + 40, ypos + 48))
            
            self.labels.append(self.lbl)
        arr = np.array(self.labels)
        return arr


    
    def displayreel(self):
        
        self.animationgroup = QParallelAnimationGroup()
        self.anim_group = [QParallelAnimationGroup(), QParallelAnimationGroup()]
        self.printvisibility()
        # Generate a new random array of values
        self.playingfield.generate_field()
        #self.start_btn.setEnabled(False)
        for i, reel in enumerate(self.playingfield.reels):
            text = reel.reel_disp
            x = 200 + i * 80
            self.textinwindownew(text, x, i)
        
        self.displaywinnersnew()
        #self.animationgroup.finished.connect(self.displaywinnersnew)
        self.first = False
        
        # self.displaywinners()
    

    def printvisibility(self):
        this_arr = np.empty((5, 6))
        for x in range(5):
            for y in range(6):
                thislabel: CustomLabels = self.label_array[x, y]
                this_arr[x, y] = thislabel.windowOpacity()
        print(this_arr)

    @Slot()
    def enablestart(self):
        self.start_btn.setEnabled(True)


    def displaywinnersnew(self):
        straight_arr, zigzag_arr = self.playingfield.checkwinnings()
        arrlist = [straight_arr, zigzag_arr]
        
        
        for i, linearray in enumerate(arrlist):
            
            if np.any(linearray):
                anims = []
                
                for x in np.argwhere(linearray):
                    label: CustomLabels = self.label_array[x[0]][x[1]]
                    #print(i)
                    
                    self.anim_group[i].addAnimation(label.animation2)
                    
                        
                self.anim_group[i].start()



    def createfallanimation(self):
        for x in range(5):
            for y in range(6):
                xpos = 200 + y * 80
                ypos = x * 96
                label: CustomLabels = self.label_array[x, y]
                label.animation.setStartValue(QPoint(xpos, 0))
                label.animation.setEndValue(QPoint(xpos, ypos))
                label.animation.setDuration(100 + xpos)
                self.fallanimationgroup.addAnimation(label.animation)
    

    def createwinanimation(self):
        for x in range(5):
            for y in range(6):
                label: CustomLabels = self.label_array[x, y]
                label.animation2.setKeyValueAt(0, QRect(label.shiftedpos, QSize(0, 0)))
                label.animation2.setKeyValueAt(0.25,QRect(label.currentpos, QSize(80, 96)))
                label.animation2.setKeyValueAt(0.60, QRect(label.shiftedpos, QSize(0, 0)))
                label.animation2.setKeyValueAt(1, QRect(label.currentpos, QSize(80, 96)))
                label.animation2.setDuration(800)
                
                
        
        





    def textinwindownew(self, text, xpos, index):
        self.anims = []
        # self.animationgroup = QParallelAnimationGroup()
        for i, letter in enumerate(text):
            ypos = i*96
            
            # Custom label with image
            self.label: CustomLabels = self.label_array[i, index]
            self.label.clear()
            
            self.label.setnewimage(str(letter))
            self.label.setVisible(True)
            self.label.show()
            self.label.isnotanimated()
        
            
            # Create animation
            # self.anim = QPropertyAnimation(self.label, b"pos")
            # self.anim.setStartValue(QPoint(xpos, 0))
            # self.anim.setEndValue(QPoint(xpos, ypos))
            
            # self.anim.setDuration(100 + xpos)
            
            # self.anims.append(self.anim)
            # self.animationgroup.addAnimation(self.anim)
            self.fallanimationgroup.start()
            
            
            

    def startanimationgroup(self):
        self.animationgroup.start()



class CustomLabels(QtWidgets.QLabel):

    def __init__(self):

        super().__init__()

        self.animated = False
        self.pathname = "src/SlotMachine/images/"
        self.pixmap1 = QPixmap()
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation2 = QPropertyAnimation(self, b"geometry")
        self.width = 80
        self.height = 96
        self.setMaximumWidth(self.width)
        self.setMaximumHeight(self.height)

    @Property(bool)
    def isanimated(self):
        return self.animated
    
    def setanimated(self):
        self.animated = True

    def isnotanimated(self):
        self.animated = False
    
    @Property(str)
    def currentpicture(self):
        return self.currently
    
    @Property(QPoint)
    def currentpos(self):
        return self.currentposition
    
    @Property(QPoint)
    def shiftedpos(self):
        return self.shiftedposition

    
    def setpos(self, pos:QPoint):
        self.currentposition = pos

    def setshiftpos(self, shiftpos:QPoint):
        self.shiftedposition = shiftpos
    

    def setnewimage(self, filename):
        
        self.pixmap1 = QPixmap()
        choices = {
            "A":"acecard.jpg",
            "K": "kheart.jpg",
            "Q": "Qheart.jpg",
            "J": "jhearts.jpg",
            "10": "10heart.jpg",
            "5": "5heart.jpg",
            "4": "4heart.jpg",
            "3": "3heart.jpg",
            "2": "2heart.jpg",
        }

        
        self.currently = choices.get(filename)
        self.pixmap1.load(f"{self.pathname}" + f"{choices.get(filename)}")
        self.pixmap = self.pixmap1
        self.setPixmap(self.pixmap1)
        self.setScaledContents(True)




app = QtWidgets.QApplication(sys.argv)
ui = TestWindow()
ui.show()
app.exec()