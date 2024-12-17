from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from math import *
import numpy as np
import random
from src.extrafiles.labels import BaccaratCard
from src.extrafiles.backgroundwidget import BaccaratBackground
from src.baccarat.baccarat_table_handler import BaccaratTable, PlayerType
from src.baccarat.baccarat_cards import Kind, CardSymbol, Shoe
import sys






class BaccaratGui(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        self.central_widget = BaccaratBackground()
        self.central_widget.setParent(self)
        self.central_widget.resize(QSize(1200, 600))
        self.resize(1200, 700)

        self.banker_left_right_x = [690, 790]           # Xpositions for bankers cards
        self.player_left_right_x = [328, 428]           # Xpositions for players cards
        self.label_ypos          = 118                  # right in the middle of the box
        self.player_label        = QtWidgets.QLabel(self)   # Used to update and display the players points
        self.banker_label        = QtWidgets.QLabel(self)   # Used to update and display the bankers points

        self.start_btn           = QtWidgets.QPushButton(text="PLAY")

        self.player_label.setParent(self)
        self.banker_label.setParent(self)
        self.start_btn.setParent(self)

        self.player_label.resize(QSize(100, 50))
        self.banker_label.resize(QSize(100, 50))
        self.start_btn.resize(QSize(100, 50))

        self.player_label.move(QPoint(328, 225))
        self.banker_label.move(QPoint(690, 225))
        self.start_btn.move(QPoint(550, 650))

        self.player_label.setStyleSheet("border: 2px solid gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
        self.banker_label.setStyleSheet("border: 2px solid gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")

        self.start_btn.show()
        self.player_label.show()
        self.banker_label.show()


        self.table = BaccaratTable()

        self.start_btn.clicked.connect(self.StartRound)
        self.table.PointsChanged.connect(self.UpdatePoints)
    


    def UpdatePlayerLabel(self):
        """Called when the players points have changed
        """        
        self.player_label.clear()
        points = self.table.player.CalculatePoints()
        self.player_label.setText(f"PLAYER, POINTS: {points}")
        self.player_label.update()
    
    def UpdateBankerLabel(self):
        """Called when the Bankers points have changed
        """        
        self.banker_label.clear()
        points = self.table.banker.CalculatePoints()
        self.banker_label.setText(f"BANKER, POINTS: {points}")
        self.banker_label.update()

    @Slot(PlayerType)
    def UpdatePoints(self, signal):
        if signal == PlayerType.PLAYER:
            self.UpdatePlayerLabel()
        elif signal == PlayerType.BANKER:
            self.UpdateBankerLabel()

    @Slot()
    def StartRound(self):
        """Starts a game of baccarat by giving 2 cards to the player and two to the banker
        """        
        self.StartingAnimationGroup         = QSequentialAnimationGroup()
        self.player_card, self.banker_cards = self.table.PlaceFirstCards()

        for player_xpos, banker_xpos, player_card, banker_card in zip(self.player_left_right_x, self.banker_left_right_x, self.player_card, self.banker_cards):

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
        
        self.StartingAnimationGroup.start()


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = BaccaratGui()
    ui.show()
    app.exec()


if __name__ == "__main__":
    main()

    