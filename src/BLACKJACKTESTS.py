from blackjack.gui_hand import BlackJackHand
from baccarat.baccarat_cards import Shoe, Card, Kind, CardSymbol, Color
from blackjack.player import BlackJackPlayer, BlackJackDealer
import sys
from blackjack.gui2 import BlackJackGUI
from PySide6 import QtWidgets

def main():
    hand1 = BlackJackHand()
    hand2 = BlackJackHand()
    shoe1 = Shoe(1)
    for x in range(2):
        hand1.AddCard(shoe1.getcard())
        hand2.AddCard(shoe1.getcard())

    print(f"hand 1 (player test): cards are {[card._get_value() for card in hand1.cards]}, total value is {hand1._get_handtotal()} \n blackjack is {hand1._is_blackjack()}")
    print(f"Hand 2 (dealer test): cards are {[card._get_value() for card in hand2.cards]}, total value is {hand2._get_handtotal()} \n blackjack is {hand2._is_blackjack()}. dealer should hit is {hand2.DealerTurn()} ")
    print(f"WHO WINS? {hand1.final_result(hand2)}")


def PlayerTests():
    ace = Card(Kind.DIAMOND, CardSymbol.ACE)
    ten = Card(Kind.CLOVER, CardSymbol.TEN)
    five = Card(Kind.CLOVER, CardSymbol.FIVE)

    shoe = Shoe(1)
    player = BlackJackPlayer()
    player.add_hands(1)
    player.hit_card(shoe.getcard())
    player.hit_card(ace)
    player.split_hand([ten, five])
    player.stand()


def UItests():
    app = QtWidgets.QApplication(sys.argv)
    ui  = BlackJackGUI()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    UItests()