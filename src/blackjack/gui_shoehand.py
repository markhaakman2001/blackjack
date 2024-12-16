import numpy as np
import random
from math import *
from src.extrafiles.labels import Shoe, DeckOfCards, EasyCardLabels
from enum import Enum
from PySide6.QtCore import Signal, SignalInstance, Slot, QObject

class WinFunctions:

    def __init__(self, function):
        self.function = function
    
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

class WinType(Enum):

    BLACKJACK = WinFunctions(lambda x: x * 2.5)
    LOSE      = WinFunctions(lambda x: x * 0  )
    PUSH      = WinFunctions(lambda x: x * 1  )
    WIN       = WinFunctions(lambda x: x * 2  )



class Hand:
    
    def __init__(self, bet=0):
        self.cards = []
        self.card_symbols = []
        self.total = 0
        self.hands = []
        self.results = []
        self._bet = bet
        self.split = False
        self.active = True
    
    def deactivate(self):
        self.active = False

    def addcard(self, card, cardsymbol):
        """Add a card to the hand

        Args:
            card (int): The card thats added
        """        
        self.cards.append(card)
        self.card_symbols.append(cardsymbol)
    

    def handtotal(self, ace = False):
        """Return the total value of the hand. If the total is over 21 and the player has an ace count it as 1

        Args:
            ace (bool, optional): True if player has ace, false if not. Defaults to False.

        Returns:
            int: total value of all cards in hand
        """        
        self.total = 0

        for card in self.cards:
            self.total += card
        
        if ace == True:
            if self.total > 21:
                self.total -= 10
        
        return self.total
        
    
    def splithand(self, shoe : Shoe):
        self.split  = True
        self.hands  = [Hand(), Hand()]
        current_bet = self._bet
        split_texts = []

        for i, hand in enumerate(self.hands):
            hand.addcard(self.cards[0], self.card_symbols[0])
            hand._place_bet(current_bet)
            card, card_symbol = shoe.getcard()
            hand.addcard(card, card_symbol)
            split_text = f"Splithand {i+1}, cards: {hand.cards} : {hand.handtotal(hand.softhand())}"
            split_texts.append(split_text)
        
        return split_texts, self.hands
            
    
    
    def softhand(self):
        """check for ace

        Returns:
            bool: False if player has no ace, true if player has ace
        """        
        for card in self.cards:
            if card == 11:
                return True
        return False
    
    
    def dealerturn(self):
        """Dealers turn to take cards. stands on 17 or higher. hits on soft 17.

        Returns:
            bool: True if total is lower than 17.
        """        
        total = self.handtotal(self.softhand())
        
        if total < 17:
            return True
        elif total >= 17:
            return False

    def PlayHand(self, card, cardsymbol:str, no_double=True):
        """Give the player a card and show the new total.

        Args:
            card (int): Value of the card that was given

        Returns:
            Bool: True if player hits, False if player busts or stands.
        """        
        self.addcard(card, cardsymbol)
        print(f"Your cards are {self.cards}, Total is {self.handtotal(self.softhand())}")

        
        if self.handtotal(self.softhand()) > 21:
            print(f"You Busted!")
            return False
        
        elif no_double:
            play = input(f"Hit or Stand?")
            if play == "h":
                return True
        else:
            return False

    
    def blackjack(self):
        """Check for blackjack

        Returns:
            Bool: True if player has blackjack, False otherwise.
        """        
        return (len(self.cards) == 2) and (self.handtotal() == 21)

    
    def _bet(self) -> int:
        return self._bet

    
    def _place_bet(self, amount_credits):
        self._bet = amount_credits
    
    
    def _del_bet(self):
        self._bet = 0


    def reset(self):
        self.cards = []
        self.total = 0
        self.__init__()


class Bank(QObject):

    BetsChanged = Signal(int, name="BetChanged")

    def __init__(self, deposit:float):
        super().__init__()
        self.credits = deposit * 100
        self.total_bets = 0
        
    
    def emitsignal(self):
        self.BetsChanged.emit(1)
    

    def deposit_euros(self, amount):
        """Deposit money into bank account

        Args:
            amount (float): amount in euros
        """        
        credit_extra = amount * 100
        self.credits += credit_extra
        self.BetsChanged.emit(1)
    
    def place_bet(self, amount, hand:Hand):
        """place a bet on the current hand

        Args:
            amount (float): bet amount in euros
            hand (Hand): which hand
        """        
        amount_in_credits = amount * 100
        self.credits -= amount_in_credits
        hand._place_bet(amount_in_credits)
        self.total_bets += amount_in_credits
        self.BetsChanged.emit(1)
       
    
    def win_amount(self, RESULT : WinType, hand : Hand) -> int:
        """Calculate the win based on the result and bet

        Args:
            RESULT (WinType): what type of win
            hand (Hand): which hand

        Returns:
            int: amount won in credits
        """        
        bet_in_credits = hand._bet
        win_in_credits = RESULT.value(bet_in_credits)
        self.credits += win_in_credits
        self.BetsChanged.emit(1)
        return win_in_credits
        

    def DoubleDown(self, hand : Hand):
        """Used when double down

        Args:
            hand (Hand): which hand
        """        
        current_bet_credits = hand._bet
        self.credits -= current_bet_credits
        hand._place_bet(current_bet_credits * 2)
        self.total_bets += current_bet_credits
        self.BetsChanged.emit(1)
    
    
    def Split(self, hand : Hand):
        current_bet = hand._bet
        self.total_bets += current_bet
        self.credits -= current_bet
        self.BetsChanged.emit(1)
    
    def clear_bets(self):
        self.total_bets = 0
        self._total_bets_euros = 0
        print(f"Bank Cleared, balance is {self._funds}")


    
    @property
    def _total_bets(self) -> float:
        self._total_bets_euros = self.total_bets / 100
        return self._total_bets_euros
        


    @property
    def _funds(self) -> float:
        self._funds_euros = (self.credits / 100)
        return self._funds_euros

    

