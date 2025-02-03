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

class BetButtonType(Enum):

    PLACEBET  = 0
    REMOVEBET = 1

class BlackJackBetButton(QPushButton):

    xButtonSignal        = Signal(WhichButton, name="xButton")
    xButtonRemovalSignal = Signal(WhichButton, name="xButtonRemoval")

    def __init__(self):
        super().__init__()
        self._ButtonType = BetButtonType.PLACEBET
        self.clicked.connect(self.Emit_x_Signal)

    @Slot()
    def Emit_x_Signal(self) -> None:
        
        if self._ButtonType == BetButtonType.PLACEBET:
            x = self._x_button
            y = WhichButton(x)
            self.xButtonSignal.emit(y)
        
        elif self._ButtonType == BetButtonType.REMOVEBET:
            x = self._x_button
            y = WhichButton(x)
            self.xButtonRemovalSignal.emit(y)


    @property
    def _x_button(self) -> int:
        return self._x_button_
    
    @_x_button.setter
    def _x_button(self, x : int) -> None:
        self._x_button_ = x
    
    @property
    def _ButtonType(self) -> BetButtonType:
        return self._ButtonType_
    
    @_ButtonType.setter
    def _ButtonType(self, type : BetButtonType) -> None:
        self._ButtonType_ = type