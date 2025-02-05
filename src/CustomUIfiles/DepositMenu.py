from PySide6 import QtWidgets
from PySide6.QtWidgets import  QDialog, QPushButton, QDoubleSpinBox
from PySide6.QtCore import Signal, QPoint, QSize, Slot
from PySide6.QtGui import QPixmap, QIcon


class DepositMenu(QDialog):

    AmountConfirmed = Signal(int, name="AmountConfirmed")

    def __init__(self):
        super().__init__()
        self.resize(200, 150)

        self.DepositTen         = QPushButton(text="10")
        self.DepositTwentyfive  = QPushButton(text="25")
        self.DepositFifty       = QPushButton(text="50")
        self.DepositOneHundred  = QPushButton(text="100")

        self.ConfirmButton     = QPushButton(text="Confirm")

        self.DepositSpinBox     = QDoubleSpinBox(self)
        
        self.DepositTen.resize(50, 50)
        self.DepositTwentyfive.resize(50, 50)
        self.DepositFifty.resize(50, 50)
        self.DepositOneHundred.resize(50, 50)

        self.ConfirmButton.resize(200, 50)

        self.DepositTen.move(0, 50)
        self.DepositTwentyfive.move(50, 50)
        self.DepositFifty.move(100, 50)
        self.DepositOneHundred.move(150, 50)

        self.ConfirmButton.move(0, 100)

        self.DepositTen.setParent(self)
        self.DepositTwentyfive.setParent(self)
        self.DepositFifty.setParent(self)
        self.DepositOneHundred.setParent(self)

        self.ConfirmButton.setParent(self)

        self.DepositTen.show()
        self.DepositTwentyfive.show()
        self.DepositFifty.show()
        self.DepositOneHundred.show()

        self.ConfirmButton.show()

        self.DepositTen.clicked.connect(self.UpdateAmountTen)
        self.DepositTwentyfive.clicked.connect(self.UpdateAmountTwentyFive)
        self.DepositFifty.clicked.connect(self.UpdateAmountFifty)
        self.DepositOneHundred.clicked.connect(self.UpdateAmountOneHundred)

        self.ConfirmButton.clicked.connect(self.ConfirmDeposit)

        self.DepositSpinBox.setValue(50)
        self.DepositSpinBox.setMinimum(10)
        self.DepositSpinBox.setMaximum(5000)

        self.DepositSpinBox.resize(200, 50)

        self.DepositSpinBox.show()
    
    def ConfirmDeposit(self):
        DepositAmount  = self.DepositSpinBox.value()
        self.AmountConfirmed.emit(DepositAmount)
        self.accept()

    def UpdateAmountTen(self):
        self.DepositSpinBox.setValue(10)
    
    def UpdateAmountTwentyFive(self):
        self.DepositSpinBox.setValue(25)
    
    def UpdateAmountFifty(self):
        self.DepositSpinBox.setValue(50)
    
    def UpdateAmountOneHundred(self):
        self.DepositSpinBox.setValue(100)





