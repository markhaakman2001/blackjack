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
import sys



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


class ErrorChecker(object):
    
    
    def _CheckFundsDecorator(func):
        
        from src.baccarat.BaccaratBank import Bank

        def CheckFunds(*args, who):
            
            self : Bank = args[0]
            if self.funds <= 0:
                raise ZeroFundsError
            elif self.funds < self.BetSize:
                raise InsufficientFundsError(self.Balance)
            else:
                func(*args, who)

        return CheckFunds

def main():
    pass

if __name__ == "__main__":
    main()