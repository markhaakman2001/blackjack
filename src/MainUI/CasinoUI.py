from PySide6 import QtWidgets, QtCore
from src.blackjack.gui import BJinterface
from src.blackjack.gui_shoehand import Bank as BJBank
from src.baccarat.baccarat import BaccaratGui
from src.baccarat.BaccaratBank import Bank
from src.SlotMachine.SlotGui import SlotMachineGUI
from src.SlotMachine.slot_generator import BankAccount
from src.UnifiedBanking.UnifiedBank import MainBank
import sys
import time

class CasinoUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.BlackJack   = BJinterface()
        self.Baccarat    = BaccaratGui()
        self.SlotMachine = SlotMachineGUI()

        self.central_widget = QtWidgets.QWidget()
        self.resize(1000, 700)
        self.setCentralWidget(self.central_widget)



def main():
    app = QtWidgets.QApplication(sys.argv)
    Casino = CasinoUI()
    Casino.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()