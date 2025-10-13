from blackjack.gui_hand import BlackJackHand, WinFunctions, WinType
from baccarat.baccarat_cards import Shoe, DeckOfCards, Card, CardSymbol, Kind, Color
from ErrorFiles.PlayingErrors import PlayingError,  BlackJackErrorChecker
from ErrorFiles.BankingErrors import BankingErrorChecker,  BalanceError,  BettingError
from UnifiedBanking.UnifiedBank import MainBank
from extrafiles.gametrackingtools import GameState
from blackjack.player import BlackJackPlayer, BlackJackDealer

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