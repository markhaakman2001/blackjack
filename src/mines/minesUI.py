from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Signal, Slot
from src.mines.minesgame import MinesGame
from src.extrafiles.gametrackingtools import GameState, gt
from src.UnifiedBanking.UnifiedBank import MainBank
from src.mines.minesbank import MinesBank
from src.ErrorFiles.minesErrors import MinesError, MinesErrorChecker
from src.ErrorFiles.BankingErrors import BalanceError, BankingErrorChecker
from math import trunc
import sys


class MinesUI(QtWidgets.QMainWindow):

    def __init__(self, main_bank : MainBank = MainBank(100)):
        super().__init__()
        self.central_widget = QtWidgets.QWidget()
        self.start_btn      = QtWidgets.QPushButton(text="start")
        self.nMines         = QtWidgets.QSpinBox(self.central_widget)
        self.bet_euros      = QtWidgets.QSpinBox(self.central_widget)
        self.funds_lbl      = QtWidgets.QLabel(self.central_widget)

        self.mines_game     = MinesGame()
        self._gamestate     = GameState.INACTIVE
        self.bank           = MinesBank(main_bank)
        self.button_list    = []

        self.start_btn.setParent(self.central_widget)

        self.start_btn.resize(100, 100)
        self.bet_euros.resize(100, 50)
        self.nMines.resize(100, 50)

        self.bet_euros.move(QtCore.QPoint(0, 150))
        self.nMines.move(QtCore.QPoint(0, 100))
        self.nMines.setValue(1)
        self.nMines.setMaximum(10)
        self.nMines.setMinimum(1)

        self.bet_euros.setValue(1)
        self.bet_euros.setMaximum(100)
        self.bet_euros.setMinimum(1)

        self.bet_euros.valueChanged.connect(self.UpdateBetSize)
        self.start_btn.clicked.connect(self.start_game)

        self.nMines.show()
        self.start_btn.show()

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
                except MinesError as e:
                    self.ErrorPopUp(e.__doc__, e.__str__())
    
    def GameEnd(self):
        self._GameState_ = GameState.INACTIVE
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