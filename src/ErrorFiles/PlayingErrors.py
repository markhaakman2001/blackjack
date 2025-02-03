class PlayingError(Exception):
    """General Exception for errors while playing
    """    

    pass

class ActiveBetsError(PlayingError):

    def __init__(self, message="Cannot change number of hands while bets are placed."):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        message2 = "Please remove all bets before changing the number of hands."
        return str(f"\n".join([self.message, message2]))


class BlackJackErrorChecker(object):

    def _CheckForPlacedBets_(func):
        """Used to check if there are any bets placed before changing the number of hands in BlackJack.
        

        Args:
            func (function): function
        """        
        def CheckBets(*args):

            from src.blackjack.gui          import BJinterface
            from src.blackjack.gui_shoehand import BlackJackBank


            self : BJinterface = args[0]
            bank : BlackJackBank        = self.bank

            if bank.TotalBet > 0:
                raise  PlayingError(ActiveBetsError())
            else:
                func(*args)
        
        return CheckBets
