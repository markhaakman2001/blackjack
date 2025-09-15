from PySide6 import QtWidgets
from PySide6.QtWidgets import  QDialog
from PySide6.QtCore import Signal, QPoint, QSize, Slot
from PySide6.QtGui import QPixmap, QIcon
import sys
import os


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
        self._icon_pixmap = QPixmap()
        self._value  = 0
        self.clicked.connect(self.SendCurrentValue)
    

    def _set_chip_image(self, relative_path, value):
        base_path = os.path.dirname(__file__)  # Path to this file
        full_path = os.path.join(base_path, relative_path)

        self._icon_pixmap.load(relative_path)
        if self._icon_pixmap.isNull():
            print(f"❌ Failed to load image: {full_path}")
            return

        # Apply icon
        self.setIcon(QIcon(self._icon_pixmap))
        self.setIconSize(QSize(100, 100))
        self._value = value

    
    def SetOneValueFiche(self):
        self._set_chip_image("src/extrafiles/baccaratImagePNG/1casinochip.png", 1)
        # self._icon_pixmap.load("extrafiles/baccaratImage/1casinochip.jpg")

        # self._icon_pixmap = QPixmap("src/extrafiles/baccaratImage/25casinochip.jpg"  )
        # # self._icon = QIcon(self._pixmap)
        # # self.icon = self._icon
        # self.setIcon(QIcon(self._icon_pixmap))
        # self.setIconSize(QSize(100, 100))
        # self._value = 1
    
    def SetFiveValueFiche(self):
        self._icon_pixmap.load("src/extrafiles/baccaratImagePNG/5casinochip.png")

        self._icon = QIcon(self._icon_pixmap)
        self.setIcon(self._icon)
        self.setIconSize(QSize(100, 100))
        self._value = 5
    
    def SetTwentyFiveValueFiche(self):
        self._icon_pixmap.load("src/extrafiles/baccaratImagePNG/25casinochip.png")

        self._icon = QIcon(self._icon_pixmap)
        self.setIcon(self._icon)
        self.setIconSize(QSize(100, 100))
        self._value = 25
    
    def SetOneHundredValueFiche(self):
        self._icon_pixmap.load("src/extrafiles/baccaratImagePNG/100casinochip.png")

        self._icon = QIcon(self._icon_pixmap)
        self.setIcon(self._icon)
        self.setIconSize(QSize(100, 100))
        self._value = 100
    
    def SendCurrentValue(self):
        self.ButtonValueSignal.emit(self._value)


def main():
    print("Working dir:", os.getcwd())  # Debug
    print("Image exists?", os.path.exists("src/extrafiles/baccaratImagePNG/25casinochip.png"))

if __name__ == "__main__":
    main()
