from src.extrafiles.gametrackingtools import GameState as gs


class MinesError(Exception):
    pass

class ActiveGamesError(MinesError):
    
    def __init__(self, message = "Please finish the current game first."):
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return str(self.message)

class NoActiveGamesError(MinesError):

    def __init__(self, message = "Please start a new game first."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return str(self.message)

class RevealedMinesError(MinesError):

    def __init__(self):
        self.message1 = "This square has already been revealed"
        self.message2 = "Please pick another square to reveal"
        super().__init__(self.message1)
    
    def __str__(self):
        return str(f".\n".join([self.message1, self.message2]))

class MinesErrorChecker(object):
    

    def _CheckActiveGames(func):

        def _CheckMinesGames(*args, **kwargs):
            from src.mines.minesUI import MinesUI
            
            self : MinesUI = args[0]
            checkfor : gs  = args[1]
            state : gs     = self._GameState_
            if state == checkfor:
                if checkfor == gs.ACTIVE:
                    raise MinesError(ActiveGamesError())
                else:
                    raise MinesError(NoActiveGamesError())
            else:
                func(*args, **kwargs)
            
        return _CheckMinesGames
    
    def _CheckRevealedMines(func):

        def RevealedOrNot(*args, **kwargs):
            from src.mines.minesUI import MinesButton

            btn : MinesButton = args[0]
            checked : bool    = btn.MineChecked

            if checked:
                raise MinesError(RevealedMinesError())
            else:
                func(*args, **kwargs)
        
        return RevealedOrNot



