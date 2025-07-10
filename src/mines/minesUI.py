from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Signal, Slot
from mines.minesgame import MinesGame
from extrafiles.gametrackingtools import GameState, gt
from UnifiedBanking.UnifiedBank import MainBank
from mines.minesbank import MinesBank
from ErrorFiles.minesErrors import MinesError, MinesErrorChecker
from ErrorFiles.BankingErrors import BalanceError, BankingErrorChecker
from math import trunc
import sys


class MinesUI(QtWidgets.QMainWindow):

    def __init__(self, main_bank : MainBank = MainBank(100)):
        super().__init__()
        self.central_widget = QtWidgets.QWidget()
        self.start_btn      = QtWidgets.QPushButton(text="start")
        self.cash_out       = QtWidgets.QPushButton(text="Cash Out")
        self.nMines         = QtWidgets.QSpinBox(self.central_widget)
        self.bet_euros      = QtWidgets.QSpinBox(self.central_widget)

        self.nMines_lbl     = QtWidgets.QLabel(self.central_widget)
        self.bet_lbl        = QtWidgets.QLabel(self.central_widget)

        self.funds_lbl      = QtWidgets.QLabel(self.central_widget)
        self.odds_lbl       = QtWidgets.QLabel(self.central_widget)


        self.mines_game     = MinesGame()
        self._gamestate     = GameState.INACTIVE
        self.bank           = MinesBank(main_bank)
        self.button_list    = []

        self.start_btn.setParent(self.central_widget)
        self.cash_out.setParent(self.central_widget)

        self.start_btn.resize(100, 100)
        self.cash_out.resize(100, 100)

        self.bet_euros.resize(100, 50)
        self.nMines_lbl.resize(50, 50)
        self.bet_lbl.resize(50, 50)
        self.funds_lbl.resize(200, 100)

        self.nMines.resize(100, 50)
        self.odds_lbl.resize(200, 50)


        self.bet_euros.move(QtCore.QPoint(0, 150))
        self.nMines.move(QtCore.QPoint(0, 100))
        self.nMines_lbl.move(QtCore.QPoint(100, 100))
        self.bet_lbl.move(QtCore.QPoint(100, 150))
        self.funds_lbl.move(QtCore.QPoint(0, 500))
        self.odds_lbl.move(QtCore.QPoint(0, 400))
        self.cash_out.move(QtCore.QPoint(0, 200))

        self.nMines.setValue(1)
        self.nMines.setMaximum(10)
        self.nMines.setMinimum(1)

        self.bet_euros.setValue(1)
        self.bet_euros.setMaximum(100)
        self.bet_euros.setMinimum(1)

        self.funds_lbl.setStyleSheet("border : 2px solid black ; border-radius 2px ; font : bold 20px ; background : grey")
        self.odds_lbl.setStyleSheet("border : 2px solid black ; border-radius 2px ; font : bold 10px ; background : grey")

        self.bet_euros.valueChanged.connect(self.UpdateBetSize)
        self.start_btn.clicked.connect(self.start_game)
        self.bank.BalanceChanged.connect(self.UpdateFunds)

        self.UpdateFunds()
        

        self.funds_lbl.update()
        self.odds_lbl.update()

        self.nMines.show()
        self.start_btn.show()
        self.funds_lbl.show()
        self.odds_lbl.show()

        self.setCentralWidget(self.central_widget)
        self.resize(1000, 700)
        self.CreateButtons()
    
    def CreateButtons(self):
        for x in range(25):
            xpos          = 250 + (x % 5) * 100
            ypos          = 100 + (trunc(x / 5)) * 100

            self.n_button = MinesButton(x)
            self.n_button.move(QtCore.QPoint(xpos, ypos))
            self.n_button.setParent(self)
            self.n_button.nButton.connect(self.CheckMine)
            self.button_list.append(self.n_button)
            self.n_button.show()
    
    def UpdateFunds(self):
        self.funds_lbl.clear()
        self.funds_lbl.setText(f"Balance: ${self.bank.funds_euros} \n")
        self.funds_lbl.update()

    def UpdateOddsLabel(self):
        if self._GameState_ == GameState.ACTIVE:
            odds = self.mines_game.OddsCalculator()
        else:
            odds = 0
        self.odds_lbl.clear()
        self.odds_lbl.setText(f"Total odds of getting this far: {odds:.2f}")
        self.odds_lbl.update()

    @Slot()
    def UpdateBetSize(self):
        BetSizeCredits = (self.bet_euros.value() * 100)
        self.bank._BetSize_ = BetSizeCredits

    @MinesErrorChecker._CheckActiveGames
    def CheckGame(self, checkfor : GameState):
        pass
    
    def start_game(self):
        try:
            self.CheckGame(GameState.ACTIVE)
        except MinesError as e:
            self.ErrorPopUp(e.__doc__, e.__str__())
        else:
            self.UpdateOddsLabel()
            self._GameState_  = GameState.ACTIVE
            n                 = self.nMines.value()
            self.bank.PlaceBet()

            for button in self.button_list:
                button : MinesButton
                button.UnCheck()
                button.setStyleSheet("background: grey")
                button.update()
            
            self.mines_game.CreateMines(n)
            print(self.mines_game.matrix)
    
    @Slot(int, name="nButton")
    def CheckMine(self, signal : int):
        try:
            self.CheckGame(GameState.INACTIVE)
        except MinesError as e:
            self.ErrorPopUp(e.__doc__, e.__str__())
        else:
            mine = self.mines_game.CheckMine(signal)

            if mine:
                self.GameEnd()
            else:
                try:
                    btn : MinesButton = self.button_list[signal]
                    btn.ChangeButtonToMine(mine)
                    self.mines_game.n_correct += 1
                    self.UpdateOddsLabel()
                except MinesError as e:
                    self.ErrorPopUp(e.__doc__, e.__str__())
    
    def GameEnd(self):
        self._GameState_ = GameState.INACTIVE
        self.UpdateOddsLabel()
        for x, button in enumerate(self.button_list):
            button : MinesButton
            if not button.MineChecked:
                button.ChangeButtonToMine(self.mines_game.CheckMine(x))

    def ErrorPopUp(self, error, error_message):
        self.ErrorPopUpLabel = QtWidgets.QLabel()
        self.error_timer       = QtCore.QTimer(self.ErrorPopUpLabel)

        self.ErrorPopUpLabel.setWindowTitle(f"{error}")
        self.ErrorPopUpLabel.setText(f"{error_message}")
        self.ErrorPopUpLabel.setParent(self)

        self.ErrorPopUpLabel.setStyleSheet("color: darkblue ; font : bold 20px")
        self.ErrorPopUpLabel.move(QtCore.QPoint(400, 50))
        self.ErrorPopUpLabel.width = 1200
        self.ErrorPopUpLabel.setFixedWidth(1000)

        self.error_timer.setSingleShot(True)
        self.error_timer.setInterval(1500)
        self.error_timer.timeout.connect(self.ErrorPopUpLabel.deleteLater)

        self.ErrorPopUpLabel.show()
        self.error_timer.start()
        

    @Slot()
    def DestroyErrorPopUp(self):
        self.ErrorPopUpLabel.close()


    @property
    def _GameState_(self) -> GameState:
        """Get the current state of the game

        Returns:
            GameState: active or inactive
        """       
        return self._gamestate

    @_GameState_.setter
    def _GameState_(self, newstate : GameState) -> None:
        self._gamestate = newstate 




class MinesButton(QtWidgets.QPushButton):

    nButton = Signal(int, name="nButton")

    def __init__(self, n_button):
        super().__init__()
        self.resize(100, 100)
        self.n_button = n_button
        self._Checked = False
        self.clicked.connect(self.n_button_signal)
    

    def n_button_signal(self):
        self.nButton.emit(self.n_button)
    
    @MinesErrorChecker._CheckRevealedMines
    def ChangeButtonToMine(self, mine : bool):
        self.MineChecked = True
        if mine:
            self.setStyleSheet("background: red")
        else:
            self.setStyleSheet("background: green")
        
        self.update()
    
    def UnCheck(self):
        self.MineChecked = False
    
    @property
    def MineChecked(self) -> bool:
        return self._Checked
    
    @MineChecked.setter
    def MineChecked(self, chk : bool) -> None:
        self._Checked = chk

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui  = MinesUI()
    ui.show()
    sys.exit(app.exec())