from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from src.SlotMachine.slot_generator import Reels, PlayingField, BankAccount
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from math import *
import numpy as np
import random
import sys



class TestWindow(QtWidgets.QMainWindow):

    signal1 = Signal()
    signal2 = Signal()
    

    def __init__(self):

        super().__init__()

        self.bank = BankAccount()
        self.bank.deposit(10000)
        self.funds = self.bank._get_funds()
        print(self.funds)

        self.central_widget = QtWidgets.QWidget()
        self.resize(900, 700)
        self.setCentralWidget(self.central_widget)

        # create start button
        self.start_btn = QtWidgets.QPushButton("Spin")
        self.start_btn.setParent(self.central_widget)
        self.start_btn.pos = QPoint(250, 625)
        self.start_btn.move(self.start_btn.pos)
        self.start_btn.resize(QSize(400, 50))
        self.start_btn.clicked.connect(self.displayreel)
        self.start_btn.clicked.connect(self.getridofpopup)

        # bet button
        self.betbutton = QtWidgets.QComboBox()
        self.betbutton.acceptDrops
        self.betbutton.setParent(self.central_widget)
        self.betbutton.pos = QPoint(150, 625)
        self.betbutton.move(self.betbutton.pos)
        self.betbutton.resize(QSize(50, 50))

        self.balance = QtWidgets.QTextEdit()
        self.balance.setParent(self.central_widget)
        self.balance.pos = QPoint(150, 575)
        self.balance.move(self.balance.pos)
        self.balance.resize(QSize(100, 50))
                              


        self.betbutton.addItems(["$0.1", "$0.2", "$0.4", "$0.6", "$1", "$2", "$5", "$10"])
        self.betsizes = [0.1, 0.2, 0.4, 0.6, 1, 2, 5, 10]

        # initialise the slot generator
        self.playingfield = PlayingField()
        self.animationgroup = QParallelAnimationGroup()


        self.fallanimationgroup = QParallelAnimationGroup()
        # self.sequantialanimgroup = QSequentialAnimationGroup(self)
        
        self.sequentialanimgroup1 = QSequentialAnimationGroup(self)
        self.sequentialanimgroup2 = QSequentialAnimationGroup(self)

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


        self.lastwin = 0
        self.dlg_off = True
        self.signal1.connect(self.winpopup)
        self.signal2.connect(self.enablestart)
        
        
        self.createfallanimation()
        self.createwinanimation()
        

            

    def createlabelarray(self, xpos):
        """Create a reel of customlabels that is used to display the symbols on the playingfield.

        Args:
            xpos (int): The x position of the reel on the screen.

        Returns:
            numpy array: array of 5 custom labels with same xposition and stacked vertically with yposition.
        """        
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
    
    def update_balance(self):
        self.balance.clear()
        self.balance.append(f"Current balance: ${self.bank._get_funds():.2f}")


    def displayreel(self):
        """Generate a new playingfield and starts the fallinganimation for the labels in the slots.
        When the fallinganimation is finished, the displaywinners method is called.
        """        
        
        self.animationgroup = QParallelAnimationGroup()
        self.lastwin = 0
        
        self.printvisibility()
        self.bank.placebet(self.betsizes[self.betbutton.currentIndex()])
        self.update_balance()
        # Generate a new random array of values
        self.playingfield.generate_field()
        self.start_btn.setEnabled(False)
        for i, reel in enumerate(self.playingfield.reels):
            text = reel.reel_disp
            x = 200 + i * 80
            self.textinwindownew(text, x, i)
        
        #self.displaywinnersnew()
        self.fallanimationgroup.finished.connect(self.displaywinnersnew)
        
        
        # self.displaywinners()
    

    def printvisibility(self):
        """Print the visibility setting of the labels. 
        """        
        this_arr = np.empty((5, 6))
        for x in range(5):
            for y in range(6):
                thislabel: CustomLabels = self.label_array[x, y]
                this_arr[x, y] = thislabel.windowOpacity()
        print(this_arr)

    
    def enablestart(self):
        self.start_btn.setEnabled(True)
        self.update_balance()

    
    def displaywinnersnew(self):
        """Displaywinners checks the displayarray for winning lines and creates two animationgroups for the labels that belong to winning lines.
            the animationgroups for straight lines and Animations for zigzag lines are added to a sequential animationgroup.
        """        
        straight_arr, zigzag_arr, totalwin = self.playingfield.checkwinnings(betsize=self.betsizes[self.betbutton.currentIndex()])
        arrlist = [straight_arr, zigzag_arr]
        self.anim_group = [QParallelAnimationGroup(self), QParallelAnimationGroup(self)]
        self.sequantialanimgroup = QSequentialAnimationGroup(self)
        
        self.sequantialanimgroup.finished.connect(self.enablestart)
        for i, linearray in enumerate(arrlist):
            self.anim_group[i].clear()
            
            if np.any(linearray):
                
                for x in np.argwhere(linearray):
                    
                    self.label: CustomLabels = self.label_array[x[0]][x[1]]
                    #print(i)
                    
                    self.anim_group[i].addAnimation(self.label.animation2)
                    
                #self.anim_group[i].start()
                self.sequantialanimgroup.addAnimation(self.anim_group[i])
        

        if totalwin > 0:
            self.lastwin = totalwin
            
            self.sequantialanimgroup.finished.connect(self.signal1.emit)
            self.sequantialanimgroup.updateState(QAbstractAnimation.State.Running, QAbstractAnimation.State.Stopped)
            self.sequantialanimgroup.start()
            
        else:
            self.signal2.emit()

    
        


    def createfallanimation(self):
        """Creates the fallinganimation that is used whenever a new playingfield is generated.
        The animation is an attribute of the customlabels and only needs to be generated once for each label in the labelarray.
        """        
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
        """Creates the winning animation that is used for labels that are part of a winning combination.
        The animation is an attribute of the customlabels and only needs to be generated once for each label in the labelarray.
        """        
        for x in range(5):
            for y in range(6):
                self.label: CustomLabels = self.label_array[x, y]
                self.label.animation2.setKeyValueAt(0, QRect(self.label.shiftedpos, QSize(0, 0)))
                self.label.animation2.setKeyValueAt(0.25,QRect(self.label.currentpos, QSize(80, 96)))
                self.label.animation2.setKeyValueAt(0.60, QRect(self.label.shiftedpos, QSize(0, 0)))
                self.label.animation2.setKeyValueAt(1, QRect(self.label.currentpos, QSize(80, 96)))
                self.label.animation2.setDuration(800)



    def textinwindownew(self, text, xpos, index):
        """Set a new image for the customlabel that corresponds to the value at that specific slot.

        Args:
            text (list[str]): List of the displayvalues of one of the reels.
            xpos (None): not used (for now)
            index (int): Index of the column where the reel is, between 0 and 5.
        """        
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
            self.fallanimationgroup.start()
    

    def winpopup(self):
        if self.dlg_off:
            self.dlg = QtWidgets.QDialog(self)
            self.dlg.setWindowTitle(f"You win!")
            self.dlg.resize(QSize(100, 25))
            label = QtWidgets.QLabel(text=f"You win ${self.lastwin:.2f}")
            label.setParent(self.dlg)
            self.dlg_off = False
            label.show()
            self.dlg.show()
            self.bank.add_winnings(self.lastwin)
            self.update_balance()
    
    
    def getridofpopup(self):
        try:
            self.dlg.destroy()
            self.dlg_off = True
        except AttributeError:
            pass

    def startanimationgroup(self):
        self.animationgroup.start()



class CustomLabels(QtWidgets.QLabel):
    """Custom label class used for easier animations in the slot machine.

    Args:
        QtWidgets (_type_): _description_
    """    

    

    def __init__(self):
        

        super().__init__()

        self.animated = False
        self.pathname = "src/SlotMachine/images/"
        self.pixmap1 = QPixmap()
        self.animation = QPropertyAnimation(self, b"pos", self)
        self.animation2 = QPropertyAnimation(self, b"geometry", self)
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
        """Used set a different image on the label.

        Args:
            filename (str): The dictionary key for the images.
        """        
        
        self.pixmap1 = QPixmap()
        choices = {
            "A":"acecard.jpg",
            "K": "kheart.jpg",
            "Q": "qheart.jpg",
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