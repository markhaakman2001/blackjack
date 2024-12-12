from src.blackjack.gui_shoehand import Hand, Bank
from src.blackjack.gui_playerdealer import Player, Dealer
from src.extrafiles.labels import EasyCardLabels, Shoe, DeckOfCards
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import sys
import time



class Table:

    def __init__(self, hands=1):

        super().__init__()
        self.shoe = Shoe(8)
        self.player = Player(hands)
        self.dealer = Dealer()
        self.bank = Bank(hands)
        self.hands = self.player.hands
        self.results = []
        self.bets = []
        self.bank.deposit()
        
    
    def deal_first_cards(self):

        for x in range(2):
            cards, card_symbols = self.shoe.getcard(n_cards=int(len(self.hands)+1))
            self.dealer.hand.addcard(cards.pop(-1), card_symbols.pop(-1))
            self.player.get_cards(cards, card_symbols)


    def print_first_results(self):
        first_results = []
        first_symbols = []

        for i, hand in enumerate(self.hands):
            hand:Hand
            first_results.append(f"Hand {i + 1}, cards are {hand.cards}, total is {hand.handtotal(hand.softhand())}")
            first_symbols.append(hand.card_symbols)
        
        dealerupcard = f"Dealer upcard is {self.dealer.dealerupcard()}"
        dealer_symbols = self.dealer.hand.card_symbols

        return first_results, dealerupcard, first_symbols, dealer_symbols

    def checkforbust(self, hand):

        if hand.handtotal(hand.softhand()) >= 21:
            
            if hand.handtotal(hand.softhand()) ==  21:             
                
                hand.deactivate()
                return "You have 21."
                
            else:
                
                hand.deactivate()
                return "You busted"
    

    def check_for_win(self, dealertotal, hand):

        if self.dealer.hand.blackjack():
            if hand.blackjack():
                return "Push"
            else:
                return "Lose"

        elif hand.handtotal(hand.softhand()) > 21:
            return "Lose"
        
        elif hand.handtotal(hand.softhand()) <= 21:
            
            if dealertotal > 21:
                return "Win"

            elif hand.blackjack():
                return "BlackJack, win"
            
            elif dealertotal == hand.handtotal(hand.softhand()):
                return "Push"
            
            elif dealertotal < hand.handtotal(hand.softhand()):
                return "Win"
            
            elif dealertotal > hand.handtotal(hand.softhand()):
                return "Lose"

    

    def winlose(self, hand):
        
        dealer_total = self.dealer.hand.handtotal(self.dealer.hand.softhand())
        result = self.check_for_win(dealer_total, hand)
        return result

    def hitcard(self, hand : Hand):
        card, cardsymbol = self.shoe.getcard()
        hand.addcard(card, cardsymbol)
        text = f"Cards are {hand.cards}, total: {hand.handtotal(hand.softhand())}"
        return card, text, cardsymbol


    def NextOrNot(self, hand):

        if hand.active:
            return False
        else:
            return True


    def split(self, hand : Hand):
        """split hand

        Args:
            hand (which hand): _description_

        Returns:
            (list, list): Split hand texts, and a list with the new hands [texts, hands]
        """        
        texts, hands = hand.splithand(self.shoe)
        
        return texts, hands
    

    def place_bets(self):

        for i, hand in enumerate(self.hands):
            bet = float(input(f"Hand {i+1}, place your bet \n"))
            hand.bet += float(bet)
            self.bank.betamount(hand, amount=bet)

    def addresults(self, hand):
        self.results.append(hand)    
    
    def PlayRound(self):

        for hand in self.hands:
            self.bank.betamount(hand, 100)

        self.results = []
        
        self.deal_first_cards()
        
        
        #print(self.shoe.cards)

        for i, hand in enumerate(self.hands):

            self.playhand(hand, i)
        
        print(f"Dealer has {self.dealer.hand.cards}, total is {self.dealer.hand.handtotal(self.dealer.hand.softhand())}")
        dealerplay = self.dealer.hand.dealerturn()

        while dealerplay:

            dealer_card = self.shoe.getcard()
            self.dealer.dealerplay(dealer_card)
            dealerplay = self.dealer.hand.dealerturn()
        
        final_results = []
        
        print(self.results)

        for i, hand in enumerate(self.results):
            
            results = self.winlose(hand)
            winnings = self.bank.amount_won(result=results, hand=hand)
            print(f"Hand {i+1}, {results=}, you win ${winnings}")
            final_results.append(self.winlose(hand))
        
        self.bets = [hand.bet for hand in self.results]
        print(f"Your funds are now ${self.bank.funds}")

        self.player.reset()
        self.dealer.reset()

    def dealer_play(self):
        card, cardsymbol = self.shoe.getcard(n_cards=1)
        txt = self.dealer.dealerplay(card, cardsymbol)
        return txt


def main():
    app = QtWidgets.QApplication(sys.argv)
    table = Table()
    table.ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
