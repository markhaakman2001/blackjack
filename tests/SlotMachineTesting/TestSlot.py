import numpy as np
import random
from PySide6.QtCore import Signal, QObject

class Reels:

    def __init__(self):

        # What the slot machine has to display, instead of integers
        self.possible_values = { 
            1 : "10",
            2 : "j",
            3 : "q",
            4 : "k",
            5 : "a",
            6 : "moneybag",
            7 : "goldstack",
            8 : "diamond",
            9 : "chest",
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
        self.CreateDiagonalLines()
        self.CreateZigZagLines()
        self.CreateStraightLines()
    
    def generate_field(self):
        """
        The PlayingField is a (5, 6) numpy array with integers representing symbols.
        Each column represents a Reel of 5 symbols and each row can represent a line.

        An example of a PlayingField represented by integers can be:
        ----------

        |   [[3. 1. 1. 8. 3. 5.]   | \n
        |    [1. 7. 5. 5. 3. 2.]   | \n
        |    [4. 7. 4. 1. 6. 4.]   | \n
        |    [3. 6. 4. 1. 3. 6.]   | \n
        |    [9. 1. 4. 1. 7. 7.]]  | \n

        The same PlayingField represented by symbols is:
        ----------
        |   [['4' '2' '2'  'K'  '4' '10']   |\n
        |    ['2' 'Q' '10' '10' '4' '3' ]   |\n
        |    ['5' 'Q' '5'  '2'  'J' '5' ]   |\n
        |    ['4' 'J' '5'  '2'  '4' 'J' ]   |\n
        |    ['A' '2' '5'  '2'  'Q' 'Q' ]]  |\n

        ----------
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
    
    #@_LoggingDecorator_
    def checkwinnings(self, betsize) -> tuple[np.ndarray, np.ndarray, float]:
        """Using the current PlayingField and the given betsize, checks for any winning lines.

        The PlayingField is a (5, 6) numpy array with integers representing symbols.
        Each column represents a Reel of 5 symbols and each row can represent a line.

        A winning line can be a straight vertical line with 2 or more identical symbols in a row starting from the leftmost reel.
        A winning line can also be a 'ZigZag line', with 2 or more identical symbols in a row.

        Example of a playing field with a winning straight line in the first row:
        ----------
        [[2. 2. 2. 2. 2. 2.] \n
        [5. 3. 2. 2. 9. 9.] \n
        [4. 2. 7. 5. 8. 7.] \n
        [5. 1. 9. 1. 3. 2.] \n
        [4. 6. 8. 4. 3. 8.]] \n
        
        ----------
        Example of a playing field with a winning ZigZag line in the First and Last row:
        ----------
        [[2. 3. 2. 8. 2. 8.] \n
        [5. 2. 3. 2. 9. 2.] \n
        [4. 2. 7. 5. 8. 7.] \n
        [5. 4. 9. 4. 3. 4.] \n
        [4. 6. 4. 6. 4. 8.]] \n

        Args:
            betsize (_type_): _description_

        Returns:
            tuple[np.ndarray, np.ndarray, float]: _description_
        """        
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
                print(f"ZigZagWin is {win}")
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
                print(f"Straightwin = {win}")
                totalwin += win
                straight_arr[i, :straightwins] = True
                
            zigzags.append(zigzagwins)
            straights.append(straightwins)
        
        print(straight_arr, zigzag_arr, totalwin)
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
    
    def CreateDiagonalLines(self):
        self.diagonals = [[], []]
        for x in range(6):
            if x <= 2:
                self.diagonals[0].append([x  , x])
                self.diagonals[1].append([4-x, x])
            if x >= 3:
                self.diagonals[0].append([x-1, x])
                self.diagonals[1].append([5-x, x])
    
    def CreateZigZagLines(self):
        self.zigzags = [[], [], [], [], []]
        for x in range(6):

            if ((x+1) % 2) == 0:
                y=1
            else:
                y=0
            
            for i, zigzaglist in enumerate(self.zigzags):
                if i == 4:
                    zigzaglist.append([i-y, x])
                else:
                    zigzaglist.append([i+y, x])
    
    def CreateStraightLines(self):
        self.straights = [[], [], [], [], []]
        for x in range(6):
            for i, str in enumerate(self.straights):
                str.append([i, x])


    def LineCountGenerator(self):
        lists = [self.diagonals, self.zigzags, self.straights]
        for lineslists in lists:
            
            for line in lineslists:
                x=0
                y=0
                while x < 6:
                    current = line[x]
                    nextone = line[x+1]
                    fld     = self.full_field
                    if fld[current[0], current[1]] == fld[nextone[0], nextone[1]]:
                        x += 1
                        y += 1
                    else:
                        x = 6
                yield y




def main():
    field = PlayingField()
    field.generate_field()

    print(field.full_field)

    for x in field.LineCountGenerator():
        print(x)


if __name__ == "__main__":
    main()
    

        

