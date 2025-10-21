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

    def __init__(self):
        super().__init__()
    

    def TestAnimationold(self, card : Card, y_position = 350):
        cardname = card._get_CardName()
        self.setnewimage(cardname)
        self.animation.setStartValue(QPoint(0, 0))
        self.animation.setEndValue(QPoint(500, y_position))
        self.animation.setDuration(500)
    
    def TestAnimation(self, card : Card, x_end, y_end):
        cardname = card._get_CardName()
        self.setnewimage(cardname)
        self.animation.setStartValue(QPoint(0, 0))
        self.animation.setEndValue(QPoint(x_end, y_end))
        self.animation.setDuration(500)


class BlackJackAnimations:

    def __init__(self):
        self.x_positions = lambda x, i : 75 + x * 128 + i * 20
        self.extra_y_elevations = [-40, -20, 0, 0, 0, -20, -40]

    def first_deal_animation(self, player : BlackJackPlayer, dealer : BlackJackDealer):
        y_start = 470
        animated_cards = []
        anim_group = QSequentialAnimationGroup()
        for x_hand, hand in enumerate(player.hands):
            yposition = y_start + self.extra_y_elevations[x_hand]

            for i_card, card in enumerate(hand.cards):
                yposition -= i_card * 35
                xposition = self.x_positions(x_hand, i_card)
                animated_card = BlackJackAnimatedCard()
                animated_card.TestAnimation(card, xposition, yposition)
                animated_cards.append(animated_card)
                anim_group.addAnimation(animated_card.animation)
        return animated_cards, anim_group




    