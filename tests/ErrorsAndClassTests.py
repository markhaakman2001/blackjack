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


def DecoratorTest(func):

    def CheckZeroFunds(*args, **kwargs):
        
        arg = args[0]

        if arg <= 0:
            raise ZeroFundsError
        
        else:
            return func(*args, **kwargs)
    
    return CheckZeroFunds



class InsufficientFundsError(Exception):
    """Exception raised when the available funds are not sufficient for the current betsize
    """    

    def __init__(self, max_funds: int, message="Insufficient funds to perform action"):
        self.message   = message
        self.max_funds = str(f"Maximum possible bet is {max_funds}")
        super().__init__(self.message)
    
    def __str__(self):        
        return str(f".\n".join([self.message, self.max_funds]))

class ZeroFundsError(Exception):

    def __init__(self, message="No available funds"):
        self.message = message

    def __str__(self):
        return str("Your account contains no available funds, please make a deposit before placing a bet.")


@DecoratorTest
def CheckSufficientFundsForBet(funds, betsize) -> None:
    if funds < betsize:
        raise InsufficientFundsError(max_funds=funds)
    else:
        pass




class NewBank(Bank):

    def __init__(self, initial_deposit=0):
        self._funds     = initial_deposit
        super().__init__(self._funds)
    

    def PlaceBet(self, who):
        try:
            if self.funds < self.BetSize:
                raise InsufficientFundsError(max_funds = self.Balance)
            else:               
                return super().PlaceBet(who)
        except InsufficientFundsError as e:
            print(e)

if __name__ == "__main__":
    bank = NewBank()
    bank.Deposit(100)
    bank.BetSize = 99
    CheckSufficientFundsForBet(100, 101)
    
    


