import numpy as np
import random
from math import trunc



class MinesGame:

    def __init__(self):
        self.matrix    = np.zeros((5, 5))
        self.n_correct = 0
    
    def CreateMines(self, n_mines) -> None:
        self.n_correct = 0
        self.matrix    = np.zeros((5, 5))
        self.mines     = random.sample(range(25), n_mines)
        self._nMines_  = n_mines
        for mine in self.mines:
            i_mine   = (mine % 5)
            row_mine = trunc(mine / 5)
            self.matrix[row_mine, i_mine] = 1


    def CheckMine(self, n_mine) -> bool:
        row  = trunc(n_mine / 5)
        i    = (n_mine % 5)
        mine = self.matrix[row, i]
        return True if mine else False

    def OddsCalculator(self):
        n_m       = self._nMines_
        total_odd = 1
        for x in range(self.n_correct):
            nextodd = (25 - n_m - x) / (25 - x)
            total_odd = total_odd * nextodd
            print(total_odd)
        
        return total_odd

    @property
    def _nMines_(self):
        return self._nmines
    
    @_nMines_.setter
    def _nMines_(self, nmines : int):
        self._nmines = nmines




def main():
    game = MinesGame()
    game.CreateMines(1)


if __name__ == "__main__":
    main()