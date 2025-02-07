from src.extrafiles.gametrackingtools import gt

class ActiveGameError(Exception):

    def __init__(self, current_game : gt):
        self.message1 = "Cannot perform action while there is still an active game"
        self.message2 = f"Please finish and close game : {current_game} before starting a new game"
        self.game     = current_game
        super().__init__(self.message1)
    
    def __str__(self):
        return str(f".\n".join([self.message1, self.message2]))


class MainUIErrorChecker(object):

    def _CheckForActiveGames_(func):

        def _CheckGames_(*args, **kwargs):
            
            from src.MainUI.CasinoUI import CasinoUI
            from src.extrafiles.gametrackingtools import GameState as gs

            self : CasinoUI = args[0]
            blackjack       = self.BlackJack
            baccarat        = self.Baccarat
            slotmachine     = self.SlotMachine
            if blackjack._GameState_ == gs.ACTIVE:
                raise ActiveGameError(gt.BLACKJACK)
            elif baccarat._GameState_ == gs.ACTIVE:
                raise ActiveGameError(gt.BACCARAT)
            elif slotmachine._GameState_ == gs.ACTIVE:
                raise ActiveGameError(gt.SLOTMACHINE)
            else:
                func(*args)

        return _CheckGames_
    
    def _CheckActiveGamesnew(func):

        def _CheckGame(*args, **kwargs):
            from src.extrafiles.gametrackingtools import GameState as gs
            from src.MainUI.CasinoUI import CasinoUI
            self : CasinoUI     = args[0]
            gametype : gt       = args[1]
            for game, type in self.games_dict.items():
                state : gs = game._GameState_
                if state == gs.ACTIVE and gametype != type:
                    raise ActiveGameError(type)
        return _CheckGame
                    