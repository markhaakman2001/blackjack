from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from src.blackjack.gui_table import Table
import sys
import time


class BJinterface(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        

        central_widget =  QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.vbox = QtWidgets.QVBoxLayout(central_widget)
        self.deal_label= QtWidgets.QLabel(text="Dealer:")
        self.vbox.addWidget(self.deal_label)

        self.deal_info = QtWidgets.QTextEdit(self)
        self.deal_info.setReadOnly(True)
        self.vbox.addWidget(self.deal_info)

        self.hand_lbl = QtWidgets.QLabel(text="Your hand:")
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

        self.double_button.clicked.connect(self.double_text)
        self.hit_button.clicked.connect(self.hit_text)
        self.stand_button.clicked.connect(self.stand_text)
        self.split_button.clicked.connect(self.split_text)

        self.play_button.clicked.connect(self.start_round)

        self.table = None

    def update_txt(self, text):
        self.display_txt.clear()
        self.display_txt.append(text)

    def update_player_hand(self):

        if self.table:
            

    def hit(self):

        if self.table:
            card = self.table.shoe.getcard()
            self.table.player.hands[0].addcard(card)
            self.update_txt(f"You hit and received: {card}.")
            self.update_player_hand()
    
    @Slot()
    def start_round(self):
        
        



def main():

    app = QtWidgets.QApplication(sys.argv)
    ui = BJinterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()