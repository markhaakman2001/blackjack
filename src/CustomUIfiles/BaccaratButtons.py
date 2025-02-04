from PySide6 import QtWidgets
from PySide6.QtWidgets import  QDialog
from PySide6.QtCore import Signal, QPoint, QSize, Slot
from PySide6.QtGui import QPixmap, QIcon


class BaccaratFicheOptionMenu(QDialog):
    """Simple Qdialog that opens a window with 4 pushbuttons. used to choose the amount to place for a bet.

    """
    BetSizeSignal = Signal(int, name="BetSize")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(250, 250)

        self._BetSize_         = 1
        
        self.one_fiche         = BaccaratFiche()
        self.five_fiche        = BaccaratFiche()
        self.twentyfive_fiche  = BaccaratFiche()
        self.onehundred_fiche  = BaccaratFiche()

        self.one_fiche.SetOneValueFiche()
        self.five_fiche.SetFiveValueFiche()
        self.twentyfive_fiche.SetTwentyFiveValueFiche()
        self.onehundred_fiche.SetOneHundredValueFiche()

        self.one_fiche.setParent(self)
        self.five_fiche.setParent(self)
        self.twentyfive_fiche.setParent(self)
        self.onehundred_fiche.setParent(self)
        
        self.one_fiche.resize(QSize(125, 125))
        self.five_fiche.resize(QSize(125, 125))
        self.twentyfive_fiche.resize(QSize(125, 125))
        self.onehundred_fiche.resize(QSize(125, 125))

        self.one_fiche.move(QPoint(0, 0))
        self.five_fiche.move(QPoint(125, 0))
        self.twentyfive_fiche.move(QPoint(0, 125))
        self.onehundred_fiche.move(QPoint(125,125))

        self.one_fiche.ButtonValueSignal.connect(self.SendBetSizeSignal)
        self.five_fiche.ButtonValueSignal.connect(self.SendBetSizeSignal)
        self.twentyfive_fiche.ButtonValueSignal.connect(self.SendBetSizeSignal)
        self.onehundred_fiche.ButtonValueSignal.connect(self.SendBetSizeSignal)
    
    @Slot(int, name="ButtonValue")
    def SendBetSizeSignal(self, signal):
        self.BetSize = signal
        self.BetSizeSignal.emit(signal)
    
    @property
    def BetSize(self):
        return self._BetSize_
    
    @BetSize.setter
    def BetSize(self, Size):
        self._BetSize_ = Size
    
    @BetSize.deleter
    def BetSize(self):
        self._BetSize_ = 1

class BaccaratFiche(QtWidgets.QPushButton):
    """Class that is used for displaying different valued fiches that function as Qpushbuttons

    
    """    

    ButtonValueSignal = Signal(int, name="ButtonValue")

    def __init__(self):
        super().__init__()
        self._pixmap = QPixmap()
        self._value  = 0
        self.clicked.connect(self.SendCurrentValue)
        
    
    def SetOneValueFiche(self):
        self._pixmap.load("customimages/baccaratImage/1casinochip.jpg")

        self._icon = QIcon(self._pixmap)
        self.icon = self._icon
        self.setIcon(self.icon)
        self.setIconSize(QSize(100, 100))
        self._value = 1
    
    def SetFiveValueFiche(self):
        self._pixmap.load("customimages/baccaratImage/5casinochip.jpg")

        self._icon = QIcon(self._pixmap)
        self.icon = self._icon
        self.setIcon(self.icon)
        self.setIconSize(QSize(100, 100))
        self._value = 5
    
    def SetTwentyFiveValueFiche(self):
        self._pixmap.load("customimages/baccaratImage/25casinochip.jpg")

        self._icon = QIcon(self._pixmap)
        self.icon = self._icon
        self.setIcon(self.icon)
        self.setIconSize(QSize(100, 100))
        self._value = 25
    
    def SetOneHundredValueFiche(self):
        self._pixmap.load("customimages/baccaratImage/100casinochip.jpg")

        self._icon = QIcon(self._pixmap)
        self.icon = self._icon
        self.setIcon(self.icon)
        self.setIconSize(QSize(100, 100))
        self._value = 100
    
    def SendCurrentValue(self):
        self.ButtonValueSignal.emit(self._value)