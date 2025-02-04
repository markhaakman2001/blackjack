class ActiveGameError(Exception):

    def __init__(self):
        self.message1 = "Cannot perform action while there is still an active game"
        self.message2 = "Please close all open games before starting a new one"
        super().__init__(self.message1)
    
    def __str__(self):
        return str(f".\n".join([self.message1, self.message2]))


class MainUIErrorChecker(object):

    def _CheckForActiveGames_(func):
        from src.MainUI.CasinoUI import CasinoUI
        from src.extrafiles.gamestate import GameState as gs
        
        def _CheckGames_(*args):
            self : CasinoUI = args[0]
            blackjack       = self.BlackJack
            baccarat        = self.Baccarat
            if blackjack._GameState_ == gs.ACTIVE:
                raise ActiveGameError()
            elif baccarat._GameState_ == gs.ACTIVE:
                raise ActiveGameError()
            else:
                func(*args)

        return _CheckGames_