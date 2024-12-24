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
from src.baccarat.BankingErrors import InsufficientFundsError, ZeroFundsError
import sys


class ErrorChecker(object):

    
    def _CheckFundsDecorator(func):

        
        def CheckFunds(*args, who):
            
            self : Bank = args[0]
            if self.funds <= 0:
                raise ZeroFundsError
            elif self.funds < self.BetSize:
                raise InsufficientFundsError(self.Balance)
            else:
                func(*args, who)

        return CheckFunds



class Bank(QObject):

    BalanceChanged = Signal(name="BalanceChanged")

    def __init__(self, initial_deposit_euros = 0):
        """_summary_

        Args:
            initial_deposit_euros (int, optional): _description_. Defaults to 0.
        """       
        super().__init__() 
        self._funds     = initial_deposit_euros * 100
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

        old_funds      = self._funds
        amount_credits = amount * 100
        self._funds = amount_credits + old_funds
        self.BalanceChanged.emit()
    
    @funds.deleter
    def funds(self, amount):
        old_funds      = self._funds
        amount_credits = amount * 100
        self._funds =  old_funds - amount_credits
    
    @property
    def Balance(self):
        """Get the balance in euros

        Returns:
            float : The current balance in euros
        """        
        self._Balance = self.funds / 100
        return self._Balance
    
    
    @property
    def TotalBet(self):
        self._TotalBet = (self._BankerBet + self._PlayerBet + self._TieBet) * 100
        return self._TotalBet
    
    @TotalBet.deleter
    def TotalBet(self):
        self._BankerBet = 0
        self._PlayerBet = 0
        self._TieBet    = 0
    
    @property
    def BetSize(self) -> int:
        return self._BetSize
    
    @BetSize.setter
    def BetSize(self, amount) -> None:
        """Set the BetSize

        Args:
            amount (float): The currently selected BetSize in euros
        """        
        self._BetSize = int(amount * 100)
    
    @BetSize.deleter
    def BetSize(self) -> None:
        self._BetSize = 100

    def Deposit(self, amount):
        """Deposit amount in euros

        Args:
            amount (float): amount to deposit in euros
        """
        self.funds = amount

    @ErrorChecker._CheckFundsDecorator
    def PlaceBet(self, who : OutComeTypes) -> None:
        """Place a bet in euros on one of the outcomes

        Args:
            who (OutComeTypes): The outcome that the bet is placed on
            amount (float): amount in euros
        """        
        amount = self.BetSize / 100
        if who == OutComeTypes.BANKER:
            self._BankerBet += amount
        elif who == OutComeTypes.PLAYER:
            self._PlayerBet += amount
        elif who == OutComeTypes.TIE:
            self._TieBet += amount

        self._funds -= self.BetSize
        self.BalanceChanged.emit()
        print(f"You bet {amount} on {who.name}")
        print(f"Your current balance is {self.Balance}")
    

    # dit fix ik morgen wel
    def CheckTotalWin(self, result : OutComeTypes) -> int:
        """Calculate the amount won in credits. based on the result

        Args:
            result (OutComeTypes): PLAYER and BANKER pay 2:1, TIE pays 8:1

        Returns:
            int: The amount won in credits
        """        
        
        if result == OutComeTypes.BANKER:
            TotalWinEuros = (self._BankerBet) * 2
        elif result == OutComeTypes.PLAYER:
            TotalWinEuros = (self._PlayerBet) * 2
        elif result == OutComeTypes.TIE:
            TotalWinEuros = (self._TieBet ) * 8
        
        TotalWinCredits = TotalWinEuros * 100

        del self.TotalBet
        
        self.funds = TotalWinEuros

        return TotalWinCredits
        

class NewBank(Bank):
    

    def __init__(self, initial_deposit=0):
        self._funds     = initial_deposit
        super().__init__(self._funds)
    
    
    def PlaceBet(self, who):
        who=who
        try:
            return super().PlaceBet(who=who)
        except InsufficientFundsError as e:
            print(e)
            raise InsufficientFundsError(self.Balance)
        except ZeroFundsError as e:
            print(e)
            raise ZeroFundsError
        



def main():
    bank = NewBank()
    bank.Deposit(100)
    bank.BetSize = 101
    bank.PlaceBet(who=OutComeTypes.BANKER)

if __name__ == "__main__":
    main()