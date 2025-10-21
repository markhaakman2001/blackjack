from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QSize, QPoint, QSequentialAnimationGroup, QParallelAnimationGroup
import PySide6.QtCore as Core
from CustomUIfiles import EasyCardLabels, BackGroundWidget, BaccaratFiche, BaccaratFicheOptionMenu, BlackJackBetButton, WhichButton, BetButtonType
from ErrorFiles.PlayingErrors import PlayingError,  BlackJackErrorChecker
from ErrorFiles.BankingErrors import BankingErrorChecker,  BalanceError,  BettingError
from UnifiedBanking.UnifiedBank import MainBank
from extrafiles.gametrackingtools import GameState
from blackjack.player import BlackJackPlayer, BlackJackDealer
from blackjack.gui_hand import BlackJackHand, BlackJackSplitHand
from blackjack.BJanimations import BlackJackAnimatedCard
from blackjack.gui_table2 import BlackJackTable
from baccarat.baccarat_cards import Card, CardSymbol, Color, Kind, Shoe, DeckOfCards
import sys





class BlackJackGUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.table = BlackJackTable()
        self.central_widget = BackGroundWidget()
        self.setCentralWidget(self.central_widget)
        self.resize(1000, 700)
        self.central_widget.resize(QSize(1000, 700))


        # THIS IS A TEST BUTTON
        self.testbutton = QtWidgets.QPushButton(text="test", parent=self)
        self.testbutton.move(QPoint(0, 0))
        self.testbutton.show()
        self.testbutton.clicked.connect(self.start_round_test)
    
    @Slot()
    def start_round_onehand(self):
        self.animgroup = QParallelAnimationGroup()
        
        player_cards, dealer_cards = self.table.StartRound_onehand()
        for player_card, dealer_card in zip(player_cards, dealer_cards):
            self.card = BlackJackAnimatedCard()
            self.card.setParent(self)
            
            self.card2 = BlackJackAnimatedCard()
            self.card2.setParent(self)
            self.card.TestAnimation(player_card)
            self.card2.TestAnimation(dealer_card, 500)
            self.card.show()
            self.card2.show()
            self.animgroup.addAnimation(self.card.animation)
            self.animgroup.addAnimation(self.card2.animation)
        
        self.animgroup.start()
    
    @Slot()
    def start_round_test(self):
        self.cards, self.animgroup = self.table.StartNhand()
        for card in self.cards:
            card : EasyCardLabels
            card.setParent(self)
            card.show()
        self.animgroup.start()
            
