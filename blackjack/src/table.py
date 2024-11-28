from shoehand import Shoe, Hand, Bank
from playerdealer import Player, Dealer


class Table:

    def __init__(self, hands=1):
        self.shoe = Shoe(8)
        self.player = Player(hands)
        self.dealer = Dealer()
        self.hands = self.player.hands
        self.results = []
        
    def deal_first_cards(self):

        for x in range(2):
            cards = self.shoe.getcard(n=int(len(self.hands)+1))
            self.dealer.hand.addcard(cards.pop(-1))
            self.player.get_cards(cards)


    def print_first_results(self):
        self.player.print_hands()
        print(f"Dealer upcard is {self.dealer.dealerupcard()}")
    

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



    def playhand(self, hand, i):
            
            print(f"Hand {i+1}, cards are {hand.cards}, total is {hand.handtotal(hand.softhand())}, dealer upcard is {self.dealer.dealerupcard()}")
            if hand.blackjack():

                print("Blackjack")
                self.results.append(hand)
                return
                
            
                
            elif len(hand.cards) == 2:

                if hand.cards[0] == hand.cards[1]:
                    choice = input("Hit, Stand, Split or Double?\n")
                    
                else:
                    choice = input("Hit, Stand or Double? \n")
                
            else:
                choice = input("Hit or Stand?")

            if choice == "h":

                play = True

                while play == True:

                    play = hand.PlayHand(self.shoe.getcard())

                

            elif choice == "split":
                    
                self.split(hand)
                
            elif choice == "d":
                play = True

                while play:
                    
                    play = hand.PlayHand(self.shoe.getcard(), no_double=False)

            else:
                self.results.append(hand)
                print(self.results)


    def split(self, hand):
        hand.splithand(self.shoe)
        print(f"You split your hand")
        print(hand.hands[0].cards, hand.hands[1].cards)
        for i, h in enumerate(hand.hands):
            self.playhand(h, i)
        
    

    def PlayRound(self):
        self.results = []
        
        self.deal_first_cards()
        self.print_first_results()
        upcard = self.dealer.dealerupcard()
        

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

            
            result = self.winlose(hand)
            print(f"Hand {i+1}, {result=}")
            final_results.append(self.winlose(hand))



            
            
                    
        
      
        
        

table1 = Table(hands=2)
#table1.deal_first_cards()

table1.PlayRound()
        
        
