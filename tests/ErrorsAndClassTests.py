from src.baccarat.baccarat_rules_handler import OutComeTypes
from src.baccarat.BaccaratBank import Bank


def DecoratorTest(func):

    def CheckZeroFunds(*args, **kwargs):
        
        arg = args[0]

        if arg <= 0:
            raise ZeroFundsError
        
        else:
            return func(*args, **kwargs)
    
    return CheckZeroFunds



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

    def __init__(self, message="No available funds"):
        self.message = message

    def __str__(self):
        return str("Your account contains no available funds, please make a deposit before placing a bet.")


class ErrorChecker(object):

    
    def _CheckFundsDecorator(func):
        

        def CheckFunds(*args, who):
            
            self : NewBank = args[0]
            if self.funds <= 0:
                raise ZeroFundsError
            elif self.funds < self.BetSize:
                raise InsufficientFundsError(self.Balance)
            else:
                func(*args, who)

        return CheckFunds


class NewBank(Bank):

    def __init__(self, initial_deposit=0):
        self._funds     = initial_deposit
        super().__init__(self._funds)
    
    @ErrorChecker._CheckFundsDecorator
    def PlaceBet(self, who):
        who=who
        try:
            return super().PlaceBet(who=who)
        except InsufficientFundsError(self.Balance) as e:
            print("There was an error")

        
        
        

if __name__ == "__main__":
    bank = NewBank()
    bank.Deposit(100)
    bank.BetSize = 99
    bank.PlaceBet(who=OutComeTypes.BANKER)
    bank.PlaceBet(who=OutComeTypes.BANKER)

   
    
    


