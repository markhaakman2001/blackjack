from typing import Any
from PySide6 import QtWidgets
from PySide6.QtCore import Slot, QSize, QPoint, QSequentialAnimationGroup, QParallelAnimationGroup
import PySide6.QtCore as Core
from CustomUIfiles import EasyCardLabels
from PySide6.QtWidgets import QGraphicsRotation
from PySide6.QtCore import QPropertyAnimation, QPoint
from PySide6.QtCore import QPropertyAnimation, Property
from PySide6.QtGui import QPixmap
from baccarat.baccarat_cards import Card
from blackjack.player import BlackJackPlayer, BlackJackDealer


class BlackJackAnimatedCard(EasyCardLabels):

    def __init__(self, card : Card | None = None):
        super().__init__()
        self.xshift = 30
        if card:
            self.setnewimage(card._get_CardName())

    def TestAnimationold(self, card : Card, y_position = 350):
        cardname = card._get_CardName()
        self.setnewimage(cardname)
        self.animation.setStartValue(QPoint(0, 0))
        self.animation.setEndValue(QPoint(500, y_position))
        self.animation.setDuration(500)
    
    def TestAnimation(self, card : Card, x_end, y_end):
        cardname = card._get_CardName()
        self.setnewimage(cardname)
        self.resize(QSize(60, 72))
        self.animation.setStartValue(QPoint(0, 0))
        self.animation.setEndValue(QPoint(x_end, y_end))
        self.animation.setDuration(500)
    
    def Create_Animation(self, x_end, y_end):
        self.resize(QSize(60, 72))
        self.animation.setStartValue(QPoint(0, 0))
        self.animation.setEndValue(QPoint(x_end, y_end))
        self.animation.setDuration(500)
        
    @property
    def split_shift(self):
        return self._shiftposition_
    
    @split_shift.setter
    def split_shift(self, shift_sign):
        xshift = self.x() + 20 * shift_sign
        yshift = self.y() + 10 * shift_sign
        self._shiftposition_ = QPoint(xshift, yshift)

    def SplitAnimation(self, shift_sign): #shift sign should be (-1) for the left cards and (+1) for the right cards
        x_start = self.x()
        y_start = self.y()
        self.split_shift = shift_sign
        self.animation.setStartValue(QPoint(x_start, y_start))
        self.animation.setEndValue(self.split_shift)
        self.animation.setDuration(500)



class BlackJackAnimations:

    x_positions = lambda x, i : 75 + x * 128 + i * 20
    extra_y_elevations = [-40, -20, 0, 0, 0, -20, -40]
    y_positions = lambda x, i : 470  + x - i*20
    

    @classmethod
    def first_deal_animation(cls, player : BlackJackPlayer, dealer : BlackJackDealer):
        y_start = 470
        animated_cards = []
        anim_group = QSequentialAnimationGroup()
        cards_per_hand = {x : [] for x in range(len(player.hands))}
        for x in range(2):
            yposition = y_start + cls.extra_y_elevations[x]
            for x_hand, hand in enumerate(player.hands):
                xpos = cls.x_positions(x_hand, x)
                ypos = y_start + cls.extra_y_elevations[x_hand] - x *20
                card = hand.cards[x]
                animated_card = BlackJackAnimatedCard()
                animated_card.TestAnimation(card, xpos, ypos)
                anim_group.addAnimation(animated_card.animation)
                animated_cards.append(animated_card)
                cards_per_hand[x_hand].append(animated_card)

            if x == 0:
                dealer_upcard = dealer.hand.cards[0]
                dealer_anim_card = BlackJackAnimatedCard()
                dealer_anim_card.TestAnimation(dealer_upcard, 500, 150)
                anim_group.addAnimation(dealer_anim_card.animation)
                animated_cards.append(dealer_anim_card)
                  
        return animated_cards, anim_group, cards_per_hand
    
    @classmethod
    def hit_card_animation(cls, card : Card, xhand, icard):
        animated_card = BlackJackAnimatedCard(card)
        xpos = cls.x_positions(xhand, icard)
        ypos = cls.y_positions(cls.extra_y_elevations[xhand], icard)
        animated_card.Create_Animation(xpos, ypos)
        return animated_card
    
    @classmethod
    def dealer_card_animations(cls, dealer : BlackJackDealer) -> tuple[list[BlackJackAnimatedCard], QSequentialAnimationGroup]:
        animated_cards = []
        anim_group     = QSequentialAnimationGroup()
        for i, card in enumerate(dealer.hand.cards[1:]):
            animated_card = BlackJackAnimatedCard(card)
            xpos = 520 + i * 20
            ypos = 130 - i * 20
            animated_card.Create_Animation(xpos, ypos)
            animated_cards.append(animated_card)
            anim_group.addAnimation(animated_card.animation)
        return animated_cards, anim_group

    @classmethod
    def split_animation(cls, cards : list[BlackJackAnimatedCard], new_cards : list[Card], hand_nr_origin):
        anim_group = QParallelAnimationGroup()
        new_animated_cards = []

        for i, card in enumerate(cards):
            card.SplitAnimation(((-1) * (-1)**i))
            anim_group.addAnimation(card.animation)

            new_card   = BlackJackAnimatedCard(new_cards[i])
            new_card_x = card.split_shift.x()
            new_card_y = card.split_shift.y() - 20
            
            new_card.split_shift = (-1) * (-1)**i
            new_card.Create_Animation(new_card_x, new_card_y)
            anim_group.addAnimation(new_card.animation)
            new_animated_cards.append(new_card)
            
        return cards, anim_group, new_animated_cards

    




    