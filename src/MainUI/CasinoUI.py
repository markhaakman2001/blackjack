from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Slot, Signal
from src.blackjack.gui import BJinterface
from src.blackjack.gui_shoehand import BlackJackBank as BJBank
from src.baccarat.baccarat import BaccaratGui
from src.baccarat.BaccaratBank import BaccaratBank
from src.SlotMachine.SlotGui import SlotMachineGUI
from src.SlotMachine.slot_generator import BankAccount
from src.UnifiedBanking.UnifiedBank import MainBank
import sys
import time

class CasinoUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.MainBank    = MainBank()
        self.BlackJack   = BJinterface()
        self.Baccarat    = BaccaratGui()
        self.SlotMachine = SlotMachineGUI()

        self.central_widget = QtWidgets.QWidget()
        self.MainBank.DepositMoney(100)

        self.resize(1000, 700)
        self.setCentralWidget(self.central_widget)

        self.BlackJackButton  = QtWidgets.QPushButton(text="BlackJack")
        self.BaccaratButton   = QtWidgets.QPushButton(text="Baccarat")
        self.SlotButton       = QtWidgets.QPushButton(text="Slot Machine")

        self.BlackJackButton.resize(100, 80)
        self.BaccaratButton.resize(100, 80)
        self.SlotButton.resize(100, 80)

        self.BlackJackButton.move(QtCore.QPoint(0, 50))
        self.BaccaratButton.move(QtCore.QPoint(100, 50))
        self.SlotButton.move(QtCore.QPoint(200, 50))

        self.BlackJackButton.setParent(self)
        self.BaccaratButton.setParent(self)
        self.SlotButton.setParent(self)

        self.BlackJackButton.clicked.connect(self.OpenBlackJack)
        self.BaccaratButton.clicked.connect(self.OpenBaccarat)
        self.SlotButton.clicked.connect(self.OpenSlotMachine)
    
    
    def OpenBlackJack(self):
        self.BlackJack.show()

    def OpenBaccarat(self):
        self.Baccarat.show()

    def OpenSlotMachine(self):
        self.SlotMachine.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    Casino = CasinoUI()
    Casino.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()