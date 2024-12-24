from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Slot, Signal
from enum import Enum

class WhichButton(Enum):

    FIRST   = 0
    SECOND  = 1
    THIRD   = 2
    FOURTH  = 3
    FIFTH   = 4
    SIXTH   = 5
    SEVENTH = 6


class BlackJackBetButton(QPushButton):

    xButtonSignal = Signal(WhichButton, name="xButton")

    def __init__(self):
        super().__init__()
        self.clicked.connect(self.Emit_x_Signal)

    @Slot()
    def Emit_x_Signal(self):
        x = self._x_button
        y = WhichButton(x)
        self.xButtonSignal.emit(y)

    @property
    def _x_button(self) -> int:
        return self._x_button_
    
    @_x_button.setter
    def _x_button(self, x : int):
        self._x_button_ = x