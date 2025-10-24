from blackjack.gui_hand import BlackJackHand, WinFunctions, WinType
from baccarat.baccarat_cards import Shoe, DeckOfCards, Card, CardSymbol, Kind, Color
from ErrorFiles.PlayingErrors import PlayingError,  BlackJackErrorChecker
from ErrorFiles.BankingErrors import BankingErrorChecker,  BalanceError,  BettingError
from UnifiedBanking.UnifiedBank import MainBank
from extrafiles.gametrackingtools import GameState
from blackjack.player import BlackJackPlayer, BlackJackDealer
from blackjack.BJanimations import EasyCardLabels
from blackjack.BJanimations import BlackJackAnimations as BJanim
from PySide6.QtCore import Slot, Signal, QObject

class BlackJackTable:

    def __init__(self, bank : MainBank = MainBank(500)):
        self.bank   = bank
        self.player = BlackJackPlayer()
        self.dealer = BlackJackDealer()
        self.shoe   = Shoe(8)

        self._observers : list[function] = []

        self.player.add_points_observer(self.notify_gui_points)
        #self.dealer.add_points_observer(self.notify_gui_dealer)
    
    def add_observer_points_changed(self, callback):
        self._observers.append(callback)


    def StartRound_onehand(self):
        self.player.add_hands(1)
        for x in range(2):
            self.player.hit_card(self.shoe.getcard())
            self.dealer.hand.AddCard(self.shoe.getcard())
        
        return self.player.active_hand.cards, self.dealer.hand.cards
    
    def StartNhand(self, n_hands : int = 2):
        self.player.add_hands(n_hands)

        for x in range(2):
            for i in range(len(self.player.hands)):
                self.player.hit_card(self.shoe.getcard(), hand_nr=i)
            
            self.dealer.hit_card(self.shoe.getcard())

        cards , animgroup = BJanim.first_deal_animation(player=self.player, dealer=self.dealer)
        self.player.print_cards()
        self.dealer.print_cards()

        return cards, animgroup
    
    def hit(self):
        card = self.shoe.getcard()
        self.player.hit_card(card)
        animated_card = BJanim.hit_card_animation(card, self.player.active_hand.hand_number, len(self.player.active_hand.cards))
        return animated_card


    def notify_gui_points(self, *args):
        for callback in self._observers:
            callback(*args)

    
        
