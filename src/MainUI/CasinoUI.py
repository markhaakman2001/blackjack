from PySide6 import QtWidgets, QtCore
from src.blackjack.gui import BJinterface
from src.baccarat.baccarat import BaccaratGui
from src.SlotMachine.SlotGui import SlotMachineGUI
from src.mines.minesUI import MinesUI
from src.UnifiedBanking.UnifiedBank import MainBank
from src.extrafiles.gametrackingtools import gt, GameState
from src.ErrorFiles.mainUIErrors import MainUIErrorChecker, ActiveGameError
from src.CustomUIfiles.DepositMenu import DepositMenu
import sys

class CasinoUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.MainBank    = MainBank(1000)

        self.BlackJack   = BJinterface(self.MainBank)
        self.Baccarat    = BaccaratGui(self.MainBank)
        self.SlotMachine = SlotMachineGUI(self.MainBank)
        self.Mines       = MinesUI(self.MainBank)

        self.central_widget = QtWidgets.QWidget()

        self.resize(1000, 700)
        self.setCentralWidget(self.central_widget)

        self.BlackJackButton  = QtWidgets.QPushButton(text="BlackJack")
        self.BaccaratButton   = QtWidgets.QPushButton(text="Baccarat")
        self.SlotButton       = QtWidgets.QPushButton(text="Slot Machine")
        self.MinesButton      = QtWidgets.QPushButton(text="mines")
        self.DepositButton    = QtWidgets.QPushButton(text="RUN \n IT \n BACK")

        self.BlackJackButton.resize(100, 80)
        self.BaccaratButton.resize(100, 80)
        self.SlotButton.resize(100, 80)
        self.MinesButton.resize(100, 80)
        self.DepositButton.resize(100, 80)

        self.BlackJackButton.move(QtCore.QPoint(0, 50))
        self.BaccaratButton.move(QtCore.QPoint(100, 50))
        self.SlotButton.move(QtCore.QPoint(200, 50))
        self.MinesButton.move(QtCore.QPoint(300, 50))
        self.DepositButton.move(QtCore.QPoint(400, 50))

        self.BlackJackButton.setParent(self)
        self.BaccaratButton.setParent(self)
        self.SlotButton.setParent(self)
        self.MinesButton.setParent(self)
        self.DepositButton.setParent(self)

        self.BlackJackButton.clicked.connect(self.OpenBlackJack)
        self.BaccaratButton.clicked.connect(self.OpenBaccarat)
        self.SlotButton.clicked.connect(self.OpenSlotMachine)
        self.MinesButton.clicked.connect(self.OpenMines)
        self.DepositButton.clicked.connect(self.OpenDeposit)

        self.BJDialogWindow   = QtWidgets.QDialog(self)
        self.BacDialogWindow  = QtWidgets.QDialog(self)
        self.SlotDialogWindow = QtWidgets.QDialog(self)
        self.MineDialogWindow = QtWidgets.QDialog(self)
        self.DepositDialog    = DepositMenu()

        self.BJDialogWindow.resize(1000, 700)
        self.BacDialogWindow.resize(1200, 700)
        self.SlotDialogWindow.resize(900, 700)
        self.MineDialogWindow.resize(1000, 700)

        self.BlackJack.setParent(self.BJDialogWindow)
        self.Baccarat.setParent(self.BacDialogWindow)
        self.SlotMachine.setParent(self.SlotDialogWindow)
        self.Mines.setParent(self.MineDialogWindow)
        self.DepositDialog.AmountConfirmed.connect(self.MakeDeposit)

        self.games_dict : dict = {self.BlackJack : gt.BLACKJACK,
                                   self.Baccarat : gt.BACCARAT, 
                                   self.SlotMachine : gt.SLOTMACHINE, 
                                   self.Mines : gt.MINES
                                   }


    @QtCore.Slot(float, name="AmountConfirmed")
    def MakeDeposit(self, signal : float):
        self.MainBank.DepositMoney(signal)

    def OpenDeposit(self):
        self.DepositDialog.exec()

    @MainUIErrorChecker._CheckActiveGamesnew
    def testactivegames(self, game : gt):
        pass
    
    
    def OpenMines(self):
        self.Mines.UpdateFunds()
        try:
            self.testactivegames(gt.MINES)
        except ActiveGameError as e:
            print(e.__str__())
        else:
            self.MineDialogWindow.exec()


    def OpenBlackJack(self):
        self.BlackJack.update_funds()
        try:
            self.testactivegames(gt.BLACKJACK)
        except ActiveGameError as e:
            print(e.__str__())
        else:
            self.BJDialogWindow.exec()

    def OpenBaccarat(self):
        self.Baccarat.UpdateBalanceLabel()
        try:
            self.testactivegames(gt.BACCARAT)
        except ActiveGameError as e:
            if e.game == gt.BACCARAT:
                self.BacDialogWindow.exec()
            else: 
                print(e.__str__())
        else:
            self.BacDialogWindow.exec()
            

    def OpenSlotMachine(self):
        try:
            self.testactivegames(gt.SLOTMACHINE)
        except ActiveGameError as e:
            if e.game == gt.SLOTMACHINE:
                self.SlotDialogWindow.exec()
            else:
                print(e.__str__())
        else:
            self.SlotDialogWindow.exec()


def main():
    app = QtWidgets.QApplication(sys.argv)
    Casino = CasinoUI()
    Casino.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()