from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QPoint, QSize
import PySide6.QtCore as Core
from PySide6.QtCore import QSequentialAnimationGroup, QAbstractAnimation
from src.baccarat.baccarat_animations import BaccaratCard
from src.extrafiles.backgroundwidget import BaccaratBackground
from src.baccarat.baccarat_table_handler import BaccaratTable
from src.baccarat.baccarat_cards import Card
from src.baccarat.baccarat_rules_handler import ActionState,OutComeTypes
from src.extrafiles.BaccaratButtons import BaccaratFiche, BaccaratFicheOptionMenu
from src.baccarat.BaccaratBank import Bank
from src.baccarat.BankingErrors import BalanceError, ZeroBetsPlacedError
import sys


class BaccaratGui(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        self.central_widget = BaccaratBackground()
        self.central_widget.setParent(self)
        self.central_widget.resize(QSize(1200, 600))
        self.resize(1200, 700)

        self.banker_left_right_x = [690, 790]                            # Xpositions for bankers cards
        self.player_left_right_x = [328, 428]                            # Xpositions for players cards
        self.label_ypos          = 118                                   # right in the middle of the box
        self.player_label        = QtWidgets.QLabel(self)                # Used to update and display the players points
        self.banker_label        = QtWidgets.QLabel(self)                # Used to update and display the bankers points
        self.Balance_Label       = QtWidgets.QLabel(self)                # Used to display the players current balance and total betsize
        self.BetSizeDialog       = BaccaratFicheOptionMenu(self)         # Dialog window to choose a betsize
        self.OpenBetSizeMenu     = QtWidgets.QPushButton(text="BetSize") 
        self.start_btn           = QtWidgets.QPushButton(text="PLAY")
        self.BetPlayer           = QtWidgets.QPushButton(text="Player")
        self.BetBanker           = QtWidgets.QPushButton(text="Banker")
        self.BetTie              = QtWidgets.QPushButton(text="Tie 8:1")


        self.CurrentBetSizeImage = BaccaratFiche()
        self.all_cards           = []
        self.bank                = Bank(500)
        self.bank.BetSize        = 1
        self.table               = BaccaratTable()


        self.CurrentBetSizeImage.setEnabled(False)
        self.CurrentBetSizeImage.SetOneValueFiche()

        
        self.player_label.setParent(self)
        self.banker_label.setParent(self)
        self.start_btn.setParent(self)
        self.Balance_Label.setParent(self)
        self.OpenBetSizeMenu.setParent(self)
        self.CurrentBetSizeImage.setParent(self)
        self.BetPlayer.setParent(self)
        self.BetBanker.setParent(self)
        self.BetTie.setParent(self)

        self.player_label.resize(QSize(100, 50))
        self.banker_label.resize(QSize(100, 50))
        self.Balance_Label.resize(QSize(300, 100))

        self.player_label.move(QPoint(300, 50))
        self.banker_label.move(QPoint(790, 50))
        self.Balance_Label.move(QPoint(0, 600))

        self.player_label.setStyleSheet("border: 2px solid gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
        self.banker_label.setStyleSheet("border: 2px solid gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
        self.Balance_Label.setStyleSheet("border : 2px solid black ; border-radius 2px ; font : bold 20px ; background : grey")

        self.start_btn.resize(QSize(100, 50))
        self.OpenBetSizeMenu.resize(QSize(100, 50))
        self.CurrentBetSizeImage.resize(QSize(100, 50))

        self.start_btn.move(QPoint(550, 650))
        self.OpenBetSizeMenu.move(QPoint(450, 650))
        self.CurrentBetSizeImage.move(QPoint(350, 650))


        self.BetPlayer.resize(QSize(328, 355))
        self.BetBanker.resize(QSize(333, 355))
        self.BetTie.resize(QSize(470, 175))

        self.BetPlayer.move(QPoint(40, 225))
        self.BetBanker.move(QPoint(835, 225))
        self.BetTie.move(QPoint(368, 225))

        self.BetPlayer.setStyleSheet("color: blue ; font : bold 50px ; background: green")
        self.BetBanker.setStyleSheet("color: red ; font: bold 50px ; background : green")
        self.BetTie.setStyleSheet("color: white  ; font : bold 50px ; background : lightgreen")

        self.start_btn.show()
        self.player_label.show()
        self.banker_label.show()

        self.start_btn.clicked.connect(self.Replay)    
        self.start_btn.clicked.connect(self.StartRound)

        self.table.PointsChanged.connect(self.UpdatePoints)
        self.table.FirstAnimSignal.connect(self.FirstAnimations)
        self.table.CardDrawnSignal.connect(self.PlaceNewCard)
        self.table.WinnerSignal.connect(self.announcewinner)
        self.table.WinnerSignal.connect(self.savewinners)

        self.OpenBetSizeMenu.clicked.connect(self.ShowBetSizeMenu)
        self.BetSizeDialog.BetSizeSignal.connect(self.ChangeCurrentBetSize)

        self.BetPlayer.clicked.connect(self.PlaceBetPlayer)
        self.BetBanker.clicked.connect(self.PlaceBetBanker)
        self.BetTie.clicked.connect(self.PlaceBetTie)

        self.bank.BalanceChanged.connect(self.UpdateBalanceLabel)
        self.UpdateBalanceLabel()

    def BalanceErrorPopup(self, error, error_message):
        self.BalancePopUpLabel = QtWidgets.QLabel()
        self.error_timer       = Core.QTimer(self.BalancePopUpLabel)

        self.BalancePopUpLabel.setWindowTitle(f"{error}")
        self.BalancePopUpLabel.setText(f"{error_message}")
        self.BalancePopUpLabel.setParent(self)

        self.BalancePopUpLabel.setStyleSheet("color: darkblue ; font : bold 20px")
        self.BalancePopUpLabel.move(QPoint(400, 50))
        self.BalancePopUpLabel.width = 1200
        self.BalancePopUpLabel.setFixedWidth(1000)

        self.error_timer.setSingleShot(True)
        self.error_timer.setInterval(1500)
        self.error_timer.timeout.connect(self.BalancePopUpLabel.deleteLater)

        self.BalancePopUpLabel.show()
        self.error_timer.start()
        

    @Slot()
    def DestroyErrorPopUp(self):
        self.BalancePopUpLabel.close()

    @Slot()
    def UpdatePlayerLabel(self):
        """Called when the players points have changed
        """        
        self.player_label.clear()
        points = self.table.player.CalculatePoints()
        self.player_label.setText(f"PLAYER POINTS: {points}")
        self.player_label.update()
    
    @Slot()
    def UpdateBankerLabel(self):
        """Called when the Bankers points have changed
        """        
        self.banker_label.clear()
        points = self.table.banker.CalculatePoints()
        self.banker_label.setText(f"BANKER POINTS: {points}")
        self.banker_label.update()

    @Slot(int)
    def UpdateBalanceLabel(self):
        self.Balance_Label.clear()
        self.Balance_Label.setText(f"Current balance: ${self.bank.Balance} \n Total bet: {self.bank.TotalBet / 100}")
        self.Balance_Label.update()

    @Slot()
    def PlaceBetPlayer(self):
        try:
            self.bank.PlaceBet(who=OutComeTypes.PLAYER)
        except BalanceError as e:
            print(e.with_traceback, e.__str__)
            self.BalanceErrorPopup(e.__doc__, e.__str__())
    
    @Slot()
    def PlaceBetBanker(self):
        try:    
            self.bank.PlaceBet(who=OutComeTypes.BANKER)
        except BalanceError as e:
            print(e.with_traceback, e.__str__)
            self.BalanceErrorPopup(e.__doc__, e.__str__())
    
    @Slot()
    def PlaceBetTie(self):
        try:
            self.bank.PlaceBet(who=OutComeTypes.TIE)
        except BalanceError as e:
            print(e.with_traceback, e.__str__)
            self.BalanceErrorPopup(e.__doc__, e.__str__())

    @Slot(int, name="BetSize")
    def ChangeCurrentBetSize(self, signal):
        if signal == 1:
            self.CurrentBetSizeImage.SetOneValueFiche()
        elif signal == 5:
            self.CurrentBetSizeImage.SetFiveValueFiche()
        elif signal == 25:
            self.CurrentBetSizeImage.SetTwentyFiveValueFiche()
        elif signal == 100:
            self.CurrentBetSizeImage.SetOneHundredValueFiche()
        self.bank.BetSize = signal
        self.CurrentBetSizeImage.update()
    
    @Slot()
    def ShowBetSizeMenu(self):
        self.BetSizeDialog.exec()

    @Slot(name="PointsChanged")
    def UpdatePoints(self):
        self.UpdatePlayerLabel()
        self.UpdateBankerLabel()

    
    
    def StartRound(self):
        """Starts a game of baccarat by giving 2 cards to the player and two to the banker
        """        
        self.StartingAnimationGroup = QSequentialAnimationGroup()
        self.SecondAnimGroup        = QSequentialAnimationGroup()

        try:
            self.table.PlayRound(self.bank)
        except ZeroBetsPlacedError as e:
            self.BalanceErrorPopup(e.__doc__, e.__str__())
        
        
    @Slot(name="Animations")    
    def FirstAnimations(self):
        self.banker_cards = self.table.banker_cards
        self.player_cards = self.table.player_cards
        for player_xpos, banker_xpos, player_card, banker_card in zip(self.player_left_right_x, self.banker_left_right_x, self.player_cards, self.banker_cards):

            self.CurrentPlayerCard = BaccaratCard()
            self.CurrentBankerCard = BaccaratCard()

            self.CurrentPlayerCard.setParent(self)
            self.CurrentBankerCard.setParent(self)

            self.CurrentPlayerCard.CreateAnimation(xposition=player_xpos, card=player_card)
            self.CurrentBankerCard.CreateAnimation(xposition=banker_xpos, card=banker_card)
            
            self.CurrentPlayerCard.show()
            self.CurrentBankerCard.show()

            self.StartingAnimationGroup.addAnimation(self.CurrentPlayerCard.animation)
            self.StartingAnimationGroup.addAnimation(self.CurrentBankerCard.animation)

            self.all_cards.append(self.CurrentBankerCard)
            self.all_cards.append(self.CurrentPlayerCard)
        
        self.StartingAnimationGroup.start()

    @Slot(Card)
    def PlaceNewCard(self, signal : Card):
        self.current_card = BaccaratCard()
        self.current_card.setParent(self)
        
        if self.table.CurrentState == ActionState.PLAYERTURN:
            xposition = 228
        
        elif self.table.CurrentState == ActionState.BANKERTURN:
            xposition = 890
        
        self.current_card.CreateAnimation(xposition, signal)
        self.current_card.show()
        self.SecondAnimGroup.addAnimation(self.current_card.animation)
        self.StartingAnimationGroup.finished.connect(self.SecondAnimGroup.start)
        self.SecondAnimGroup.finished.connect(self.UpdatePoints)
        self.all_cards.append(self.current_card)


    def announcewinner(self):
        
        if self.SecondAnimGroup.state() == QAbstractAnimation.State.Running:
            self.SecondAnimGroup.finished.connect(self.DeclareWinner, type=Core.Qt.ConnectionType.SingleShotConnection)
        else:
            self.StartingAnimationGroup.finished.connect(self.DeclareWinner, type=Core.Qt.ConnectionType.SingleShotConnection)


    @Slot(OutComeTypes, name="winner")
    def savewinners(self, signal1 : OutComeTypes):
        self.result = signal1
    
        
    def DeclareWinner(self):

        self.LastTotalWinCredits = self.bank.CheckTotalWin(self.result)
        TotalWinEuros = (self.LastTotalWinCredits / 100)

        self.dlg = QtWidgets.QDialog(self)
        self.dlg.setWindowTitle(f"WINNER")

        lbl = QtWidgets.QLabel(text=f"winner {self.result.name} \n You win ${TotalWinEuros}")
        lbl.setParent(self.dlg)

        self.dlg.resize(QSize(300, 150))
        lbl.resize(QSize(200, 100))
        self.dlg.show()
        

    @Slot()
    def Replay(self):
        try:
            self.table.ResetTable()
            for card in self.all_cards:
                card : BaccaratCard
                card.deleteLater()
            self.all_cards = []
        except AttributeError:
            pass
        


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = BaccaratGui()
    ui.show()
    app.exec()


if __name__ == "__main__":
    main()

    