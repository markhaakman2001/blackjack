import numpy as np
import random
from math import trunc



class MinesGame:

    def __init__(self):
        self.matrix = np.zeros((5, 5))

    
    def CreateMines(self, n_mines) -> None:
        self.matrix = np.zeros((5, 5))
        self.mines = random.sample(range(25), n_mines)
        for mine in self.mines:
            i_mine   = (mine % 5)
            row_mine = trunc(mine / 5)
            self.matrix[row_mine, i_mine] = 1
        


    def CheckMine(self, n_mine) -> bool:
        row  = trunc(n_mine / 5)
        i    = (n_mine % 5)
        mine = self.matrix[row, i]
        return True if mine else False




def main():
    game = MinesGame()
    game.CreateMines(1)


if __name__ == "__main__":
    main()