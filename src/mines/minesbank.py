from PySide6.QtCore import QObject, Signal, Slot
from src.UnifiedBanking.UnifiedBank import MainBank


class MinesBank(QObject):

    BalanceChanged = Signal(name="BalanceChanged")

    def __init__(self, main_bank : MainBank = MainBank(100)):
        super().__init__()
        self.MainBank = main_bank
        self._funds   = self.MainBank._BalanceCredits_
        self._BetSize = 100
    
    def PlaceBet(self):
        bet_credits = self._BetSize_
        self._funds_credits_ = (-1) * bet_credits
        self._CurrentBet_    = bet_credits

    @property
    def _CurrentBet_(self) -> int:
        return self._currentbet

    @_CurrentBet_.setter
    def _CurrentBet_(self, betsize):
        self._currentbet = betsize

    @property
    def _funds_credits_(self) -> int:
        self._funds = self.MainBank._BalanceCredits_
        return self._funds
    
    @_funds_credits_.setter
    def _funds_credits_(self, amount_credits):
        self.MainBank._BalanceCredits_ = amount_credits
        self.BalanceChanged.emit()
    
    @property
    def funds_euros(self) -> float:
        self._funds_euros = (self._funds_credits_ / 100)
        return self._funds_euros

    @property
    def _BetSize_(self) -> int:
        return self._BetSize
    
    @_BetSize_.setter
    def _BetSize_(self, amount_credits):
        self._BetSize = amount_credits


