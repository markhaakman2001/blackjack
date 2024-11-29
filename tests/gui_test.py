import sys
import time
from PySide6 import QtCore, QtWidgets
from src.blackjack.shoehand import Shoe, Hand, Bank
from src.blackjack.playerdealer import Player, Dealer
from src.blackjack.table import Table  # Assuming this is your main game logic

class BJinterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Blackjack")
        self.setGeometry(100, 100, 800, 600)  # Width, Height of the window

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.vbox = QtWidgets.QVBoxLayout(self.central_widget)

        # Text Edit for displaying messages like player actions and results
        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.vbox.addWidget(self.text_edit)

        # Betting UI
        self.bet_label = QtWidgets.QLabel("Place Your Bet:")
        self.bet_input = QtWidgets.QLineEdit()
        self.bet_button = QtWidgets.QPushButton("Confirm Bet")
        self.bet_button.clicked.connect(self.place_bet)
        self.vbox.addWidget(self.bet_label)
        self.vbox.addWidget(self.bet_input)
        self.vbox.addWidget(self.bet_button)

        # Player's hand display
        self.player_hand_label = QtWidgets.QLabel("Your Hand:")
        self.vbox.addWidget(self.player_hand_label)

        # Buttons for actions
        self.button_layout = QtWidgets.QHBoxLayout()

        self.hit_button = QtWidgets.QPushButton("Hit")
        self.hit_button.clicked.connect(self.hit)
        self.button_layout.addWidget(self.hit_button)

        self.stand_button = QtWidgets.QPushButton("Stand")
        self.stand_button.clicked.connect(self.stand)
        self.button_layout.addWidget(self.stand_button)

        self.split_button = QtWidgets.QPushButton("Split")
        self.split_button.clicked.connect(self.split)
        self.button_layout.addWidget(self.split_button)

        self.double_button = QtWidgets.QPushButton("Double")
        self.double_button.clicked.connect(self.double)
        self.button_layout.addWidget(self.double_button)

        self.vbox.addLayout(self.button_layout)

        # Play Button
        self.play_button = QtWidgets.QPushButton("Play")
        self.play_button.clicked.connect(self.start_game)
        self.vbox.addWidget(self.play_button)

        self.table = None  # Will initialize later when starting a game
        
    def update_text(self, text):
        """Helper function to update the game status on the text area"""
        self.text_edit.clear()
        self.text_edit.append(text)

    def start_game(self):
        """Start a new round"""
        self.table = Table(hands=1)  # Initialize the table (game logic)
        self.update_text("Round Started!\n")
        self.place_bet()
        self.table.deal_first_cards()
        self.update_text("Cards dealt. Your turn.")
        self.update_player_hand()

    def place_bet(self):
        """Place bet based on input"""
        try:
            bet = float(self.bet_input.text())
            if bet <= 0:
                raise ValueError("Bet must be greater than zero")
            self.update_text(f"Bet placed: ${bet}")
            self.table.bank.betamount(self.table.player.hands[0], bet)
        except ValueError as e:
            self.update_text(f"Error placing bet: {e}")
        
    def update_player_hand(self):
        """Display the current state of player's hand"""
        hands_text = "\n".join([f"Hand {i + 1}: {hand.cards} Total: {hand.handtotal(hand.softhand())}" for i, hand in enumerate(self.table.player.hands)])
        self.player_hand_label.setText(f"Your Hand:\n{hands_text}")

    def hit(self):
        """Player chooses to hit"""
        if self.table:
            card = self.table.shoe.getcard()
            self.table.player.hands[0].addcard(card)
            self.update_text(f"You hit and received: {card}.")
            self.update_player_hand()
            self.check_bust()

    def stand(self):
        """Player chooses to stand"""
        if self.table:
            self.update_text("You stand. The dealer's turn now.")
            self.dealer_turn()

    def split(self):
        """Player chooses to split hand"""
        if self.table:
            hand = self.table.player.hands[0]
            if len(hand.cards) == 2 and hand.cards[0] == hand.cards[1]:
                self.table.player.hands[0].splithand(self.table.shoe, self.table.bank)
                self.update_text("You split your hand!")
                self.update_player_hand()
            else:
                self.update_text("You can't split this hand.")

    def double(self):
        """Player chooses to double down"""
        if self.table:
            hand = self.table.player.hands[0]
            self.table.bank.doubled(0)  # Assuming we are doubling the first hand
            card = self.table.shoe.getcard()
            hand.addcard(card)
            self.update_text(f"You doubled down and received: {card}.")
            self.update_player_hand()
            self.check_bust()

    def dealer_turn(self):
        """Dealer's turn to play"""
        dealer_total = self.table.dealer.hand.handtotal(self.table.dealer.hand.softhand())
        while dealer_total < 17:
            card = self.table.shoe.getcard()
            self.table.dealer.dealerplay(card)
            dealer_total = self.table.dealer.hand.handtotal(self.table.dealer.hand.softhand())
            self.update_text(f"Dealer's total is {dealer_total}.")
        
        self.show_results()

    def show_results(self):
        """Show game results (Win, Lose, Push)"""
        results = []
        for i, hand in enumerate(self.table.player.hands):
            result = self.table.winlose(hand)
            results.append(f"Hand {i + 1}: {result}")
        self.update_text("\n".join(results))
        self.reset_game()

    def reset_game(self):
        """Reset the game for the next round"""
        self.table = None  # Reset table to start new round
        self.bet_input.clear()
        self.update_text("Game Over. Start a new round!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = BJinterface()
    window.show()
    sys.exit(app.exec())