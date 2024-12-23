from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
import numpy as np
import random
from src.baccarat.baccarat_animations import BaccaratCard
from src.extrafiles.backgroundwidget import BaccaratBackground
from src.baccarat.baccarat_table_handler import BaccaratTable, PlayerType
from src.baccarat.baccarat_cards import Kind, CardSymbol, Shoe, Card
from src.baccarat.baccarat_rules_handler import ActionState, ActionTypes, OutComeTypes, PlayerType, SideBets
from src.extrafiles.BaccaratButtons import BaccaratFiche, BaccaratFicheOptionMenu
from src.baccarat.BaccaratBank import Bank
import sys



class InsufficientFundsException(Exception):

    def __init__(self, message="Insufficient funds to complete transaction", max_funds=100):
        self.message = message
        self.max_funds = max_funds
        super().__init__(self.message)
    
    def __str__(self):
        return f"Insufficient funds, maximum possible bet is {self.max_funds}"


class NewBank(Bank):

    def __init__(self, initial_deposit=500):
        self._funds     = initial_deposit * 100
        super().__init__(self._funds)
    

    def PlaceBet(self, who):
        try:
            if self.funds < self.BetSize:
                raise InsufficientFundsException(max_funds = self.Balance)
            else:               
                return super().PlaceBet(who)
        except InsufficientFundsException as e:
            print(e)

if __name__ == "__main__":
    bank = NewBank()
    bank.Deposit(100)
    bank.BetSize = 99
    bank.PlaceBet(OutComeTypes.BANKER)
    print("one bet new the next:")
    bank.PlaceBet(OutComeTypes.BANKER)