import numpy as np
from math import *
import random
from PySide6.QtCore import Signal, Slot


class Reels:

    def __init__(self):

        # What the slot machine has to display, instead of integers
        self.possible_values = { 
            5 : "10",
            6 : "J",
            7 : "Q",
            8 : "K",
            9 : "A",
            1 : "2",
            2 : "3",
            3 : "4",
            4 : "5",
        }

        self.inverse_possible_values = {v: k for k, v in self.possible_values.items()}

        slots = [0]*5
        self.reel_values = np.array(slots)
        self.reel_disp = np.array(slots)
    

    def generate_reel(self):
        """For each of the 5 slots in the reel, choose a random integer between 1 and 9 that corresponds to a symbol in the game.
        """        

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
    """The playingfield is the full screen with 6 reels.
    """    
    signal1 = Signal()
    def __init__(self):

        self.reels = []
        for x in range(6):
            r = Reels()
            self.reels.append(r)
        self.full_field = np.zeros((5, 6))
        self.full_field_disp = np.empty((5, 6), dtype='<U5')
        self.signal1 = Signal()
    
    def generate_field(self):
        """Generate new reels for all 6 reels in the playingfield.
        """        
        
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
    

    def checkwinnings(self, betsize):
        zigzags = []
        straights = []

        zigzag_arr = np.zeros((5, 6), dtype=bool)
        straight_arr = np.zeros((5, 6), dtype=bool)

        totalwin = 0

        for i in range(5):
            
            zigzag, straight = self.printaline(i)

            zigzagwins = self.winningline(zigzag)
            straightwins = self.winningline(straight)
            if zigzagwins:
                
                symbol = int(self.full_field[i, 0])
                win = self.prizecheck(symbol_val=symbol, length=zigzagwins, betsize=betsize)
                totalwin += win
                for x in range(zigzagwins):
                    
                    if (x + 1) % 2 == 0:
                        if i == 4:
                            zigzag_arr[i-1, x] = True
                            
                        else:
                            zigzag_arr[i+1, x] = True
                    else:
                        
                        zigzag_arr[i, x] = True
            
            if straightwins:
                symbol = int(self.full_field[i, 0])
                win = self.prizecheck(symbol_val=symbol, length=straightwins, betsize=betsize)
                totalwin += win
                straight_arr[i, :straightwins] = True
                
            zigzags.append(zigzagwins)
            straights.append(straightwins)
        

        return straight_arr, zigzag_arr, totalwin
    

    def prizecheck(self, symbol_val:int, length:int, betsize):
        calculator = { 
            1 : lambda x, y: y * x*0.1,
            2 : lambda x, y: y * x *  0.2,
            3 : lambda x, y: y * x *  0.2,
            4 : lambda x, y: y * x *  0.2,
            5 :  lambda x, y: y * x * 0.2 ,
            6 : lambda x, y: y * x * 0.5,
            7 : lambda x, y: y * x * 0.5,
            8 : lambda x, y: y * x * 0.6,
            9 : lambda x, y: y * x * 2,
            }
        winamount = calculator.get(symbol_val)(length, betsize)
        return winamount


    
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


class BankAccount:

    def __init__(self):
        self.current_funds : float = 0
        self.funds : float = 0
        self._bet : float = 0

    def deposit(self, amount):
        self._set_funds(amount)
        self.current_funds += amount


    def placebet(self, amount):
        self.current_bet = amount
        self.current_funds -= amount
        self._set_funds(amount * (-1))
        print(self.current_funds, self._get_funds())
    
    def add_winnings(self, winnings):
        self.current_funds += winnings
        self.current_bet = 0
        self._set_funds((winnings))
        print(self.current_funds, self._get_funds())
    

    def _get_funds(self):
        return self.funds
    
    def _set_funds(self, amount):
        self.funds += amount
    
    def _del_funds(self):
        del self.funds

    fundings = property(
        fget=_get_funds,
        fset=_set_funds,
        fdel=_del_funds,
    )
        

            



def main():
    x = Reels()
    y = PlayingField()
    y.generate_field()
    x.generate_reel()
    y.checkwinnings()

    


if __name__ == "__main__":
    main()

