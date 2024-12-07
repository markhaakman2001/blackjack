import numpy as np
from math import *
import random


class Reels:

    def __init__(self):

        # What the slot machine has to display, instead of integers
        self.possible_values = { 
            1 : "10",
            2 : "J",
            3 : "Q",
            4 : "K",
            5 : "A",
            6 : "2",
            7 : "3",
            8 : "4",
            9 : "5",
        }

        self.inverse_possible_values = {v: k for k, v in self.possible_values.items()}

        slots = [0]*5
        self.reel_values = np.array(slots)
        self.reel_disp = np.array(slots)
    

    def generate_reel(self):

        new_reel = []

        # choose a random digit for every slot in the reel
        for x in range(5):
            x = random.randint(1, 9)
            new_reel.append(x)

        # array values
        self.reel_values = np.array(new_reel)
        
        self.reel_disp = np.array([str(self.possible_values.get(x)) for x in self.reel_values])
    
    def reset(self):
        self.__init__()
        

class PlayingField:

    def __init__(self):

        self.reels = []
        for x in range(6):
            r = Reels()
            self.reels.append(r)
        self.full_field = np.zeros((5, 6))
        self.full_field_disp = np.empty((5, 6), dtype='<U5')
    
    def generate_field(self):
        
        for i, reel in enumerate(self.reels):
            reel.generate_reel()
            self.full_field[:, i] = reel.reel_values
            self.full_field_disp[:, i] = reel.reel_disp

        
    def printaline(self, row_index):
        zigzagline = []
        straightline = self.full_field[row_index]


        for x in range(1, 7):
            if x % 2 == 0:
                if row_index == 4:
                    zigzagline.append(int(self.full_field[row_index - 1, x - 1]))
                else:
                    zigzagline.append(int(self.full_field[row_index + 1, x - 1]))
            else:
                zigzagline.append(int(self.full_field[row_index][x-1]))
        
        return zigzagline, straightline
    

    def checkwinnings(self):
        zigzags = []
        straights = []

        zigzag_arr = np.zeros((5, 6), dtype=bool)
        straight_arr = np.zeros((5, 6), dtype=bool)

        for i in range(5):
            
            zigzag, straight = self.printaline(i)

            zigzagwins = self.winningline(zigzag)
            straightwins = self.winningline(straight)
            if zigzagwins:
                for x in range(zigzagwins):
                    
                    if (x + 1) % 2 == 0:
                        if i == 4:
                            zigzag_arr[i-1, x] = True
                            
                        else:
                            zigzag_arr[i+1, x] = True
                    else:
                        
                        zigzag_arr[i, x] = True
            
            if straightwins:
                straight_arr[i, :straightwins] = True
            zigzags.append(zigzagwins)
            straights.append(straightwins)
        

        return straight_arr, zigzag_arr
    
    
    def winningline(self, line):
        inarow = 0
        for i in range(5):
            if line[i] == line[i+1]:
                inarow += 1
            else:
                break
        if inarow >= 1:
            return inarow + 1
        else:
            return False


def main():
    x = Reels()
    y = PlayingField()
    y.generate_field()
    x.generate_reel()
    y.checkwinnings()
    


if __name__ == "__main__":
    main()

