import src.UnifiedBanking.BalanceTrackingTools as bt

class MainBank:

    def __init__(self):
        self._FundsCredits : int = 0
    
    def DepositMoney(self, AmountEuros : float):
        AmountCredits         = int(AmountEuros * 100)
        self._BalanceCredits_ = AmountCredits
    
    @property
    def _BalanceEuros_(self) -> float:
        """Get the balance in euros. (1 euro = 100 credits)

        Returns:
            float: Current account balance in EUROS
        """       
        _FundsEuros_ = (self._BalanceCredits_ / 100)
        return _FundsEuros_
    
    @property
    def _BalanceCredits_(self) -> int:
        """Get account balance in CREDITS (100 credits = 1 euro)

        Returns:
            _type_: _description_
        """        
        return self._FundsCredits
    
    @_BalanceCredits_.setter
    def _BalanceCredits_(self, AmountCredits : int) -> None:
        """Change the balance by a certain amount

        Args:
            AmountCredits (int): How much credits should be added to the balance
        """             
        OldFunds = self._FundsCredits
        NewFunds = OldFunds + AmountCredits
        self._FundsCredits = NewFunds
    
    def UpdateBankAccounts(self, bjbank, bacbank, slotbank, amount, origin):
        bj_amount              = (amount / 100)
        bac_amount             = (amount / 100)
        slot_amount            = amount
        update_amounts         = [bac_amount, bj_amount, slot_amount]
        update_amounts[origin] = 0

        bt.UpdateBalanceAfterChanges(bjbank, bacbank, slotbank, update_amounts)
