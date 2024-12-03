import numpy as np
from math import *
import random


class Reels:

    def __init__(self):
        self.possible_values = { 
            1 : "10",
            2 : "J",
            3 : "Q",
            4 : "K",
            5 : "A",
            6 : "Koen",
            7 : "Raasa",
            8 : "Mark",
        }

        self.inverse_possible_values = {v: k for k, v in self.possible_values.items()}

        slots = [0]*5
        self.reel_values = np.array(slots)
        self.reel_disp = np.array(slots)
    
    def generate_reel(self):

        new_reel = []
        for x in range(5):
            x = random.randint(1, 8)
            new_reel.append(x)

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
        

            

        




def main():
    x = Reels()
    y = PlayingField()
    y.generate_field()
    x.generate_reel()


if __name__ == "__main__":
    main()

