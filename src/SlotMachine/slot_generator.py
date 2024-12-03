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
            6 : "Koen",
            7 : "Raasa",
            8 : "Mark",
            9 : "Niels",
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
        
        self.reel_disp = np.array([self.possible_values.get(x) for x in self.reel_values])
        


class PlayingField:

    def __init__(self):

        self.reels = [Reels()] * 6
        self.full_field = np.zeros((5, 6))
        self.full_field_disp = np.empty((5, 6), dtype='<U5')
    
    def generate_field(self):
        
        for i, reel in enumerate(self.reels):
            reel.generate_reel()
            self.full_field[:, i] = reel.reel_values
            self.full_field_disp[:, i] = reel.reel_disp

            print(self.full_field)
            print(self.full_field_disp)
            for i, slot in enumerate(self.full_field):
                print(i, slot)
        
    def printaline(self, row_index):
        zigzagline = []
        straightline = self.full_field[row_index]

        for x in range(1, 7):
            if x % 2 == 0:
                zigzagline.append(int(self.full_field[row_index+1, x-1]))
            else:
                zigzagline.append(int(self.full_field[row_index][x-1]))

        print(zigzagline)
        print(straightline)

def main():

    x = Reels()
    y = PlayingField()
    y.generate_field()
    x.generate_reel()
    y.printaline(0)


if __name__ == "__main__":
    main()

