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

        # Need label array to animate winning lines
        self.label_array = None
        labels = []

        # Label array for reusing labels instead of making new ones
        for x in range(6):
            
            if x == 0:
                self.label_array = self.createlabelarray()
            else:
                arr = self.createlabelarray()
                self.label_array = np.column_stack((self.label_array, arr))
        

            

    def createlabelarray(self):
        labels = []
        for x in range(5):
            lbl = CustomLabels()
            lbl.setParent(self.central_widget)
            labels.append(lbl)
        arr = np.array(labels)
        return arr


    
    def displayreel(self):
        
        # Generate a new random array of values
        self.playingfield.generate_field()
        for i, reel in enumerate(self.playingfield.reels):
            text = reel.reel_disp
            x = 200 + i * 80
            self.textinwindownew(text, x, i)
        
        self.displaywinnersnew()
        # self.displaywinners()



    def displaywinnersnew(self):
        straight_arr, zigzag_arr = self.playingfield.checkwinnings()
        arrlist = [straight_arr, zigzag_arr]
        

        for linearray in arrlist:
            print(linearray)
            if np.any(linearray):
                
                winarray = self.label_array[np.asarray(linearray).nonzero()]
                thisarray = (linearray).nonzero()
                
                anims = []
                self.anim_group = QSequentialAnimationGroup()

                print(np.argwhere(linearray))
                for x in np.argwhere(linearray):
                    label = self.label_array[x[0]][x[1]]
                    #print(i)
                    if not label.isanimated:
                        win_anim = QPropertyAnimation(label, b"geometry")
                        win_anim.setStartValue(QRect(label.shiftedpos, QSize(0, 0)))
                        win_anim.setEndValue(QRect(label.currentpos, QSize(80, 96)))
                        win_anim.setDuration(800)
                        self.anim_group.addAnimation(win_anim)
                        anims.append(win_anim)
                    
                self.anim_group.start()


                

    
    def textinwindownew(self, text, xpos, index):
        self.anims = []
        
        for i, letter in enumerate(text):
            ypos = i*96

            # Custom label with image
            label: CustomLabels = self.label_array[i, index]
            label.setnewimage(str(letter))
            label.show()
            label.isnotanimated()
            
            # Create animation
            anim = QPropertyAnimation(label, b"pos")
            anim.setStartValue(QPoint(xpos, 0))
            anim.setEndValue(QPoint(xpos, ypos))
            label.setpos(QPoint(xpos, ypos))
            label.setshiftpos(QPoint(xpos + 40, ypos + 48))
            anim.setDuration(100 + xpos)

            self.anims.append(anim)
            self.animationgroup.addAnimation(anim)
            self.animationgroup.start()


    def startanimationgroup(self):
        self.animationgroup.start()



class CustomLabels(QtWidgets.QLabel):

    def __init__(self):

        super().__init__()

        self.animated = False
        self.pathname = "src/SlotMachine/images/"
        self.pixmap1 = QPixmap()
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