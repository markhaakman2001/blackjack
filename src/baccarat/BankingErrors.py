class BalanceError(Exception):
    """An error occured while trying to place a bet.
    """    
    pass


class InsufficientFundsError(Exception):
    """Exception raised when the available funds are not sufficient for the current betsize
    """    

    def __init__(self, max_funds: int, message="Insufficient funds to perform action"):
        self.message   = message
        self.max_funds = str(f"Maximum possible bet is {max_funds}")
        super().__init__(self.message)
    
    def __str__(self):        
        return str(f".\n".join([self.message, self.max_funds]))

class ZeroFundsError(Exception):

    def __init__(self, message="Your account contains no available funds."):
        self.message = message
        self.message2 = "Please make a deposit before placing a bet."
        super().__init__(self.message)

    def __str__(self):
        return str(f".\n".join([self.message, self.message2]))


class ZeroBetsPlacedError(Exception):

    def __init__(self, message="No active bets.", message2="Place a bet before starting."):
        self.message  = message
        self.message2 = message2
        super().__init__(self.message)
    
    def __str__(self):
        return str(f"\n".join([self.message, self.message2]))



class ErrorChecker(object):

    
    def _CheckFundsDecorator(func):

        
        def CheckFunds(*args, **kwargs):

            from src.baccarat.BaccaratBank import Bank

            print("Starting FundsCheck")
            print(f"{[arg for arg in args]=}")
            self : Bank = args[0]

            if self.funds <= 0:
                raise BalanceError(ZeroFundsError())
            elif self.funds < self.BetSize:
                raise BalanceError(InsufficientFundsError(self.Balance))
            else:
                func(*args, **kwargs)
                print("FundsCheck complete")

        return CheckFunds


    def _CheckForPlacedBets(func):

        def _CheckBets(*args):

            from src.baccarat.BaccaratBank import Bank

            table       = args[0]
            self : Bank = args[1]
            TotalBets   = self.TotalBet
            if self.TotalBet == 0:
                raise ZeroBetsPlacedError
            else:
                func(*args)
        
        return _CheckBets



def main():
    pass

if __name__ == "__main__":
    main()