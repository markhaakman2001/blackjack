import numpy as np
import random
from math import *
import matplotlib.pyplot as plt
from playerdealer import Player, Dealer


class Shoe:

    def __init__(self, d = 1):
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        deck =  values * 4
        self.decks = d
        self.cards = deck * self.decks
        random.shuffle(self.cards)

    
    def getcard(self):
        card = self.cards.pop(0)
        return card
    

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
    
    def __init__(self):
        self.cards = []
        self.total = 0
    
    def addcard(self, card):
        self.cards.append(card)
    

    def handtotal(self, ace = False):
        self.total = 0

        for card in self.cards:
            self.total += card
        
        if ace == True:
            if self.total > 21:
                self.total -= 10
        
        return self.total
    

    def softhand(self):
        for card in self.cards:
            if card == 11:
                return True
        return False
    
    def dealerturn(self):
        total = self.handtotal(self.softhand())
        if total < 17:
            return True
        elif total >= 17:
            return False

    def blackjack(self):
        return (len(self.cards) == 2) and (self.handtotal() == 21)
    

    def reset(self):
        self.cards = []
        self.total = 0
        self.__init__()



class Table:

    def __init__(self):
        self.shoe = Shoe(8)
        self.player = Player()
        self.dealer = Dealer()
        self.bank = Bank()
        self.bank.deposit(10**4)
    
    def dealfirstcards(self):

        for hand in self.player.hands:
            hand.addcard(self.shoe.getcard())
        self.dealer.hand.addcard(self.shoe.getcard())
        for hand in self.player.hands:
            hand.addcard(self.shoe.getcard())
        self.dealer.hand.addcard(self.shoe.getcard())
    
    def doubledown(self):
        self.bank.doubled()
        self.player.hand.addcard(self.shoe.getcard())
        # print(f"You doubled, bet is now ${self.bank.hand} \n Your card was {self.player.hand.cards[-1]}, total is {self.player.hand.handtotal(self.player.hand.softhand())}")
      

    def split(self):
        self.bank.split()
        totals = []
        actions = []
        print("You split")
        
        for i, hand in enumerate(self.player.handsplit):
            hand.addcard(self.player.hand.cards[i])
            hand.addcard(self.shoe.getcard())
            totals.append(hand.handtotal())
            print(f"Hand {i} is {self.player.handsplit[i].cards}, total is {totals[i]}")
            action = input("Hit or Stand? (h/s) \n")
            actions.append(action)
        return actions
        
        

    def print_firstresults(self):
        for hand in self.player.hands:
            playertotal = hand.handtotal(self.player.hand.softhand())
            playercards = hand.cards
            dealerupcard = self.dealer.dealerupcard()
            actions = ['h', 's', 'd', 'sp']
            print(f"Your cards are {playercards}, total is {playertotal}")
            print(f"Dealer upcard is  {dealerupcard}")
            action = 'x'
            while action not in actions:
                if playercards[0] == playercards[1]:
                    action = input("Hit, Stand , double or split? (h/s/d/sp) \n")            
                else:
                    action = input("Hit, Stand or Double? (h/s/d) \n")
            return action

    def print_finalresults(self):
        winamount = self.bank.winlosepush(self.checkresults())
        if self.dealer.hand.blackjack():
            if self.player.hand.blackjack() == True:
                print(f"Your cards are {self.player.hand.cards}, dealer cards are {self.dealer.hand.cards}")
                self.dealer.hand.reset()
                self.player.hand.reset()
                return print(f"push, you win ${winamount}, your funds are now ${self.bank.funds}")
            else:
                self.dealer.hand.reset()
                self.player.hand.reset()
                return print(f"Stop playing bro you got humbled, your funds are now ${self.bank.funds}")
        playertotal = self.player.hand.handtotal(self.player.hand.softhand())
        
        dealertotal = self.dealer.hand.handtotal(self.dealer.hand.softhand())
        print(f""" Dealer total is {dealertotal}, {self.dealer.hand.cards}
Player total is {playertotal}, {self.player.hand.cards}
""")    
        
        if self.checkresults() == 3:
            self.dealer.hand.reset()
            self.player.hand.reset()
            return print(f"Push, you win ${winamount}, your funds are now ${self.bank.funds}")
        elif self.checkresults() == True:
            self.dealer.hand.reset()
            self.player.hand.reset()
            return print(f"You win ${winamount} congratulations, your funds are now ${self.bank.funds}")
        elif self.checkresults() == False:
            self.dealer.hand.reset()
            self.player.hand.reset()
            return print(f"You lose!!!!!!!!!!!!!!!!!!!!!! idiot, your funds are now ${self.bank.funds}")

    def printresults(self):
        total = self.player.hand.handtotal(self.player.hand.softhand())
        print(f"your card was {self.player.hand.cards[-1]}, total is {total}")
        if total > 21:
            print("You bust")
            action = "s"
        elif total == 21:
            print("You have 21")
            action = "s"
        elif total < 21:
            action = input("Hit or stand? (h/s) \n")
        return action
    
    def checkresults(self):
        dealertotal = self.dealer.hand.handtotal(self.dealer.hand.softhand())
        playertotal = self.player.hand.handtotal(self.player.hand.softhand())
        if playertotal > 21:            
            return False
        elif playertotal <= 21:
            if dealertotal > playertotal:
                if dealertotal <= 21:
                    return False
                elif dealertotal > 21:
                    return True
            elif dealertotal < playertotal:
                return True
            elif dealertotal == playertotal:
                return 3


    def playround(self):
        self.bank.betamount(100)

        if self.shoe.neednewshoe():
            self.shoe.getnewshoe()
        
        self.dealfirstcards()
        cards = self.player.hands.cards

        if self.player.hand.blackjack() == True:
            return self.print_finalresults()

        if not self.dealer.hand.blackjack():
            action = self.print_firstresults()

            if action == "sp":
                if cards[0] != cards[1] or len(cards) > 2:
                    print("you cant split")
                    action = self.print_firstresults()                                       
                else:
                    self.split()

            # keep going untill player stands
            while action == "h":
                cards = self.player.hand.cards
                handtotal = self.player.hand.handtotal(self.player.hand.softhand())

                if handtotal == 21:
                    if self.player.hand.blackjack():
                        print("You have a blackjack congratulations")
                        self.print_finalresults()
                        action = "s"
                        
                    else:
                        print("Your total is 21")
                        if self.dealer.hand.dealerturn():
                            self.dealer.hand.addcard(self.shoe.getcard())
                            print(f"""dealer pulls {self.dealer.hand.cards[-1]}, total is {self.dealer.hand.handtotal(self.dealer.hand.softhand())}, {self.dealer.hand.cards}""")
                        elif not self.dealer.hand.dealerturn():
                            self.print_finalresults()
                            return self.checkresults()
                
                # player bust
                elif handtotal > 21:
                    print(f"Your card was {cards[-1]}, total is {handtotal}")
                    print("You busted, fucking idiot")
                    self.print_finalresults()
                    action == "s"
                    return self.checkresults()                   

                
                elif action == "s":

                    while self.dealer.hand.dealerturn():
                        self.dealer.hand.addcard(self.shoe.getcard())
                        print(f"""dealer pulls {self.dealer.hand.cards[-1]}, total is {self.dealer.hand.handtotal(self.dealer.hand.softhand())}, {self.dealer.hand.cards}""")
                    
                    self.print_finalresults()
                    return self.checkresults()

                # give the player a card
                else:
                    self.player.hand.addcard(self.shoe.getcard())
                    
                    if self.player.hand.handtotal(self.player.hand.softhand()) >= 21: #dont let player hit on  or above 21
                        if self.player.hand.handtotal(self.player.hand.softhand()) > 21:
                            print(f"Your total is {self.player.hand.handtotal(self.player)}, you bust {self.player.hand.cards}")
                            self.print_finalresults()
                            return self.checkresults()
                        elif self.player.hand.handtotal(self.player.hand.softhand()) == 21:
                            print(f"your total is {self.player.hand.handtotal(self.player.hand.softhand())}, {self.player.hand.cards}")
                            self.print_finalresults()
                            return self.checkresults()
                    action = self.printresults()
        
            if action == "s":
                    print("You chose 'stand'")
                    print(f"Dealer has {self.dealer.hand.handtotal()}, {self.dealer.hand.cards}")

                    # dealer gets card untill 17
                    while self.dealer.hand.dealerturn():
                        self.dealer.hand.addcard(self.shoe.getcard())
                        print(f"""dealer pulls {self.dealer.hand.cards[-1]}, total is {self.dealer.hand.handtotal()}, {self.dealer.hand.cards}""")
                    
                    self.print_finalresults()
                    return self.checkresults()

            # player double down  
            if action == "d":
                self.doubledown()

                # check for bust
                if self.player.hand.handtotal(self.player.hand.softhand()) > 21:
                    print("you busted")
                print(f"Dealer has {self.dealer.hand.handtotal()}, {self.dealer.hand.cards}")
                
                # dealer turn untill 17
                while self.dealer.hand.dealerturn():
                    self.dealer.hand.addcard(self.shoe.getcard())
                    print(f"""dealer pulls {self.dealer.hand.cards[-1]}, total is {self.dealer.hand.handtotal()}, {self.dealer.hand.cards}""")
                
                self.print_finalresults()                
                return self.checkresults()

        # dealer blackjack          
        elif self.dealer.hand.blackjack() == True:
            print("Dealer has blackjack")
            self.print_finalresults()
            return self.checkresults()
        
        
        self.player.hand.reset()
        self.dealer.hand.reset()
        return self.checkresults()

class Bank:

    def __init__(self):
        self.funds = 0
        self.hand = 0
        self.bank = 10**6
    
    def deposit(self, amount = 10**4):
        self.funds += amount
    
    def betamount(self, amount = 100):
        self.hand = 0
        self.hand += amount
        self.funds -= amount
        print(f"Your bet is ${self.hand}")
    
    def doubled(self):
        self.hand += self.hand
        self.funds -= (self.hand / 2)
        print(f"You doubled, your bet is now ${self.hand}")

    def split(self):
        hand = self.hand
        self.hand = [hand, hand]
        self.funds -= self.hand[0]
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


table = Table()
start_play = "y"
while start_play == "y":
    table.playround()
    # hstart_play = input("Play again? Yes (y) or no (n) \n" )





    




        
        
        
    

