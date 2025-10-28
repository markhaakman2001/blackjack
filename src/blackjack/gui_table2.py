from blackjack.gui_hand import BlackJackHand, WinFunctions, WinType
from baccarat.baccarat_cards import Shoe, DeckOfCards, Card, CardSymbol, Kind, Color
from ErrorFiles.PlayingErrors import PlayingError,  BlackJackErrorChecker
from ErrorFiles.BankingErrors import BankingErrorChecker,  BalanceError,  BettingError
from UnifiedBanking.UnifiedBank import MainBank
from extrafiles.gametrackingtools import GameState
from blackjack.player import BlackJackPlayer, BlackJackDealer
from blackjack.BJanimations import EasyCardLabels
from blackjack.BJanimations import BlackJackAnimations as BJanim
from blackjack.blackjackfunctions import UpdateType
from PySide6.QtCore import Slot, Signal, QObject

class BlackJackTable:

    def __init__(self, bank : MainBank = MainBank(500)):
        self.bank   = bank
        self.player = BlackJackPlayer()
        self.dealer = BlackJackDealer()
        self.shoe   = Shoe(8)

        self._observers : list[function] = []

        self.player.add_points_observer(self.notify_gui)
        self.player.add_points_observer(self.check_hand_status)
        #self.dealer.add_points_observer(self.notify_gui_dealer)
    
    # def add_observer_points_changed(self, callback):
    #     self._observers.append(callback)

    def add_observer(self, callback):
        self._observers.append(callback)

    def StartRound_onehand(self):
        self.player.add_hands(1)
        for x in range(2):
            self.player.hit_card(self.shoe.getcard())
            self.dealer.hand.AddCard(self.shoe.getcard())
        
        return self.player.active_hand.cards, self.dealer.hand.cards
    
    def StartNhand(self, n_hands : int = 2):
        self.player.add_hands(n_hands)
        self.notify_gui(UpdateType.HANDS, self.player.hands)
        for x in range(2):
            for i in range(len(self.player.hands)):
                self.player.hit_card(self.shoe.getcard(), hand_nr=i)
            
            self.dealer.hit_card(self.shoe.getcard())


        cards , animgroup, cards_per_hand = BJanim.first_deal_animation(player=self.player, dealer=self.dealer)

        self.player.print_cards()
        self.dealer.print_cards()

        return cards, animgroup, cards_per_hand
    
    def hit(self):
        card = self.shoe.getcard()
        animated_card = BJanim.hit_card_animation(card, self.player.active_hand.hand_number, len(self.player.active_hand.cards), self.player.active_hand)
        self.player.hit_card(card)
        return animated_card
    
    def stand(self):
        self.player.stand()

    
    def split(self, cards):
        new_cards = self.shoe.getcard(n_cards=2)
        origin    = self.player.active_hand.hand_number
        new_hands = self.player.split_hand(new_cards)
        cards, animgroup, new_animated_cards = BJanim.split_animation(cards, new_cards, origin)
        # for hand in self.player.hands:
        #     print(f"Hand: {hand.hand_number}, origin: {hand.origin}")
        return cards, animgroup, new_animated_cards, new_hands

    def check_hand_status(self, *args):
        if args[0] == UpdateType.POINTS:
            if self.player.active_hand._get_handtotal() > 21:
                self.notify_gui(UpdateType.NEXTHAND, self.player.active_hand, 'BUST')
            elif self.player.active_hand._get_handtotal() == 21:
                self.notify_gui(UpdateType.NEXTHAND, self.player.active_hand, "21")
            else:
                pass
    
    def DealerTurn(self):

        while self.dealer.hand._get_handtotal() < 17:
            card = self.shoe.getcard()
            self.dealer.hit_card(card)
        
        cards, animations = BJanim.dealer_card_animations(self.dealer)
        return cards, animations

    def final_results(self):
        for hand in self.player.hands:
            result = hand.final_result(self.dealer.hand)
            self.notify_gui(UpdateType.RESULT, result, hand, hand._get_handtotal())

    
    def notify_gui(self, *args):
        for callback in self._observers:
            callback(*args)

    

    
        
