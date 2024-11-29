from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from src.blackjack.table import Table
import sys
import time


class BJinterface(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        
        central_widget =  QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        self.vbox = QtWidgets.QVBoxLayout(central_widget)
        self.text_edit = QtWidgets.QTextEdit()
        self.vbox.addWidget(self.text_edit)

        self.hbox_top = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(self.hbox_top)

        hbox = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(hbox)

        hbox2 = QtWidgets.QHBoxLayout()
        self.vbox.addLayout(hbox2)

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

    @Slot()
    def stand_text(self):
        self.text_edit.clear()
        self.text_edit.append("You stand")
    
    @Slot()
    def hit_text(self):
        self.text_edit.clear()
        self.text_edit.append("You hit")
    
    @Slot()
    def split_text(self):
        self.text_edit.clear()
        self.text_edit.append("You split")

    @Slot()
    def double_text(self):
        self.text_edit.clear()
        self.text_edit.append("You doubled")
    
    @Slot()
    def start_round(self):
        self.text_edit.clear()
        self.text_edit.append("Round Started")
        time.sleep(2)
        self.text_edit.clear()
        self.text_edit.append("Dealer:")
        self.hands = []
        for x in range(self.n_hands.value()):
            hand_ui = QtWidgets.QTextEdit()
            hand_ui.windowTitle()
            hand_ui.append(f"Hand {x}")
            
            self.hands.append(hand_ui)
            self.hbox_top.addWidget(hand_ui)

        table = Table(hands=self.n_hands.value())
        #table.PlayRound()
        



def main():

    app = QtWidgets.QApplication(sys.argv)
    ui = BJinterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()