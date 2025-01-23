class BalanceError(Exception):
    """An error occured while trying to place a bet.
    """    
    pass


class InsufficientFundsError(BalanceError):
    """Exception raised when the available funds are not sufficient for the current betsize
    """    

    def __init__(self, max_funds: int, message="Insufficient funds to perform action"):
        self.message   = message
        self.max_funds = str(f"Maximum possible bet is {max_funds}")
        super().__init__(self.message)
    
    def __str__(self):        
        return str(f".\n".join([self.message, self.max_funds]))

class ZeroFundsError(BalanceError):

    def __init__(self, message="Your account contains no available funds."):
        self.message = message
        self.message2 = "Please make a deposit before placing a bet."
        super().__init__(self.message)

    def __str__(self):
        return str(f".\n".join([self.message, self.message2]))


class BettingError(Exception):
    pass


class ZeroBetsPlacedError(BettingError):

    def __init__(self, message="No active bets.", message2="Place a bet before starting."):
        self.message  = message
        self.message2 = message2
        super().__init__(self.message)
    
    def __str__(self):
        return str(f"\n".join([self.message, self.message2]))

class InvalidBetError(BettingError):

    def __init__(self,  NrOfPossibleBets, NrOfValidBets, message1="Invalid bet detected"):
        self.message  = message1
        self.message2 = f"Number of active hands: {NrOfPossibleBets}"
        self.message3 = f"Number of valid bets placed: {NrOfValidBets}"
        super().__init__(self.message)
    
    def __str__(self):
        return str(f".\n".join([self.message, self.message2, self.message3]))



class ErrorChecker(object):

    
    def _CheckFundsDecorator(func):
        """Check if there are enough available funds to place the current bet.

        If the current BetSize is greater than the total remaining funds, raise InsifficientFundsError.

        If there are no available funds, raise ZeroFundsError.

        Args:
            func (function): function used to place a bet.
        """         

        
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
        """Check if any bets have been placed before starting a round of BlackJack or Baccarat.
        If no bets are placed, raise a ZeroBetsPlacedError.

        Args:
            func (function): Function that starts the round.
        """        

        def _CheckBets(*args):

            from src.baccarat.BaccaratBank import Bank

            # try statement is used to differentiate between BlackJack and Baccarat
            # When the decorator is used for baccarat two args should be passes
            # For Blackjack only one arg is passed, which is the UI
            #
            # TO DO:
            # Fix the BlackJack interface such that the try statement can be removed.
            try:
                table       = args[0]       
                self : Bank = args[1]
                TotalBets   = self.TotalBet

            except IndexError:
                
                from src.blackjack.gui import BJinterface as BJ

                ui   : BJ     = args[0]
                self : Bank   = ui.bank
                TotalBets     = self.TotalBet
                BetList       = ui.bets_list
                NrOfBets      = len(BetList)
                NrInvalidBets = BetList.count(0)
                if NrInvalidBets:
                    raise BettingError(InvalidBetError(NrOfBets, (NrOfBets - NrInvalidBets)))

            
            if self.TotalBet == 0:
                raise BettingError(ZeroBetsPlacedError())
            else:
                func(*args)
        
        return _CheckBets
    

    def _CheckSlotBalance(func):

        def _CheckSlotBet(*args):
            
            from src.SlotMachine.slot_generator import BankAccount

            self : BankAccount = args[0]
            CurrentBetSize     = self._BetSize_
            CurrentBalance     = self._FundsCredits_

            if CurrentBalance <= 0:
                raise BalanceError(ZeroFundsError())
            
            elif CurrentBetSize > CurrentBalance:
                raise BalanceError(InsufficientFundsError(CurrentBalance))
            
            else:
                func(*args)
        
        return _CheckSlotBet



def main():
    pass

if __name__ == "__main__":
    main()