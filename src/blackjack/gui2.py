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
from blackjack.blackjackfunctions import UpdateType
import sys





class BlackJackGUI(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        self.table = BlackJackTable()
        self.central_widget = BackGroundWidget()
        self.setCentralWidget(self.central_widget)
        self.resize(1000, 700)
        self.central_widget.resize(QSize(1000, 700))

        self.table.add_observer(self.get_table_updates)

        self.active_hand = 0

        # THIS IS A TEST BUTTON
        self.testbutton = QtWidgets.QPushButton(text="test", parent=self)
        self.testbutton.move(QPoint(0, 0))
        self.testbutton.show()
        self.testbutton.clicked.connect(self.start_round_test)

        # Button used to hit an extra card on active hand
        self.hit_button = QtWidgets.QPushButton(text='hit', parent=self)
        self.hit_button.move(QPoint(0, 100))
        self.hit_button.show()
        self.hit_button.clicked.connect(self.hit)

        # button used to stand
        self.stand_button = QtWidgets.QPushButton(text='stand', parent=self)
        self.stand_button.move(QPoint(0, 150))
        self.stand_button.show()
        self.stand_button.clicked.connect(self.stand)

        #Add labels that show the total point value for each hand
        #---------
        self.dealer_handlabel = QtWidgets.QLabel(parent=self) # This is the dealers label
        self.dealer_handlabel.resize(QSize(80, 40))
        self.dealer_handlabel.move(QPoint(490, 230)) 
        self.dealer_handlabel.setStyleSheet("border: 2px solid gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
        self.dealer_handlabel.show()

        self.point_labels : list[QtWidgets.QLabel] = [] # player point labels
        elevations = [-40, -20, 0, 0, 0, -20, -40]
        
        for x in range(7):
            yposition  = 542 + int(elevations[x])
            xposition   = 65 + x * 128
            self.n_label = QtWidgets.QLabel()
            self.n_label.setStyleSheet("border: 2px dashed gold; border-radius: 1px ; font : bold 10px ; background: lightgreen ; color : black" )
            self.n_label.setParent(self)
            self.n_label.resize(QSize(80, 40))
            self.n_label.move(QPoint(xposition, yposition))
            self.point_labels.append(self.n_label)
            self.n_label.show()
        
        self.callback_dict = {UpdateType.POINTS: self.update_points_label,
                              UpdateType.NEXTHAND: self.nexthand,
                              UpdateType.DEALERTURN: self.dealerturn,
                              }

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
        self.cards, self.animgroup = self.table.StartNhand(4)
        for card in self.cards:
            card : EasyCardLabels
            card.setParent(self)
            card.show()
        self.animgroup.start()
    
    def dealerturn(self):
        cards, animations = self.table.DealerTurn()
        for card in cards:
            card.setParent(self)
            card.show()
        animations.start()

    def update_points_label(self, value, hand_nr : int):
        lbl = self.point_labels[hand_nr]
        lbl.setText(f"Points: {value}")

    def nexthand(self, hand_nr : int, text):
        lbl = self.point_labels[hand_nr]
        lbl.setText(text)
        self.stand()

    def hit(self):
        card = self.table.hit()
        card.setParent(self)
        card.show()
        card.animation.start()
    
    def stand(self):
        self.table.stand()
    
    def get_table_updates(self, type : UpdateType, *args):
        self.callback_dict[type](*args)
    
