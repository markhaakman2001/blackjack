from blackjack.gui_hand import BlackJackHand, WinFunctions, WinType
from baccarat.baccarat_cards import Shoe, DeckOfCards, Card, CardSymbol, Kind, Color
from ErrorFiles.PlayingErrors import PlayingError,  BlackJackErrorChecker
from ErrorFiles.BankingErrors import BankingErrorChecker,  BalanceError,  BettingError
from UnifiedBanking.UnifiedBank import MainBank
from extrafiles.gametrackingtools import GameState
from blackjack.player import BlackJackPlayer, BlackJackDealer
from blackjack.BJanimations import EasyCardLabels
from blackjack.BJanimations import BlackJackAnimations as BJanim

class BlackJackTable:

    def __init__(self, bank : MainBank = MainBank(500)):
        self.bank   = bank
        self.player = BlackJackPlayer()
        self.dealer = BlackJackDealer()
        self.shoe   = Shoe(8)
    
    def StartRound_onehand(self):
        self.player.add_hands(1)
        for x in range(2):
            self.player.hit_card(self.shoe.getcard())
            self.dealer.hand.AddCard(self.shoe.getcard())
        
        return self.player.active_hand.cards, self.dealer.hand.cards
    
    def StartNhand(self, n_hands : int = 2):
        self.player.add_hands(2)

        for x in range(2):
            for hand in self.player.hands:
                hand.AddCard(self.shoe.getcard())
            
            self.dealer.hand.AddCard(self.shoe.getcard())

        cards , animgroup = BJanim.first_deal_animation(player=self.player, dealer=self.dealer)
        self.player.print_cards()
        return cards, animgroup
        
