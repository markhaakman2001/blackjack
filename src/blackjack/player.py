from blackjack.gui_hand import BlackJackHand, BlackJackSplitHand, WinType
from baccarat.baccarat_cards import Card

class BlackJackPlayer:

    def __init__(self):
        self.hands        : list[BlackJackHand] = []
        self.active_hands : list[BlackJackHand] = []
        self.split_hands  : list[BlackJackHand] = []
    
    def add_hands(self, n_hands):

        for x in range(n_hands):
            hand_x = BlackJackHand(hand_number=x)
            self.hands.append(hand_x)
            self.active_hands.append(hand_x)
    
    def hit_card(self, card : Card):
        self.active_hand.AddCard(card)
    
    def stand(self):
        self.active_hand.deactivate()
        self.active_hands.pop(0)
        print(f"New active hand, origin: {self.active_hand.origin}, cards: {self.active_hand.cards[0]._get_value(), self.active_hand.cards[1]._get_value()}")
    
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

    
    @property
    def active_hand(self):
        self._active_hand_ = next(hand for hand in self.hands if hand._is_active)
        return self._active_hand_

class BlackJackDealer:

    def __init__(self):
        self.hand = BlackJackHand(0)
