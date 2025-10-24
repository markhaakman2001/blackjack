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


class BlackJackAnimations:

    x_positions = lambda x, i : 75 + x * 128 + i * 20
    extra_y_elevations = [-40, -20, 0, 0, 0, -20, -40]
    y_positions = lambda x, i : 470  + x - i*20
    

    @classmethod
    def first_deal_animation(cls, player : BlackJackPlayer, dealer : BlackJackDealer):
        y_start = 470
        animated_cards = []
        anim_group = QSequentialAnimationGroup()
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

            if x == 0:
                dealer_upcard = dealer.hand.cards[0]
                dealer_anim_card = BlackJackAnimatedCard()
                dealer_anim_card.TestAnimation(dealer_upcard, 500, 150)
                anim_group.addAnimation(dealer_anim_card.animation)
                animated_cards.append(dealer_anim_card)
                  
        return animated_cards, anim_group
    
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
        print(dealer.hand.cards)
        for i, card in enumerate(dealer.hand.cards):
            animated_card = BlackJackAnimatedCard(card)
            xpos = 520 + i * 20
            ypos = 130 - i * 20
            animated_card.Create_Animation(xpos, ypos)
            animated_cards.append(animated_card)
            anim_group.addAnimation(animated_card.animation)
        return animated_cards, anim_group


    




    