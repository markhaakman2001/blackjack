from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QSize, QPoint, QSequentialAnimationGroup, QParallelAnimationGroup, QPropertyAnimation
import PySide6.QtCore as Core
from src.blackjack.gui_table import Table
from src.blackjack.gui_shoehand import Hand
from src.extrafiles.labels import EasyCardLabels
from src.extrafiles.backgroundwidget import BackGroundWidget
import sys
import time


class BJinterface(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        

        self.central_widget =  BackGroundWidget()
        #self.setCentralWidget(self.central_widget)
        self.central_widget.setParent(self)
        
        self.resize(1000, 700)
        self.central_widget.resize(QSize(1000, 700))
        
        
        
        self.deal_label= QtWidgets.QLabel(text="Dealer:")
        

        self.hand_lbl = QtWidgets.QLabel(text="Your hands:")
        

        self.hand_info = QtWidgets.QTextEdit()
        self.hand_info.setReadOnly(True)
        self.hand_info.size = QSize(300, 100)
        self.hand_info.resize(self.hand_info.size)
        self.hand_info.move(QPoint(0, 100))

        self.display_txt = QtWidgets.QTextEdit()
        self.display_txt.setReadOnly(True)
        self.display_txt.size = QSize(250, 115)
        self.display_txt.resize(self.display_txt.size)
        self.display_txt.move(QPoint(0, 635))

        self.dealer_handlabel = QtWidgets.QLabel()
        self.dealer_handlabel.resize(QSize(80, 40))
        self.dealer_handlabel.move(QPoint(490, 230))
        self.dealer_handlabel.setStyleSheet("border: 2px solid gold; border-radius: 1px ; font : bold 10px ; background: lightgreen")
        


        self.confirm_btn   = QtWidgets.QPushButton(text="Confirm Bet")
        self.hit_button    = QtWidgets.QPushButton(text="hit")
        self.stand_button  = QtWidgets.QPushButton(text="Stand")
        self.double_button = QtWidgets.QPushButton(text="Double")
        self.split_button  = QtWidgets.QPushButton(text="Split")
        self.n_hands       = QtWidgets.QSpinBox()
        self.play_button   = QtWidgets.QPushButton(text="Play")


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
        
        # move to correct position
        self.double_button.move(QPoint(0, 600))
        self.hit_button.move(QPoint(250, 600))
        self.stand_button.move(QPoint(500, 600))
        self.split_button.move(QPoint(750, 600))
        self.n_hands.move(QPoint(250, 635))
        self.play_button.move(QPoint(500, 635))


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


        self.table       = None     # table is initiated later
        self.splitornot  = False    # this is True if the current hand is a splithand
        self.split_flag  = False    # this is True if the current hand is split more than once
        self.num         = 0        # Keeps track of the index of the current main hand being played
        self.split_num   = 0        # Keeps track of the index of the current split hand being played
        self.card_labels = []       # This list holds all the card labels of the cards that have been revealed.
        self.popup_off   = True     # If there already is a popup this should be False
        

    
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
            first_results, dealerupcard, first_symbols, dealer_symbols = self.table.print_first_results()
            
            for x in range(len(self.table.hands)):
                hand : Hand            = self.table.hands[x]
                label : EasyCardLabels = self.hand_label_list[x]
                label.clear()
                label.setText(f"{hand.handtotal(hand.softhand())}")
                label.update()

            self.firstanimations(first_symbols, dealer_symbol=dealer_symbols[0])
            self.update_player(text = "\n".join([first_results[x] for x in range(len(first_results))]))
            print(first_results)
            self.update_dealer(dealerupcard)


    @Slot()
    def final_results(self):

        if self.table:


            results = []
            
            for i, hand in enumerate(self.table.hands):
                
                if isinstance(hand, list):
                    labels : QtWidgets.QLabel = self.hand_label_list[i]
                    for hand, label in zip(hand, labels):
                        label.clear()
                        label.setText(f"{self.table.winlose(hand)}")
                        label.update()

                else:
                    results.append(self.table.winlose(hand))
                    print("YO")
                    label : QtWidgets.QLabel = self.hand_label_list[i]
                    label.clear()
                    label.setText(f"{self.table.winlose(hand)}")
                    label.update()
  
                
    
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
                    self.update_dealer(dealer_updates[0])
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

                card, text, cardsymbol       = self.table.hitcard(self.table.hands[self.num][self.split_num])
                last_label: EasyCardLabels   = self.card_labels[self.num][self.split_num][-1]
                last_label_pos : QPoint      = last_label.currentpos
                self.createcardanimation_forsplit(cardsymbol, last_label_pos)
                self.label2.animation.start()
                self.update_txt(f"You hit, your new card is {card}.")
                self.update_player(text)
                self.checkforbust()
                      
            else:

                hand : Hand = self.table.hands[self.num]
                card, text, cardsymbol = self.table.hitcard(hand)
                n_cards =  len(hand.cards) - 1
                self.createcardanimation(cardsymbol, n_cards)
                label : EasyCardLabels = self.hand_label_list[self.num]
                label.clear()
                label.setText(f"{hand.handtotal(hand.softhand())}")
                label.update()
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
                n                      = self.split_num
                hand                   = self.table.hands[self.num][n]
                card, text, cardsymbol = self.table.hitcard(hand)

                self.update_txt(f"You doubled, your new card is {card}.")
                self.update_player(text)
                self.split_num += 1

                self.nexthand()

            else:
                hand : Hand            = self.table.hands[self.num]
                n_cards                = int(len(hand.cards))
                card, text, cardsymbol = self.table.hitcard(hand)
                self.createcardanimation(cardsymbol, n_cards)
                self.update_txt(f"You doubled, your new card is {card}.")
                self.update_player(text)
                self.num += 1

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
                    self.update_txt("Splithand 1, pick an action")


            else:

                self.split_flag = True
                self.splitornot = True
                current_hand    = self.table.hands[self.num]
                texts, hands    = self.table.split(current_hand)
                current_labels  = self.card_labels[self.num]
                new_symbols     = [hands[i].card_symbols[-1] for i in range(2)]
                self.splitanimation(current_labels, new_symbols, hands)
                current_textbox.clear()
                current_textbox.append(f"\n".join([text for text  in texts]))
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
                    self.update_txt("Splithand 1, pick an action")
            

    def blackjack(self, split=False):

        if self.table:
            split = self.splitornot
            n     = self.split_num
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
        
        self.dealer_handlabel.setParent(self)
        self.dealer_handlabel.show()
        self.num       = 0
        self.table     = Table(hands=self.n_hands.value())
        self.textboxes = []

        for x in range(self.n_hands.value()):

            yposition  = 562 + int(self.extra_elevations[x])
            xposition   = 65 + x * 128

            n_label = QtWidgets.QLabel()
            n_label.setStyleSheet("border: 2px dashed gold; border-radius: 1px ; font : bold 10px ; background: lightgreen" )
            n_label.setParent(self)
            n_label.resize(QSize(80, 40))
            n_label.move(QPoint(xposition, yposition))
            self.hand_label_list.append(n_label)
            n_label.show()



            txtbox = QtWidgets.QTextEdit()
            txtbox.setReadOnly(True)
            txtbox.append(f"Hand {x+1}: \n")
            self.textboxes.append(txtbox)
            txtbox.setParent(self)
            txtbox.resize(QSize(100, 100))
            txtbox.move(QPoint(xposition, yposition))
            #txtbox.show()
            
        self.update_txt("Round started, good luck!")
        self.first_cards()
        firstlabel: EasyCardLabels = self.hand_label_list[0]
        firstlabel.setStyleSheet("border: 3px solid white; border-radius: 1px ; font : bold 10px ; background: lightgreen")
        if self.table.hands[0].blackjack():
            self.firstcardanims.finished.connect(self.blackjack())
        else:
            self.update_txt("Hand 1, pick an action")



    def CreateCardLabel(self, card_symbol:str):
        self.label : EasyCardLabels = EasyCardLabels()
        self.label.setnewimage(card_symbol)
        
        return self.label
    

    def splitanimation(self, labels:list[EasyCardLabels], newsymbols:list[str], hands):
        xposition = labels[0].x()
        self.split_animgroup        = QParallelAnimationGroup(self)
        self.split_second_animgroup = QSequentialAnimationGroup(self)
        self.split_full_animgroup   = QSequentialAnimationGroup(self)
        card_labels = [[], []]

        for i, label in enumerate(labels):
            self.label   = label
            self.label2  = EasyCardLabels()
            shifted_xpos = xposition - 30 * (-1)**(i)
            yposition    = 490 + int(self.extra_elevations[self.num -1]) - i * 35
            shifted_ypos = yposition + i * 35
            

            self.label.setshiftpos = QPoint(shifted_xpos, shifted_ypos)
            self.label.setcurrentpos = QPoint(shifted_xpos, shifted_ypos)
            self.label.animation.setStartValue(QPoint(xposition, yposition))
            self.label.animation.setEndValue(QPoint(shifted_xpos, shifted_ypos))
            self.label.animation.setDuration(500)
            self.split_animgroup.addAnimation(self.label.animation)

            self.createcardanimation_forsplit(newsymbols[i], self.label.currentpos, firstanim=True)
            card_labels[i].append(self.label)
            card_labels[i].append(self.label2)
            
            self.label.update()
        self.UpdateLabelsForSplit(hands)
        
        self.card_labels.pop(self.num)
        self.card_labels.insert(self.num, card_labels)

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
        current_label.destroy()
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
        


    def firstanimations(self, first_symbols:list, dealer_symbol:str):
        self.animgroupseq    = QSequentialAnimationGroup()
        self.firstcardanims  = QSequentialAnimationGroup(self)
        self.secondcardanims = QSequentialAnimationGroup(self)
        
        
        

        for x in range(len(first_symbols)):
            
            yposition  = 490 + int(self.extra_elevations[x])
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

            
        self.animgroupseq.addAnimation(self.firstcardanims)
        self.animgroupseq.addAnimation(self.deal_label.animation)
        self.animgroupseq.addAnimation(self.secondcardanims)
        
        self.animgroupseq.start()




    def createcardanimation(self, card_symbol:str, n_cards:int):
        self.label       = EasyCardLabels()
        hand_number      = self.num
        extra_elevations = self.extra_elevations

        xposition  =  75 + hand_number * 128 + n_cards * 20
        yposition  =  490 + int(extra_elevations[hand_number]) - 35 * n_cards
        

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
        self.dealer_label.animation.start()


def main():

    app = QtWidgets.QApplication(sys.argv)
    ui = BJinterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()