from PySide6 import QtWidgets
from PySide6.QtWidgets import QStyleOption, QStyle
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture
from math import *
import numpy as np
import random
from src.baccarat.baccarat_animations import BaccaratCard
from src.extrafiles.backgroundwidget import BaccaratBackground
from src.baccarat.baccarat_table_handler import BaccaratTable, PlayerType
from src.baccarat.baccarat_cards import Kind, CardSymbol, Shoe, Card
from src.baccarat.baccarat_rules_handler import ActionState, ActionTypes, OutComeTypes, PlayerType, SideBets
import sys

class BankingErrors(Exception):
    """For errors in bankaccount 

    Args:
        Exception (_type_): _description_

    Returns:
        _type_: _description_
    """    
    def __init__(self):
        self.message = "ERROR ERROR"
        super().__init__(self.message)




class Bank:

    def __init__(self, initial_deposit_euros = 0):
        """_summary_

        Args:
            initial_deposit_euros (int, optional): _description_. Defaults to 0.
        """        
        self._funds   = initial_deposit_euros * 100
        self._PlayerBet = 0
        self._BankerBet = 0
        self._TieBet    = 0
    

    @property
    def funds(self):
        """The current funds on the account in credits

        Returns:
            _type_: _description_
        """        
        return self._funds
    
    @funds.setter
    def funds(self, amount):
        amount_credits = amount * 100
        self._funds += amount_credits
    
    @funds.deleter
    def funds(self, amount):
        amount_credits = amount * 100
        self._funds -= amount_credits
    
    @property
    def Balance(self):
        """Get the balance in euros

        Returns:
            float : The current balance in euros
        """        
        self._Balance = self.funds / 100
        return self._Balance
    
    def Deposit(self, amount):
        """Deposit amount in euros

        Args:
            amount (float): amount to deposit in euros
        """
        self.funds = amount

    
    @property
    def TotalBet(self):
        self._TotalBet = (self._BankerBet + self._PlayerBet + self._TieBet) * 100
        return self._TotalBet
    
    @TotalBet.deleter
    def TotalBet(self):
        self._BankerBet = 0
        self._PlayerBet = 0
        self._TieBet    = 0

    def PlaceBet(self, who : OutComeTypes, amount):
        
        try:
            if amount * 100 > self.funds:
                raise BankingErrors
            else: 
                pass
        except BankingErrors:
            print("Not possible")
        if who == OutComeTypes.BANKER:
            self._BankerBet += amount
        elif who == OutComeTypes.PLAYER:
            self._PlayerBet += amount
        elif who == OutComeTypes.TIE:
            self._TieBet += amount
    
        self._funds -= amount * 100
        
        






def main():
    bankacc = Bank(150)
    print(bankacc.funds)
    print(bankacc.Balance)
    bankacc.Deposit(50)
    
    bankacc.PlaceBet(who=OutComeTypes.BANKER, amount=200)
    bankacc.PlaceBet(who=OutComeTypes.BANKER, amount=1)

if __name__ == "__main__":
    main()