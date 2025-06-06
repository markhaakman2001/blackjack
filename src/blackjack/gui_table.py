from src.blackjack.gui_shoehand import Hand, WinType
from src.blackjack.gui_playerdealer import Player, Dealer
from src.CustomUIfiles import Shoe
from PySide6 import QtWidgets
import sys


class Table:

    def __init__(self, hands=1):

        super().__init__()
        self.shoe   = Shoe(8)
        self.player = Player(hands)
        self.dealer = Dealer()
        #self.bank = Bank(500)
        self.hands = self.player.hands
        self.results = []
        self.bets = []
        
        
    
    def deal_first_cards(self):

        for x in range(2):
            cards, card_symbols = self.shoe.getcard(n_cards=int(len(self.hands)+1))
            self.dealer.hand.addcard(cards.pop(-1), card_symbols.pop(-1))
            self.player.get_cards(cards, card_symbols)

    def get_current_funds(self):
        return self.bank._funds

    def print_first_results(self) -> tuple[list, list, list, list]:
        first_results = []
        first_symbols = []

        for i, hand in enumerate(self.hands):
            hand:Hand
            first_results.append(f"Hand {i + 1}, cards are {hand.cards}, total is {hand.handtotal(hand.softhand())}")
            first_symbols.append(hand.card_symbols)
        
        dealerupcard = f"Dealer upcard is {self.dealer.dealerupcard()}"
        dealer_symbols = self.dealer.hand.card_symbols

        return first_results, dealerupcard, first_symbols, dealer_symbols

    def checkforbust(self, hand) -> str:

        if hand.handtotal(hand.softhand()) >= 21:
            
            if hand.handtotal(hand.softhand()) ==  21:             
                
                hand.deactivate()
                return "You have 21."
                
            else:
                
                hand.deactivate()
                return "You busted"
    

    def check_for_win(self, dealertotal, hand) -> WinType:

        if self.dealer.hand.blackjack():
            if hand.blackjack():
                return WinType.PUSH
            else:
                return WinType.LOSE

        elif hand.handtotal(hand.softhand()) > 21:
            return WinType.LOSE
        
        elif hand.handtotal(hand.softhand()) <= 21:
            
            if dealertotal > 21:
                return WinType.WIN

            elif hand.blackjack():
                return WinType.BLACKJACK
            
            elif dealertotal == hand.handtotal(hand.softhand()):
                return WinType.PUSH
            
            elif dealertotal < hand.handtotal(hand.softhand()):
                return WinType.WIN
            
            elif dealertotal > hand.handtotal(hand.softhand()):
                return WinType.LOSE

    

    def winlose(self, hand) -> WinType:
        
        dealer_total = self.dealer.hand.handtotal(self.dealer.hand.softhand())
        result = self.check_for_win(dealer_total, hand)
        return result

    def hitcard(self, hand : Hand) -> tuple[int, str, str]:
        card, cardsymbol = self.shoe.getcard()
        hand.addcard(card, cardsymbol)
        text = f"Cards are {hand.cards}, total: {hand.handtotal(hand.softhand())}"
        return card, text, cardsymbol


    def NextOrNot(self, hand) -> bool:

        if hand.active:
            return False
        else:
            return True


    def split(self, hand : Hand) -> tuple[list, list]:
        """split hand

        Args:
            hand (which hand): _description_

        Returns:
            (list, list): Split hand texts, and a list with the new hands [texts, hands]
        """        
        texts, hands = hand.splithand(self.shoe)
        
        return texts, hands
    

    def place_bets(self) -> None:

        for i, hand in enumerate(self.hands):
            bet = float(input(f"Hand {i+1}, place your bet \n"))
            hand.bet += float(bet)
            self.bank.betamount(hand, amount=bet)

    def addresults(self, hand) -> None:
        self.results.append(hand)    
    
    def PlayRound(self):

        # for hand in self.hands:
        #     self.bank.betamount(hand, 100)

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

    def dealer_play(self) -> tuple[str, int, str]: 
        card, cardsymbol = self.shoe.getcard(n_cards=1)
        txt = self.dealer.dealerplay(card, cardsymbol)
        return txt, card, cardsymbol

    def reset(self):
        self.dealer.__init__()
        self.player.__init__()
        self.hands   = self.player.hands
        self.results = []
        self.bets    = []
        
        print(f"Reset, player hands: {self.player.hands}, dealer: {self.dealer.hand.cards}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    table = Table()
    table.ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
