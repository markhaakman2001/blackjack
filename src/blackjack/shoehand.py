import numpy as np
import random
from math import *

class Shoe:

    def __init__(self, d = 8):
        """create a shoe with multiple decks

        Args:
            d (int, optional): amount of decks. Defaults to 8.
        """        
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        deck =  values * 4
        self.decks = d
        self.cards = deck * d
        random.shuffle(self.cards)

    
    def getcard(self, n=1):
        """take the next card or cards from the shoe.

        Args:
            n (int, optional): amount of cards to be taken. Defaults to 1.

        Returns:
            int, list: the next card or cards from the shoe
        """          
        if n == 1:
            card = self.cards.pop(0)
            return card
        else:
            cards = []
            for x in range(n):
                card = self.cards.pop(0)
                cards.append(card)
            return cards
    

    def neednewshoe(self):
        return (len(self.cards) / (self.decks * 52)) < 0.5
    

    def getnewshoe(self):
        self.__init__(self.decks)


    def new_shoe(self, decks):
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        deck =  values * 4
        self.shoe = deck * decks

        
        self.shoe = random.shuffle(self.shoe)


class Hand:
    
    def __init__(self, bet=0):
        self.cards = []
        self.total = 0
        self.hands = []
        self.results = []
        self.bet = bet
        self.split = False
        self.active = True
    
    def deactivate(self):
        self.active = False

    def addcard(self, card):
        """Add a card to the hand

        Args:
            card (int): The card thats added
        """        
        self.cards.append(card)
    

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
        
    
    def splithand(self, shoe, bank):
        self.split = True
        self.hands = [Hand(), Hand()]

        for i, hand in enumerate(self.hands):
            bank.betamount(hand, self.bet)
            
            hand.addcard(self.cards[0])
            hand.addcard(shoe.getcard())
            
    
    
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

    def PlayHand(self, card, no_double=True):
        """Give the player a card and show the new total.

        Args:
            card (int): Value of the card that was given

        Returns:
            Bool: True if player hits, False if player busts or stands.
        """        
        self.addcard(card)
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


    def reset(self):
        self.cards = []
        self.total = 0
        self.__init__()


class Bank:

    def __init__(self, hands):
        """Initialise a bank account

        Args:
            hands (int): How many hands the player is playing with
        """             
        self.funds = 0
        self.bets = []
        for x in range(hands):
            self.bets.append(0)
        self.bank = 10**6
    
    def deposit(self, amount = 10**4):
        """Add money to the funds

        Args:
            amount (float, optional): Amount of money to be added to funds. Defaults to 10**4.
        """        
        self.funds += amount
    
    def betamount(self, hand, amount = 100):
        """Place a bet for a certain amount

        Args:
            amount (int, optional): How much money to bet. Defaults to 100.
        """        
        hand.bet += amount
        self.funds -= amount
        print(f"Your bet is {hand.bet}")

    def amount_won(self, result, hand):
        total_bet = hand.bet
        calculator = { 
            "BlackJack, win": lambda x: x * 2.5,
            "Lose": lambda x: x * 0,
            "Push": lambda x: x * 1,
            "Win": lambda x: x * 2
        }
        win = calculator.get(result)(total_bet)
        self.funds += win
        return win
    
    def doubled(self, i):
        self.bets[i] += self.bets[i]
        self.funds -= (self.bets[i] / 2)
        print(f"You doubled, your bet is now ${self.hand}")

    def split(self, i):
        
        print(f"Split, your bet is now ${self.hand}")

    def winlosepush(self, condition = False):
        hand = self.hand
        win = 0
        if condition == True:
            self.funds += (hand * 2)
            self.bank -= hand
            win = hand * 2
            
        elif condition == False:
            self.bank += hand
            
        elif condition == 3:
            self.funds += hand
            win = self.hand
        
        self.hand = 0
        return win
