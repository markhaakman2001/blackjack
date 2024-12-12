from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QSize, QPoint
import PySide6.QtCore as Core
from src.blackjack.gui_table import Table
from src.blackjack.gui_shoehand import Hand
from src.extrafiles.labels import EasyCardLabels
import sys
import time


class BJinterface(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        

        central_widget =  QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.showFullScreen()
        

        self.vbox = QtWidgets.QVBoxLayout(central_widget)
        self.deal_label= QtWidgets.QLabel(text="Dealer:")
        self.vbox.addWidget(self.deal_label)

        self.deal_info = QtWidgets.QTextEdit(self)
        self.deal_info.setReadOnly(True)
        self.deal_info.size = QSize(100, 100)
        self.deal_info.resize(self.deal_info.size)
        self.deal_info.setParent(self)
        self.deal_info.show()

        self.hand_lbl = QtWidgets.QLabel(text="Your hands:")
        self.vbox.addWidget(self.hand_lbl)

        self.hand_info = QtWidgets.QTextEdit(self)
        self.hand_info.setReadOnly(True)
        self.hand_info.size = QSize(100, 100)
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
        self.double_button.clicked.connect(self.doubledown)
        self.split_button.clicked.connect(self.splityourhand)

        self.play_button.clicked.connect(self.start_round)

        self.table       = None     # table is initiated later
        self.splitornot  = False    # this is True if the current hand is a splithand
        self.split_flag  = False    # this is True if the current hand is split more than once
        self.num         = 0        # Keeps track of the index of the current main hand being played
        self.split_num   = 0        # Keeps track of the index of the current split hand being played
        self.card_labels = []       # This list holds all the card labels of the cards that have been revealed.
        self.popup_off   = True     # If there already is a popup this should be False

        self.timer = Core.QTimer()

    
    def update_txt(self, text):
        self.display_txt.clear()
        self.display_txt.append(text)

    
    def update_dealer(self, text):
        self.deal_info.clear()
        self.deal_info.append(text)
    
    
    def update_player(self, text):
        self.hand_info.clear()
        self.hand_info.append(text)

    
    def first_cards(self):

        if self.table:
            self.table.deal_first_cards()
            first_results, dealerupcard, first_symbols = self.table.print_first_results()
            
            for symbol in first_symbols[0]:
                symbol:str
                self.label = EasyCardLabels()
                self.label.setParent(self.popup)
                self.label.setnewimage(symbol)
                self.label.show()
            
            
            self.update_player(text = "\n".join([first_results[x] for x in range(len(first_results))]))
            print(first_results)
            self.update_dealer(dealerupcard)


    @Slot()
    def final_results(self):

        if self.table:
            if self.split_flag:
                results = []
                for i, hand in enumerate(self.table.hands):

                    if isinstance(hand, list):
                        results.append(f"\n".join([self.table.winlose(handx) for handx in hand]))
                        self.textboxes[i].append(f"\n".join([self.table.winlose(handx) for handx in hand]))
                    else:
                        results.append(self.table.winlose(hand))
                        self.textboxes[i].append(self.table.winlose(hand))
           
            else:
                results = [self.table.winlose(hand) for hand in self.table.hands]

            self.update_txt(f"\n".join([results[x] for x in range(len(results))]))
        

    def nexthand(self, split=False):
        """This method is called in the following cases: 1) whenever the player chooses stand. 2) Whenever the player busts. 3) Whenever the player has a blackjack or when his hard total is 21.
        The method iterates through the last hand and updates the results accordingly. When all hands are played the dealer will pull cards untill he reaches 17 or higher.

        Args:
            split (bool, optional): True if the hand is a splithand. Defaults to False.
        """        


        if self.table:
            
            split = self.splitornot

            # check if the current hand is a split hand
            if split:
                
                texts = []

                # check the splithands cards
                for i, hand in enumerate(self.table.hands[self.num]):
                    texts.append(f"Splithand {i+1}: {hand.cards}: {hand.handtotal(hand.softhand())}")

                
                self.textboxes[self.num].clear()
                self.textboxes[self.num].append("\n".join([text for text in texts]))

                # check if the splithand is the last hand in the current split
                if  self.split_num == (len(self.table.hands[self.num])):
                    
                    self.num       += 1            
                    self.split_num  = 0            
                    self.splitornot = False
                    
                    # also check if this hand is the final hand for all main hands
                    if self.lasthand():
                        self.nexthand()
                    
                    # update texts
                    else:
                        hand = self.table.hands[self.num]
                        self.update_player(f"Hand {self.num + 1}, cards are {hand.cards}, total is {hand.handtotal(hand.softhand())}")
                        self.update_txt(f"Hand {self.num + 1}, pick an action")
                        self.nexthand()

                
                else:

                    if self.table.hands[self.num][self.split_num].blackjack():
                        self.blackjack()
                    else:
                        self.update_txt(f"Splithand {self.split_num + 1}, pick an action")
                


            else:
                
                # if the last hand is a list, then it was a split and the results must be updated accordingly
                if isinstance(self.table.hands[self.num - 1], list):
                    texts = []

                    for i, hand in enumerate(self.table.hands[self.num - 1]):
                        texts.append(f"Splithand {i+1}: {hand.cards}: {hand.handtotal(hand.softhand())}")

                
                    self.textboxes[self.num - 1].clear()
                    self.textboxes[self.num - 1].append("\n".join([text for text in texts]))

                else:
                    self.textboxes[self.num - 1].append(f"{self.table.hands[self.num - 1].cards} : {self.table.hands[self.num - 1].handtotal(self.table.hands[self.num - 1].softhand())} \n")
                
                # if the lasthand was played, then its the dealers turn to play
                if self.lasthand():
                    
                    dealer = self.table.dealer
                    dealer_updates = []
                    
                    dealer_updates.append(f"Dealer shows {dealer.hand.cards}, total is {dealer.hand.handtotal(dealer.hand.softhand())}")
                    self.update_dealer(dealer_updates[0])

                    # while the dealer has less than 17 he must hit a card
                    dealerplay = dealer.hand.dealerturn()
                    while dealerplay:
                        
                        dealer_updates.append(self.table.dealer_play())
                        self.update_dealer(text="\n".join([dealer_updates[i] for i in range(len(dealer_updates))]))
                        
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
    
    
    def checkforbust(self, split=False):
        if self.table:
            
            split = self.splitornot

            if split:

                hand: Hand = self.table.hands[self.num][self.split_num]

                if hand.handtotal(hand.softhand()) >= 21:
                    text = self.table.checkforbust(hand)
                    self.update_txt(text)
                    self.split_num += 1
                    self.nexthand()
                
            else:

                hand = self.table.hands[self.num]

                if hand.handtotal(hand.softhand()) >= 21:
                    
                    text = self.table.checkforbust(hand)
                    self.update_txt(text)
                    self.num += 1
                    self.nexthand()
        

    def hit(self, split=False):

        if self.table:
            
            split = self.splitornot

            if split:

                card, text = self.table.hitcard(self.table.hands[self.num][self.split_num])
                self.update_txt(f"You hit, your new card is {card}.")
                self.update_player(text)
                self.checkforbust()
                      
            else:

                card, text = self.table.hitcard(self.table.hands[self.num])
                self.update_txt(f"You hit, your new card is {card}.")
                self.update_player(text)
                self.checkforbust()

    def stand(self, split=False):

        if self.table:

            split = self.splitornot

            if split:
                
                self.update_txt("You chose stand")
                #self.table.hands[self.num][n].deactivate
                self.split_num += 1
                self.nexthand()

            else:               
                self.update_txt("You chose stand")
                #self.table.hands[self.num].deactivate()
                self.num += 1
                
                self.nexthand()
    
    def doubledown(self, split=False):

        if self.table:
            split = self.splitornot
            if split:
                n          = self.split_num
                hand       = self.table.hands[self.num][n]
                card, text = self.table.hitcard(hand)
                self.update_txt(f"You doubled, your new card is {card}.")
                self.update_player(text)
                self.split_num += 1

                self.nexthand()

            else:
                hand       = self.table.hands[self.num]
                card, text = self.table.hitcard(hand)
                self.update_txt(f"You doubled, your new card is {card}.")
                self.update_player(text)
                self.num += 1

                self.nexthand()

    def splityourhand(self):

        if self.table:
            
            current_textbox = self.textboxes[self.num]

            if self.splitornot:
                current_hand = self.table.hands[self.num][self.split_num]
                texts, hands = self.table.split(current_hand)
                current_textbox.append(f"\n".join([text for text in texts]))
                self.table.hands[self.num].pop(self.split_num)
                self.table.hands[self.num].insert(self.split_num, hands[1])
                self.table.hands[self.num].insert(self.split_num, hands[0])
                if self.table.hands[self.num][self.split_num].blackjack():                
                    self.blackjack()
                else:
                    self.update_txt("Splithand 1, pick an action")


            else:

                self.split_flag = True
                self.splitornot = True
                current_hand    = self.table.hands[self.num]
                texts, hands    = self.table.split(current_hand)

                current_textbox.clear()
                current_textbox.append(f"\n".join([text for text  in texts]))
                self.table.hands.pop(self.num)

                if self.lasthand():

                    self.table.hands.append(hands)
                else:

                    self.table.hands.insert(self.num, hands)

                if self.table.hands[self.num][0].blackjack():                
                    self.blackjack()
                else:
                    self.update_txt("Splithand 1, pick an action")
            

    def blackjack(self, split=False):

        if self.table:
            split = self.splitornot
            n = self.split_num
            if split:
                
                self.update_txt(f"Splithand {self.split_num + 1}, BlackJack!")
                #self.table.hands[self.num][n].deactivate()
                self.split_num += 1
                
                self.nexthand()

            
            else:

                self.textboxes[self.num].append(f"{self.table.hands[self.num].cards}, Blackjack \n")
                self.update_txt(f"Hand {self.num + 1}, BlackJack!")
                #self.table.hands[self.num].deactivate()
                self.num += 1
                
                self.nexthand()
    
    
    def start_round(self):
        self.createpopupwindow()
        self.num       = 0
        self.table     = Table(hands=self.n_hands.value())
        self.textboxes = []

        for x in range(self.n_hands.value()):
            txtbox = QtWidgets.QTextEdit()
            txtbox.setReadOnly(True)
            txtbox.append(f"Hand {x+1}: \n")
            self.textboxes.append(txtbox)
            self.hbox_top.addWidget(txtbox)
            
        self.update_txt("Round started, good luck!")
        time.sleep(1.5)
        self.first_cards()
        if self.table.hands[0].blackjack():
            self.blackjack()
        else:
            self.update_txt("Hand 1, pick an action")


    def createpopupwindow(self):
        if self.popup_off:
            self.popup = QtWidgets.QDialog(self)

            self.popup.resize(QSize(1000, 1000))
            self.popup.show()
            




    def CreateCardLabel(self, card_symbol:str):

        if not self.popup_off:
            self.label : EasyCardLabels = EasyCardLabels()
            self.label.setnewimage(card_symbol)
            
            return self.label
            
            

    def destroypopup(self):
        try:
            self.popup.destroy()
            self.popup_off = True
        except AttributeError:
            pass









def main():

    app = QtWidgets.QApplication(sys.argv)
    ui = BJinterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()