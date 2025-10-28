import enum
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
from blackjack.blackjackfunctions import UpdateType, WinFunctions, WinType
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

        # button used for split
        self.split_button = QtWidgets.QPushButton(text="split", parent=self)
        self.split_button.move(QPoint(0, 200))
        self.split_button.show()
        self.split_button.clicked.connect(self.split)


        #Add labels that show the total point value for each hand
        #---------
        self.dealer_handlabel = QtWidgets.QLabel(parent=self) # This is the dealers label
        self.dealer_handlabel.resize(QSize(80, 40))
        self.dealer_handlabel.move(QPoint(490, 230)) 
        self.dealer_handlabel.setStyleSheet("border: 2px solid gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
        self.dealer_handlabel.show()

        self.point_labels : list[QtWidgets.QLabel] = [] # player point labels
        self.elevations = [-40, -20, 0, 0, 0, -20, -40]

        # add menu to choose betsize
        #---------
        self.BetSizeDialog       = BaccaratFicheOptionMenu(self)
        self.OpenBetSizeMenu     = QtWidgets.QPushButton(text="BetSize")
        self.CurrentBetSizeImage = BaccaratFiche()
        self.CurrentBetSizeImage.setEnabled(False)
        self.CurrentBetSizeImage.SetOneValueFiche()

        self.CurrentBetSizeImage.setParent(self)
        self.OpenBetSizeMenu.setParent(self)

        self.OpenBetSizeMenu.resize(QSize(500, 35))
        self.CurrentBetSizeImage.resize(QSize(50, 50))

        self.OpenBetSizeMenu.move(QPoint(250, 670))
        self.CurrentBetSizeImage.move(QPoint(200, 635))

        self.OpenBetSizeMenu.clicked.connect(self.ShowBetSizeMenu)
        self.BetSizeDialog.BetSizeSignal.connect(self.ChangeCurrentBetSize)



        
        for x in range(7):
            yposition  = 542 + int(self.elevations[x])
            xposition   = 65 + x * 128
            self.n_label = self.create_label(xposition, yposition)
            self.point_labels.append(self.n_label)
            self.n_label.show()
        
        self.callback_dict = {UpdateType.POINTS: self.update_points_label,
                              UpdateType.NEXTHAND: self.nexthand,
                              UpdateType.DEALERTURN: self.dealerturn,
                              UpdateType.RESULT: self.final_result,
                              UpdateType.HANDS: self.create_hands_and_labels
                              }
    
    def ShowBetSizeMenu(self):
        self.BetSizeDialog.exec()

    @Slot(int)
    def ChangeCurrentBetSize(self, value):
        betsizedict = {1   : self.CurrentBetSizeImage.SetOneValueFiche,
                       5   : self.CurrentBetSizeImage.SetFiveValueFiche,
                       25  : self.CurrentBetSizeImage.SetTwentyFiveValueFiche,
                       100 : self.CurrentBetSizeImage.SetOneHundredValueFiche
        }
        betsizedict[value]()
        self.CurrentBetSizeImage.update()

    def create_label(self, xposition, yposition):
        n_label = QtWidgets.QLabel()
        n_label.setStyleSheet("border: 2px dashed gold; border-radius: 1px ; font : bold 10px ; background: lightgreen ; color : black" )
        n_label.setParent(self)
        n_label.resize(QSize(80, 40))
        n_label.move(QPoint(xposition, yposition))
        return n_label
    
    @Slot()
    def start_round_test(self):
        n_hands = 2
        cards, self.animgroup, self.cards_per_hand = self.table.StartNhand(n_hands)
        for card in cards:
            card : EasyCardLabels
            card.setParent(self)
            card.show()
        self.animgroup.start()
        self.dealer_handlabel.setText(f"Upcard: {self.table.dealer.hand.cards[0]._get_value()}")
    
    def dealerturn(self):
        cards, self.dealer_animations = self.table.DealerTurn()
        for card in cards:
            card.setParent(self)
            card.show()
        
        self.dealer_animations.finished.connect(self.table.final_results)
        self.dealer_animations.start()
        self.dealer_handlabel.setText(f"Dealer total: {self.table.dealer.hand._get_handtotal()}")

    def create_hands_and_labels(self, hands : list[BlackJackHand]):
        self.point_label_dict = {hand : self.point_labels[i] for i, hand in enumerate(hands)}
        print(self.point_label_dict)


    def update_points_label(self, value, hand : BlackJackHand):
        lbl = self.point_label_dict[hand]
        lbl.setText(f"Points: {value}")

    def nexthand(self, hand : BlackJackHand, text):
        lbl = self.point_label_dict[hand]
        lbl.setText(text)
        self.stand()

    def hit(self):
        card = self.table.hit()
        card.setParent(self)
        card.show()
        card.animation.start()
    
    def stand(self):
        self.table.stand()
    
    def split(self):
        current_hand = self.table.player.active_hand.hand_number

        lbl = self.point_label_dict[self.table.player.active_hand]
        lbl.deleteLater()

        original_cards = self.cards_per_hand.get(current_hand)
        cards, self.split_anim, new_cards, hands = self.table.split(original_cards)

        for card, hand in zip(new_cards, hands):
            xpos = 65 + 128 * hand.hand_number + hand.x_label_shift
            ypos = 542 + int(self.elevations[hand.hand_number])
            card.setParent(self)
            card.show()
            self.n_label = self.create_label(xpos, ypos)
            self.n_label.show()
            self.point_label_dict[hand] = self.n_label
            self.update_points_label(hand._get_handtotal(), hand)
        self.split_anim.start()
    
    def final_result(self, result : WinType, hand: BlackJackHand, value):
        texts = {WinType.BLACKJACK : "BlackJack, win!",
                 WinType.LOSE      : "Lose",
                 WinType.WIN       : "Win!",
                 WinType.PUSH      : "Push"}
        lbl = self.point_label_dict[hand]
        lbl.setText(f"{value}, {texts[result]}")


    def get_table_updates(self, type : UpdateType, *args):
        self.callback_dict[type](*args)
    
