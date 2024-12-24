class BlackJackBankErrors(Exception):
    pass

class InsufficientFundsError(Exception):

    def __init__(self, max_funds):
        self.message1 = "Insufficient funds to perform action"
        self.message2 = f"Maximum possible bet is: ${max_funds}"
        super().__init__(self.message1)
    
    def __str__(self):
        return str(f"\n".join([self.message1, self.message2]))


class BankingErrors:


    def _CheckInsufficientFunds(func):
        pass

