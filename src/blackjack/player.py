from shiboken6 import Object
from blackjack.gui_hand import BlackJackHand, BlackJackSplitHand, WinType
from baccarat.baccarat_cards import Card
from blackjack.blackjackfunctions import UpdateType


class BlackJackPlayer:


    def __init__(self):

        self.hands        : list[BlackJackHand] = []
        self.active_hands : list[BlackJackHand] = []
        self.split_hands  : list[BlackJackHand] = []

        self._points_observers : list[function] = []
        
    
    def add_points_observer(self, callback):
        self._points_observers.append(callback)

    def add_hands(self, n_hands):

        for x in range(n_hands):
            hand_x = BlackJackHand(hand_number=x)
            self.hands.append(hand_x)
            self.active_hands.append(hand_x)
    
    def hit_card(self, card : Card, hand_nr : int | None = None):
        if hand_nr:
            hand = self.hands[hand_nr]
        else:
            hand = self.active_hand
        hand.AddCard(card)
        self.notify_points_observer(UpdateType.POINTS, hand._get_handtotal(), hand.hand_number)

    def stand(self):
        self.active_hand.deactivate()
        self.active_hands.pop(0)
        if self.active_hand:
            if self.active_hand._is_blackjack():
                self.notify_points_observer(UpdateType.NEXTHAND, self.active_hand.hand_number, 'BlackJack!')
        #print(f"New active hand, origin: {self.active_hand.origin}, cards: {self.active_hand.cards[0]._get_value(), self.active_hand.cards[1]._get_value()}")
    
    def split_hand(self, new_cards):
        
        number = self.active_hand.hand_number
        card1 = self.active_hand.cards[0]
        card2 = self.active_hand.cards[1]
        split_hand1 = BlackJackSplitHand(hand_number=number, card1=card1, newcard=new_cards[0])
        split_hand2 = BlackJackSplitHand(hand_number=number, card1=card2, newcard=new_cards[1])
        self.hands.pop(number)
        self.hands.insert(number, split_hand2)
        self.hands.insert(number, split_hand1)
        print(f"SPLIT!, new active hand: {self.active_hand.origin}, cards: {self.active_hand.cards[0]._get_value(), self.active_hand.cards[1]._get_value()}")
    

    def print_cards(self):
        for i, hand in enumerate(self.hands):
            print(f"Hand {i}, cards: {[card._get_CardName() for card in hand.cards]}, ")

    
    def notify_points_observer(self, *args):
        for callback in self._points_observers:
            callback(*args)

    @property
    def active_hand(self):
        self._active_hand_ = next((hand for hand in self.hands if hand._is_active), None)
        if not self._active_hand_:
            self.notify_points_observer(UpdateType.DEALERTURN)
            return
        else:
            return self._active_hand_

        
    

class BlackJackDealer:

    def __init__(self):
        self.hand = BlackJackHand(0)
        self._points_observers = []
    
    def add_points_observer(self, callback):
        self._points_observers.append(callback)

    def print_cards(self):
        upcard = self.hand.cards[0]
        second_card = self.hand.cards[1]
        print(f"Dealer Upcard: {upcard._get_CardName()}, down card: {second_card._get_CardName()}")
    
    def hit_card(self, card : Card):
        self.hand.AddCard(card)
        self.notify_points_observers(self.hand._get_handtotal())


    def notify_points_observers(self, new_value, *args):
        for callback in self._points_observers:
            callback(new_value, *args)
    

