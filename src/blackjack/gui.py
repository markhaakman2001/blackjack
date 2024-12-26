from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QSize, QPoint, QSequentialAnimationGroup, QParallelAnimationGroup, QPropertyAnimation
import PySide6.QtCore as Core
from src.blackjack.gui_table import Table
from src.blackjack.gui_shoehand import Hand, Bank, WinFunctions, WinType
from src.extrafiles.labels import EasyCardLabels
from src.extrafiles.backgroundwidget import BackGroundWidget
from src.extrafiles.BaccaratButtons import BaccaratFicheOptionMenu, BaccaratFiche
from src.extrafiles.CustomButtons import BlackJackBetButton, WhichButton
import sys
import time



class BJinterface(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        
        self.central_widget =  BackGroundWidget()
        self.central_widget.setParent(self)     
        self.resize(1000, 700)
        self.central_widget.resize(QSize(1000, 700))

        self.dealer_handlabel = QtWidgets.QLabel()
        self.dealer_handlabel.resize(QSize(80, 40))
        self.dealer_handlabel.move(QPoint(490, 230))
        self.dealer_handlabel.setStyleSheet("border: 2px solid gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
        
        self.bank_label = QtWidgets.QLabel(text="Current funds: \n")
        self.bank_label.setParent(self)
        self.bank_label.resize(QSize(80, 100))
        self.bank_label.move(QPoint(0, 620))
        self.bank_label.show()


        self.confirm_btn   = QtWidgets.QPushButton(text="Confirm Bet")
        self.hit_button    = QtWidgets.QPushButton(text="hit")
        self.stand_button  = QtWidgets.QPushButton(text="Stand")
        self.double_button = QtWidgets.QPushButton(text="Double")
        self.split_button  = QtWidgets.QPushButton(text="Split")
        self.n_hands       = QtWidgets.QSpinBox()
        self.play_button   = QtWidgets.QPushButton(text="Play")


        self.BetSizeDialog       = BaccaratFicheOptionMenu(self)
        self.OpenBetSizeMenu     = QtWidgets.QPushButton(text="BetSize")
        self.CurrentBetSizeImage = BaccaratFiche()
        self.CurrentBetSizeImage.setEnabled(False)
        self.CurrentBetSizeImage.SetOneValueFiche()

        self.CurrentBetSizeImage.setParent(self)
        self.OpenBetSizeMenu.setParent(self)

        self.extra_elevations   = [-40, -20, 0, 0, 0, -20, -40]
        self.hand_label_list    = []
        
        self.hit_button.setParent(self)
        self.stand_button.setParent(self)
        self.double_button.setParent(self)
        self.split_button.setParent(self)
        self.n_hands.setParent(self)
        self.play_button.setParent(self)

        # Resize buttons
        self.hit_button.resize(QSize(250, 35))
        self.stand_button.resize(QSize(250, 35))
        self.double_button.resize(QSize(250, 35))
        self.split_button.resize(QSize(250, 35))
        self.n_hands.resize(QSize(250, 35))
        self.play_button.resize(QSize(250, 35))

        self.OpenBetSizeMenu.resize(QSize(500, 35))
        self.CurrentBetSizeImage.resize(QSize(50, 50))
        
        # move to correct position
        self.double_button.move(QPoint(0, 600))
        self.hit_button.move(QPoint(250, 600))
        self.stand_button.move(QPoint(500, 600))
        self.split_button.move(QPoint(750, 600))
        self.n_hands.move(QPoint(250, 635))
        self.play_button.move(QPoint(500, 635))
        self.OpenBetSizeMenu.move(QPoint(250, 670))
        self.CurrentBetSizeImage.move(QPoint(200, 635))


        self.hit_button.setStyleSheet("background-color: green; color:white; font: bold 20px")
        self.stand_button.setStyleSheet("background-color: red; color:white; font: bold 20px")
        self.split_button.setStyleSheet("background-color: blue; color:white; font: bold 20px")
        self.double_button.setStyleSheet("background-color: orange; color:white; font: bold 20px")

        # show them
        self.hit_button.show()
        self.double_button.show()
        self.stand_button.show()
        self.split_button.show()
        self.n_hands.show()
        self.play_button.show()
        

        self.n_hands.setValue(2)
        self.n_hands.setMinimum(1)
        self.n_hands.setMaximum(7)
        
        # connect buttons to the right methods
        self.hit_button.clicked.connect(self.hit)
        self.stand_button.clicked.connect(self.stand)
        self.double_button.clicked.connect(self.doubledown)
        self.split_button.clicked.connect(self.splityourhand)
        self.play_button.clicked.connect(self.start_round)
        
        self.OpenBetSizeMenu.clicked.connect(self.ShowBetSizeMenu)
        self.BetSizeDialog.BetSizeSignal.connect(self.ChangeCurrentBetSize)
        self.n_hands.valueChanged.connect(self.UpdatePossibleBets)


        self.table         = None     # table is initiated later
        self.splitornot    = False    # this is True if the current hand is a splithand
        self.split_flag    = False    # this is True if the current hand is split more than once
        self.num           = 0        # Keeps track of the index of the current main hand being played
        self.split_num     = 0        # Keeps track of the index of the current split hand being played
        self.card_labels   = []       # This list holds all the card labels of the cards that have been revealed.
        self.popup_off     = True     # If there already is a popup this should be False
        self.dealer_labels = []
        self.BetsLabelList = None

        self.bets_list     = []
        self.bank          = Bank(500)
        self.bank.FundsChanged.connect(self.update_funds)
        self.UpdatePossibleBets()
        self.update_funds()
    

    def UpdatePossibleBets(self):

        if self.BetsLabelList:

            for label in self.BetsLabelList:
                label     : QtWidgets.QLabel
                label.deleteLater()
                
        
        n_bets = self.n_hands.value()
        self.BetsLabelList : list[QtWidgets.QLabel]      = []
        self.BetButtonList : list[BlackJackBetButton]    = []
        self.bets_list                                   = [0] * n_bets
        
        for x in range(n_bets):

            yposition   = 582 + int(self.extra_elevations[x])
            xposition   = 65 + x * 128
            self.CurrentBetLabel    = QtWidgets.QLabel()
            self.PlaceBetButton     = BlackJackBetButton()
            self.PlaceBetButton.setText("Bet")
            self.PlaceBetButton._x_button = x

            self.PlaceBetButton.setParent(self)
            self.CurrentBetLabel.setParent(self)

            self.CurrentBetLabel.setStyleSheet("color: black ; font: bold 15px")

            self.PlaceBetButton.resize(QSize(60, 30))
            self.CurrentBetLabel.resize(QSize(60, 20))

            self.PlaceBetButton.move(QPoint(xposition, yposition - 30))
            self.CurrentBetLabel.move(QPoint(xposition, yposition))
            
            self.BetsLabelList.append(self.CurrentBetLabel)
            self.BetButtonList.append(self.PlaceBetButton)
            self.BetButtonList[x].xButtonSignal.connect(self.UpdateBetLabel)
            self.BetButtonList[x].xButtonSignal.connect(self.PlaceBetBank)
            
            self.PlaceBetButton.show()
            self.CurrentBetLabel.show()

    def PlaceBetBank(self):
        self.bank.PlaceOneBet()

    @Slot(WhichButton, name="xButton")
    def UpdateBetLabel(self, signal: WhichButton):
        x             = signal.value
        current_bet   = self.bank.BetSize
        current_label = self.BetsLabelList[x]
        NewBet = self.bets_list[x] + current_bet
        self.bets_list[x] = NewBet
        current_label.clear()
        current_label.setText(f"${NewBet}")
        current_label.update()


    @Slot(int, name="BetSize")
    def ChangeCurrentBetSize(self, signal):
        if signal == 1:
            self.CurrentBetSizeImage.SetOneValueFiche()
        elif signal == 5:
            self.CurrentBetSizeImage.SetFiveValueFiche()
        elif signal == 25:
            self.CurrentBetSizeImage.SetTwentyFiveValueFiche()
        elif signal == 100:
            self.CurrentBetSizeImage.SetOneHundredValueFiche()
        self.bank.BetSize = signal
        self.CurrentBetSizeImage.update()

    @Slot()
    def ShowBetSizeMenu(self):
        self.BetSizeDialog.exec()

    @Slot(int)
    def update_funds(self):
        self.bank_label.clear()
        self.bank_label.setText(f"Balance: \n  ${self.bank.funds} \n Total bet: \n ${self.bank.TotalBet}")
        self.bank_label.update()
    

    def check_available_buttons(self, hand: Hand):
        split_flag  = lambda : hand.cards[0] == hand.cards[1] and len(hand.cards) == 2
        double_flag = lambda : len(hand.cards) == 2
        s_flag = split_flag()
        d_flag = double_flag()
        self.split_button.setEnabled(s_flag)
        self.double_button.setEnabled(d_flag)


    def first_cards(self):
        
        if self.table:
            self.table.deal_first_cards()
            first_results, dealerupcard, first_symbols, dealer_symbols = self.table.print_first_results()
            
            for x in range(len(self.table.hands)):

                hand : Hand            = self.table.hands[x]
                label : EasyCardLabels = self.hand_label_list[x]
                label.clear()
                label.setText(f"{hand.handtotal(hand.softhand())}")
                label.update()

            self.firstanimations(first_symbols, dealer_symbol=dealer_symbols[0])

    def RoundFinished(self):
        self.NextRoundButton = QtWidgets.QPushButton(text="Next Round")
        self.NextRoundButton.setParent(self)
        self.play_button.setEnabled(False)
        self.play_button.update()

        self.NextRoundButton.resize(QSize(250, 35)) 
        self.NextRoundButton.move(QPoint(750, 635))
        self.NextRoundButton.clicked.connect(self.ClearCurrentTable)
        self.NextRoundButton.show()

    @Slot()
    def final_results(self):

        if self.table:


            results = []
            
            for i, hand in enumerate(self.table.hands):
                
                if isinstance(hand, list):
                    labels : QtWidgets.QLabel = self.hand_label_list[i]
                    for hand, label in zip(hand, labels):
                        bank  : Bank     = self.bank
                        result : WinType = self.table.winlose(hand)
                        amount_won       = bank.win_amount(result, hand)
                        label.clear()
                        label.setText(f"{result.name}\n ${amount_won/100}")
                        label.update()
                        self.update_funds()
                        self.RoundFinished()

                else:
                    results.append(self.table.winlose(hand))

                    result : WinType         = self.table.winlose(hand)
                    label : QtWidgets.QLabel = self.hand_label_list[i]
                    bank  : Bank             = self.bank
                    amount_won               = bank.win_amount(result, hand)
                    label.clear()
                    label.setText(f"{result.name} \n ${amount_won/100}")
                    label.update()
                    self.update_funds()
                    self.RoundFinished()
  
                
    
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


                label: QtWidgets.QLabel = self.hand_label_list[self.num][self.split_num-1]
                label.setStyleSheet("border: 2px dashed gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
                label.update()

                # check the splithands cards
                for i, hand in enumerate(self.table.hands[self.num]):
                    texts.append(f"Splithand {i+1}: {hand.cards}: {hand.handtotal(hand.softhand())}")
                    self.check_available_buttons(hand)
                    label : QtWidgets.QLabel = self.hand_label_list[self.num][i]
                    label.clear()
                    label.setText(f"{hand.handtotal(hand.softhand())}")
                    label.update()
                
                
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
                        label : QtWidgets.QLabel = self.hand_label_list[self.num]
                        label.setStyleSheet("border: 3px solid white; border-radius: 1px ; font : bold 10px ; background: lightgreen")
                        label.update()

                        hand = self.table.hands[self.num]
                        self.check_available_buttons(hand)
                        self.nexthand()

                
                else:

                    if self.table.hands[self.num][self.split_num].blackjack():
                        self.blackjack()
                    else:
                        label : QtWidgets.QLabel = self.hand_label_list[self.num][self.split_num]
                        label.setStyleSheet("border: 3px solid white; border-radius: 1px ; font : bold 10px ; background: lightgreen")
                        label.update()
                


            else:
                
                # if the last hand is a list, then it was a split and the results must be updated accordingly
                if isinstance(self.table.hands[self.num - 1], list):
                    label : QtWidgets.QLabel = self.hand_label_list[self.num - 1][-1]
                    label.clear()
                    label.setStyleSheet("border: 2px dashed gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
                    label.setText(f"{self.table.hands[self.num -1][-1].handtotal(self.table.hands[self.num-1][-1].softhand())}")
                    label.update()


                else:
                #self.textboxes[self.num - 1].append(f"{self.table.hands[self.num - 1].cards} : {self.table.hands[self.num - 1].handtotal(self.table.hands[self.num - 1].softhand())} \n")
                    label : QtWidgets.QLabel = self.hand_label_list[self.num - 1]
                    label.clear()
                    label.setStyleSheet("border: 2px dashed gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
                    label.setText(f"{self.table.hands[self.num -1].handtotal(self.table.hands[self.num-1].softhand())}")
                    label.update()


                # if the lasthand was played, then its the dealers turn to play
                if self.lasthand():
                    
                    dealer                = self.table.dealer
                    dealer_hand : Hand    = dealer.hand
                    dealer_updates        = []
                    dealer_downcardsymbol = dealer_hand.card_symbols[1]
                    
                    dealer_updates.append(f"Dealer shows {dealer.hand.cards}, total is {dealer.hand.handtotal(dealer.hand.softhand())}")
                    
                    self.create_dealer_animation(dealer_downcardsymbol, n_cards=1)
                    self.dealer_handlabel.clear()
                    self.dealer_handlabel.setText(f"{dealer_hand.handtotal(dealer_hand.softhand())}")
                    self.dealer_handlabel.update()
                    # while the dealer has less than 17 he must hit a card
                    dealerplay = dealer.hand.dealerturn()

                    while dealerplay:
                        amountofcards : int    = len(dealer_hand.cards)
                        text, card, cardsymbol = self.table.dealer_play()
                        self.create_dealer_animation(cardsymbol, amountofcards)
                        self.dealer_handlabel.clear()
                        self.dealer_handlabel.setText(f"{dealer_hand.handtotal(dealer_hand.softhand())}")
                        self.dealer_handlabel.update()
                        self.dealer_label.animation.start()
                        
                        dealerplay = self.table.dealer.hand.dealerturn()


                    self.final_results()
                
                else:

                    if self.table.hands[self.num].blackjack():
                        self.blackjack()

                    else:
                        label : EasyCardLabels = self.hand_label_list[self.num]
                        
                        label.setStyleSheet("border: 3px solid white; border-radius: 1px ; font : bold 10px ; background: lightgreen")
                        label.update()

                        self.table.addresults(self.table.hands[self.num - 1])
                        hand = self.table.hands[self.num]
                        self.check_available_buttons(hand)


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
                    self.split_num += 1
                    self.nexthand()
                
            else:

                hand = self.table.hands[self.num]

                if hand.handtotal(hand.softhand()) >= 21:
                    
                    text = self.table.checkforbust(hand)
                    self.num += 1
                    self.nexthand()
        

    def hit(self, split=False):

        if self.table:
            
            split = self.splitornot

            if split:
                hand : Hand                  = self.table.hands[self.num][self.split_num]
                card, text, cardsymbol       = self.table.hitcard(hand)
                last_label: EasyCardLabels   = self.card_labels[self.num][self.split_num][-1]
                last_label_pos : QPoint      = last_label.currentpos
                label : EasyCardLabels       = self.hand_label_list[self.num][self.split_num]
                self.createcardanimation_forsplit(cardsymbol, last_label_pos)
                self.card_labels[self.num][self.split_num].append(self.label2)
                self.label2.animation.start()
                label.clear()
                label.setText(f"{hand.handtotal(hand.softhand())}")
                label.update()
                self.check_available_buttons(hand)
                self.checkforbust()
            
            else:
                
                hand : Hand = self.table.hands[self.num]
                card, text, cardsymbol = self.table.hitcard(hand)
                n_cards =  len(hand.cards) - 1
                self.createcardanimation(cardsymbol, n_cards)
                self.card_labels[self.num].append(self.label)
                label : EasyCardLabels = self.hand_label_list[self.num]
                label.clear()
                label.setText(f"{hand.handtotal(hand.softhand())}")
                label.update()
                self.check_available_buttons(hand)
                self.checkforbust()
        

    def stand(self, split=False):

        if self.table:

            split = self.splitornot

            if split:
                
                #self.table.hands[self.num][n].deactivate
                self.split_num += 1
                self.nexthand()

            else:               
                #self.table.hands[self.num].deactivate()
                self.num += 1
                
                self.nexthand()
    
    def doubledown(self, split=False):

        if self.table:
            split = self.splitornot
            if split:
                n                          = self.split_num
                hand                       = self.table.hands[self.num][n]
                last_card : EasyCardLabels = self.card_labels[self.num][n][-1]
                last_card_pos              = last_card.pos()
                card, text, cardsymbol     = self.table.hitcard(hand)
                self.createcardanimation_forsplit(cardsymbol, last_card_pos)
                self.card_labels[self.num][n].append(self.label2)
                self.bank.DoubleDown(hand)
                self.split_num += 1
                self.check_available_buttons(hand)
                self.nexthand()

            else:
                hand : Hand            = self.table.hands[self.num]
                n_cards                = int(len(hand.cards))
                card, text, cardsymbol = self.table.hitcard(hand)
                self.createcardanimation(cardsymbol, n_cards)
                self.card_labels[self.num].append(self.label)
                self.bank.DoubleDown(hand)
                self.num += 1
                self.check_available_buttons(hand)
                self.label.animation.finished.connect(self.nexthand())
    


    def splityourhand(self):

        if self.table:
            
            current_textbox = self.textboxes[self.num]

            # self.splitornot is TRUE when the current hand is ALREADY SPLIT
            if self.splitornot:
                current_hand = self.table.hands[self.num][self.split_num]
                texts, hands = self.table.split(current_hand)
                #current_textbox.append(f"\n".join([text for text in texts]))
                self.table.hands[self.num].pop(self.split_num)
                self.table.hands[self.num].insert(self.split_num, hands[1])
                self.table.hands[self.num].insert(self.split_num, hands[0])
                if self.table.hands[self.num][self.split_num].blackjack():                
                    self.blackjack()
                else:
                    pass


            else:

                self.split_flag = True
                self.splitornot = True
                current_hand    = self.table.hands[self.num]

                self.bank.Split(current_hand)

                texts, hands    = self.table.split(current_hand)
                current_labels  = self.card_labels[self.num]
                new_symbols     = [hands[i].card_symbols[-1] for i in range(2)]
                current_label   = self.hand_label_list[self.num]
                current_label.deleteLater()
                self.splitanimation(current_labels, new_symbols, hands)
                self.table.hands.pop(self.num)
                if self.lasthand():

                    self.table.hands.append(hands)
                else:

                    self.table.hands.insert(self.num, hands)

                if self.table.hands[self.num][0].blackjack():                
                    self.split_full_animgroup.finished.connect(self.blackjack)
                else:
                    label : QtWidgets.QLabel = self.hand_label_list[self.num][self.split_num]
                    label.setStyleSheet("border: 3px solid white; border-radius: 1px ; font : bold 10px ; background: lightgreen")
                    label.update()
                    
            

    def blackjack(self, split=False):

        if self.table:
            split = self.splitornot
            n     = self.split_num

            if split:
                self.split_num += 1
                self.nexthand()

            else:
                self.num += 1
                self.nexthand()
    
    
    def start_round(self):

        self.dealer_handlabel.setParent(self)
        self.dealer_handlabel.show()
        self.num         = 0
        self.table       = Table(hands=self.n_hands.value())
        self.textboxes   = []

        self.bank.BetsChanged.connect(self.update_funds)
        print(self.hand_label_list)

        for x in range(self.n_hands.value()):
            
            self.BetButtonList[x].deleteLater()

            yposition  = 542 + int(self.extra_elevations[x])
            xposition   = 65 + x * 128

            self.n_label = QtWidgets.QLabel()
            self.n_label.setStyleSheet("border: 2px dashed gold; border-radius: 1px ; font : bold 10px ; background: lightgreen" )
            self.n_label.setParent(self)
            self.n_label.resize(QSize(80, 40))
            self.n_label.move(QPoint(xposition, yposition))
            self.hand_label_list.append(self.n_label)
            self.n_label.show()

            hand : Hand = self.table.hands[x]
            
            hand._place_bet((self.bets_list[x] * 100))
            

            txtbox = QtWidgets.QTextEdit()
            txtbox.setReadOnly(True)
            txtbox.append(f"Hand {x+1}: \n")
            self.textboxes.append(txtbox)
            txtbox.setParent(self)
            txtbox.resize(QSize(100, 100))
            txtbox.move(QPoint(xposition, yposition))
            #txtbox.show()

        self.update_funds()       
        
        self.first_cards()
        firstlabel: EasyCardLabels = self.hand_label_list[0]
        firstlabel.setStyleSheet("border: 3px solid white; border-radius: 1px ; font : bold 10px ; background: lightgreen")
        self.check_available_buttons(self.table.hands[0])
        if self.table.hands[0].blackjack():
            self.firstcardanims.finished.connect(self.blackjack())
        else:
            pass



    def CreateCardLabel(self, card_symbol:str):
        self.label : EasyCardLabels = EasyCardLabels()
        self.label.setnewimage(card_symbol)
        
        return self.label
    

    def splitanimation(self, labels:list[EasyCardLabels], newsymbols:list[str], hands):
        xposition = labels[0].x()
        self.split_animgroup        = QParallelAnimationGroup(self)
        self.split_second_animgroup = QSequentialAnimationGroup(self)
        self.split_full_animgroup   = QSequentialAnimationGroup(self)
        self.card_labels_split = [[], []]



        for i, label in enumerate(labels):
            self.label   = label
            self.label2  = EasyCardLabels()
            shifted_xpos = xposition - 30 * (-1)**(i)
            yposition    = 470 + int(self.extra_elevations[self.num -1]) - i * 35
            shifted_ypos = yposition + i * 35
            

            self.label.setshiftpos = QPoint(shifted_xpos, shifted_ypos)
            self.label.setcurrentpos = QPoint(shifted_xpos, shifted_ypos)
            self.label.animation.setStartValue(QPoint(xposition, yposition))
            self.label.animation.setEndValue(QPoint(shifted_xpos, shifted_ypos))
            self.label.animation.setDuration(500)
            self.split_animgroup.addAnimation(self.label.animation)

            self.createcardanimation_forsplit(newsymbols[i], self.label.currentpos, firstanim=True)
            self.card_labels_split[i].append(self.label)
            self.card_labels_split[i].append(self.label2)
            
            self.label.update()
        self.UpdateLabelsForSplit(hands)
        
        self.card_labels.pop(self.num)
        self.card_labels.insert(self.num, self.card_labels_split)

        self.split_full_animgroup.addAnimation(self.split_animgroup)
        self.split_full_animgroup.addAnimation(self.split_second_animgroup)
        self.split_full_animgroup.start()



    def createcardanimation_forsplit(self, card_symbol:str, last_card_position:QPoint, firstanim=False):
        self.label2       = EasyCardLabels()

        self.label2.setnewimage(card_symbol)
        self.label2.setParent(self)
        self.label2.move(QPoint(800, 200))
        
        self.label2.setshiftpos   = last_card_position
        self.label2.setcurrentpos = self.label.shiftedpos
        self.label2.animation.setStartValue(QPoint(800, 200))
        self.label2.animation.setEndValue(self.label2.shiftedpos)
        self.label2.animation.setDuration(500)
        
        self.label2.resize(QSize(60, 72))
        self.label2.show()
        if firstanim:
            self.split_second_animgroup.addAnimation(self.label2.animation)
        else:
            self.label2.animation.start()
    

    def UpdateLabelsForSplit(self, hands:list[Hand]):
        current_label : QtWidgets.QLabel = self.hand_label_list[self.num]
        
        current_x  = current_label.pos().x()
        current_y  = current_label.pos().y()
        new_x1     = current_x - 30
        new_x2     = current_x + 30
        new_xlist  = [new_x1, new_x2]
        new_labels = []
        

        for x in range(2):
            self.new_label = QtWidgets.QLabel()
            self.new_label.resize(QSize(60, 40))
            self.new_label.setParent(self)
            self.new_label.move(QPoint(new_xlist[x], current_y))
            self.new_label.setStyleSheet("border: 2px dashed gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
            self.new_label.setText(f"{hands[x].handtotal(hands[x].softhand())}")
            self.new_label.show()
            new_labels.append(self.new_label)
        
        self.hand_label_list.pop(self.num)
        self.hand_label_list.insert(self.num, new_labels)
        current_label.destroy(True)
        


    def firstanimations(self, first_symbols:list, dealer_symbol:str):
        self.animgroupseq    = QSequentialAnimationGroup()
        self.firstcardanims  = QSequentialAnimationGroup(self)
        self.secondcardanims = QSequentialAnimationGroup(self)
        
        
        

        for x in range(len(first_symbols)):
            
            yposition  = 470 + int(self.extra_elevations[x])
            self.card_labels.append([])

            for i, symbol in enumerate(first_symbols[x]):
                symbol:str
                yposition  -= i * 35
                xposition   = 75 + x * 128 + i*20
                self.label  = EasyCardLabels()
                
                self.label.setParent(self)
                self.label.setnewimage(symbol)
                self.label.move(QPoint(800, 200))
                self.label.animation.setStartValue(QPoint(800, 200))
                self.label.animation.setEndValue(QPoint(xposition, yposition))
                self.label.animation.setDuration(500)
                
                self.label.resize(QSize(60, 72))
                self.label.show()

                self.card_labels[x].append(self.label)
                print(symbol)
                
                if i == 0:
                    self.firstcardanims.addAnimation(self.label.animation)
                else:
                    self.secondcardanims.addAnimation(self.label.animation)
        

        self.deal_label = EasyCardLabels()
        self.deal_label.setParent(self)
        self.deal_label.setnewimage(dealer_symbol)
        self.deal_label.move(QPoint(800, 200))
        self.deal_label.animation.setStartValue(QPoint(800, 200))
        self.deal_label.animation.setEndValue(QPoint(500, 150))
        self.deal_label.animation.setDuration(500)
        self.deal_label.resize(QSize(60, 72))
        self.deal_label.show()

        self.dealer_labels.append(self.deal_label)
        self.animgroupseq.addAnimation(self.firstcardanims)
        self.animgroupseq.addAnimation(self.deal_label.animation)
        self.animgroupseq.addAnimation(self.secondcardanims)
        
        self.animgroupseq.start()




    def createcardanimation(self, card_symbol:str, n_cards:int):
        self.label       = EasyCardLabels()
        hand_number      = self.num
        extra_elevations = self.extra_elevations

        xposition  =  75 + hand_number * 128 + n_cards * 20
        yposition  =  470 + int(extra_elevations[hand_number]) - 35 * n_cards
        

        self.label.setnewimage(card_symbol)
        self.label.setParent(self)
        self.label.move(QPoint(800, 200))
        self.label.animation.setStartValue(QPoint(800, 200))
        self.label.animation.setEndValue(QPoint(xposition, yposition))
        self.label.animation.setDuration(500)
        
        self.label.resize(QSize(60, 72))
        self.label.show()
        self.label.animation.start()
    

    def create_dealer_animation(self, dealer_symbol, n_cards):
        self.dealer_label = EasyCardLabels()
        amountofcards     = n_cards

        xposition = 500 + 20 * amountofcards
        yposition = 150 - 35 * amountofcards


        self.dealer_label.setParent(self)
        self.dealer_label.setnewimage(dealer_symbol)
        
        self.dealer_label.move(QPoint(800, 200))
        self.dealer_label.animation.setStartValue(QPoint(800, 200))
        self.dealer_label.animation.setEndValue(QPoint(xposition, yposition))
        self.dealer_label.animation.setDuration(500)
        self.dealer_label.resize(QSize(60, 72))
        self.dealer_label.show()
        self.dealer_labels.append(self.dealer_label)
        self.dealer_label.animation.start()


    def ClearCurrentTable(self):
        #try:
        self.table.reset()


        # TO DO:
        # fix loop such that all labels are destroyed before the start of a new round.
        # make sure there are no attribute errors
        # fix the amount of for loops 
        for labels in self.card_labels:
            labels : list[EasyCardLabels]
            for x_label in labels:
                
                if isinstance(x_label, list):
                    for y_label in x_label:
                        y_label: EasyCardLabels
                        y_label.setParent(None)
                        y_label.deleteLater()
                else:
                    x_label : EasyCardLabels
                    x_label.setParent(None)
                    x_label.deleteLater()

        for d_label in self.dealer_labels:
            d_label : EasyCardLabels
            d_label.setParent(None)
            d_label.deleteLater()
        for hand_label in self.hand_label_list:
            hand_label : EasyCardLabels
            if isinstance(hand_label, list):
                for s_label in hand_label:
                    s_label : EasyCardLabels
                    
                    s_label.setParent(None)
                    s_label.deleteLater()
            else:
                hand_label.setParent(None)
                hand_label.deleteLater()

                
                
            self.dealer_handlabel.clear()
            self.dealer_handlabel.update()
        

        self.bank.clear_bets()
        print("card labels are:", self.card_labels)
        self.hand_label_list = []
        self.splitornot      = False
        self.split_flag      = False
        self.num             = 0
        self.split_num       = 0
        self.card_labels     = []
        self.popup_off       = True
        self.dealer_labels   = []
        self.dealer_labels   = []
        self.BetsLabelList   = None
        self.bets_list       = []

        self.NextRoundButton.deleteLater()
        self.play_button.setEnabled(True)
        self.UpdatePossibleBets()
        # except AttributeError:
        #     print("There was an attribute error, but we'll ignore it for now")
            
            


def main():

    app = QtWidgets.QApplication(sys.argv)
    ui = BJinterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()