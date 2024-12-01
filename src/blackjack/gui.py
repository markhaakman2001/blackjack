from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from src.blackjack.gui_table import Table
import sys
import time


class BJinterface(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        
        self.num = 0

        central_widget =  QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.vbox = QtWidgets.QVBoxLayout(central_widget)
        self.deal_label= QtWidgets.QLabel(text="Dealer:")
        self.vbox.addWidget(self.deal_label)

        self.deal_info = QtWidgets.QTextEdit(self)
        self.deal_info.setReadOnly(True)
        self.vbox.addWidget(self.deal_info)

        self.hand_lbl = QtWidgets.QLabel(text="Your hands:")
        self.vbox.addWidget(self.hand_lbl)

        self.hand_info = QtWidgets.QTextEdit(self)
        self.hand_info.setReadOnly(True)
        self.vbox.addWidget(self.hand_info)

        self.display_txt = QtWidgets.QTextEdit(self)
        self.display_txt.setReadOnly(True)
        self.vbox.addWidget(self.display_txt)
        
        self.hbox_top = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(self.hbox_top)
        

        hbox = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(hbox)

        hbox2 = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(hbox2)

        hbox3 = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(hbox3)

        self.confirm_btn = QtWidgets.QPushButton(text="Confirm Bet")
        hbox3.addWidget(self.confirm_btn)

        self.hit_button = QtWidgets.QPushButton(text="hit")
        hbox.addWidget(self.hit_button)

        self.stand_button = QtWidgets.QPushButton(text="Stand")
        hbox.addWidget(self.stand_button)

        self.double_button = QtWidgets.QPushButton(text="Double")
        hbox.addWidget(self.double_button)

        self.split_button = QtWidgets.QPushButton(text="Split")
        hbox.addWidget(self.split_button)

        self.n_hands = QtWidgets.QSpinBox()
        hbox2.addWidget(self.n_hands)

        self.play_button = QtWidgets.QPushButton(text="Play")
        hbox2.addWidget(self.play_button)

        

        self.n_hands.setValue(2)
        self.n_hands.setMinimum(1)
        self.n_hands.setMaximum(8)
        
        self.hit_button.clicked.connect(self.hit)
        self.stand_button.clicked.connect(self.stand)

        self.play_button.clicked.connect(self.start_round)

        self.table = None

    @Slot()
    def update_txt(self, text):
        self.display_txt.clear()
        self.display_txt.append(text)

    @Slot()
    def update_dealer(self, text):
        self.deal_info.clear()
        self.deal_info.append(text)
    
    @Slot()
    def update_player(self, text):
        self.hand_info.clear()
        self.hand_info.append(text)

    @Slot()
    def first_cards(self):

        if self.table:
            self.table.deal_first_cards()
            first_results, dealerupcard = self.table.print_first_results()
            
            self.update_player(text = "\n".join([first_results[x] for x in range(len(first_results))]))
            
            self.update_dealer(dealerupcard)

    @Slot()
    def final_results(self):
        if self.table:
            results = [self.table.winlose(hand) for hand in self.table.hands]
            self.update_txt(f"\n".join([results[x] for x in range(len(results))]))
        

    def nexthand(self):

        if self.table:

            if self.lasthand():
                
                dealerplay = self.table.dealer.hand.dealerturn()
                dealer_updates = []

                while dealerplay:

                    dealer_card = self.table.shoe.getcard()
                    deal_txt = self.table.dealer.dealerplay(dealer_card)
                    dealer_updates.append(deal_txt)
                    self.update_dealer(text="\n".join([dealer_updates[i] for i in range(len(dealer_updates))]))
                    time.sleep(1)
                    dealerplay = self.table.dealer.hand.dealerturn()


                self.final_results()
            
            else:

                if self.table.hands[self.num].blackjack():
                    self.blackjack()

                else:
                    self.table.addresults(self.table.hands[self.num - 1])
                    hand = self.table.hands[self.num]
                    self.update_player(f"Hand {self.num + 1}, cards are {hand.cards}, total is {hand.handtotal(hand.softhand())}")
                    self.update_txt(f"Hand {self.num + 1}, pick an action")

    def lasthand(self):

        if self.table:

            if self.num == len(self.table.hands):
                return True
            else:
                return False
    
    def checkforbust(self):
        hand = self.table.hands[self.num]

        if hand.handtotal(hand.softhand()) >= 21:
            if hand.handtotal(hand.softhand()) ==  21:
                self.update_txt("You have 21.")
                time.sleep(1)
                hand.deactivate()
                self.num += 1
                self.nexthand()
            else:
                self.update_txt("You busted")
                time.sleep(1)
                hand.deactivate()
                self.num += 1
                
                self.nexthand()
        

    def hit(self):

        if self.table:
            card, text = self.table.hitcard(self.table.hands[self.num])
            self.update_txt(f"You hit, your new card is {card}.")
            self.update_player(text)
            time.sleep(0.5)
            self.checkforbust()

    def stand(self):

        if self.table:
            self.update_txt("You chose stand")
            self.table.hands[self.num].deactivate()
            self.num += 1
            time.sleep(1)
            self.nexthand()
    
    def blackjack(self):

        if self.table:
            self.update_txt(f"Hand {self.num + 1}, BlackJack!")
            self.table.hands[self.num].deactivate()
            self.num += 1
            time.sleep(1)
            self.nexthand()
    
    
    def start_round(self):
        self.num = 0
        self.table = Table(hands=2)
        self.update_txt("Round started, good luck!")
        time.sleep(1.5)
        self.first_cards()
        if self.table.hands[0].blackjack():
            self.blackjack()
        else:
            self.update_txt("Hand 1, pick an action")
        
        
        
            
        


                
                
                
        
        



def main():

    app = QtWidgets.QApplication(sys.argv)
    ui = BJinterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()