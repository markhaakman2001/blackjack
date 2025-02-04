from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Slot, Signal
from src.blackjack.gui import BJinterface
from src.blackjack.gui_shoehand import BlackJackBank as BJBank
from src.baccarat.baccarat import BaccaratGui
from src.baccarat.BaccaratBank import BaccaratBank
from src.SlotMachine.SlotGui import SlotMachineGUI
from src.SlotMachine.slot_generator import BankAccount
from src.UnifiedBanking.UnifiedBank import MainBank
from src.ErrorFiles.mainUIErrors import MainUIErrorChecker, ActiveGameError
import sys
import time

class CasinoTestWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.MainBank    = MainBank(1000)

        self.BlackJack   = BJinterface(self.MainBank)
        self.Baccarat    = BaccaratGui(self.MainBank)
        self.SlotMachine = SlotMachineGUI(self.MainBank)

        self.central_widget = QtWidgets.QWidget()

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

        self.GameDialogWindow = QtWidgets.QDialog(self)
        self.GameDialogWindow.resize(1000, 700)
        self.BlackJack.setParent(self.GameDialogWindow)

    @MainUIErrorChecker._CheckForActiveGames_
    def testactivegames(self):
        pass
    
    def OpenBlackJack(self):
        try:
            self.testactivegames()
        except ActiveGameError as e:
            print(e.__str__())
        else:
            self.GameDialogWindow.exec()

    def OpenBaccarat(self):
        try:
            self.testactivegames()
        except ActiveGameError as e:
            print(e.__str__())
        else:
            self.Baccarat.show()

    def OpenSlotMachine(self):
        try:
            self.testactivegames()
        except ActiveGameError as e:
            print(e.__str__())
        else:
            self.SlotMachine.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    Casino = CasinoTestWindow()
    Casino.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()