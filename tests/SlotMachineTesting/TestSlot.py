import numpy as np
import random
from PySide6.QtCore import Signal, QObject
import pandas as pd
import itertools as it
import matplotlib.pyplot as plt
import threading

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

        self.choices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.weights = [0, 0, 0.25, 0.25, 0.2, 0, 0.1, 0.1, 0.1]

        slots = [0]*5
        self.reel_values = np.array(slots)
        self.reel_disp = np.array(slots)
    

    def generate_reel(self):
        """For each of the 5 slots in the reel, choose a random integer between 1 and 9 that corresponds to a symbol in the game.
        """        

        new_reel = []

        # choose a random digit for every slot in the reel
        for x in range(5):
            # x = random.randint(1, 9)
            z = random.choices(self.choices, weights=self.weights, k=1)
            y = z[0]
            new_reel.append(y)

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
            self.symbol_val_dict = r.possible_values
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
            1 : lambda x, y: y * x * 0.1,
            2 : lambda x, y: y * x * 0.2,
            3 : lambda x, y: y * x * 0.2,
            4 : lambda x, y: y * x * 0.2,
            5 : lambda x, y: y * x * 0.2,
            6 : lambda x, y: y * x * 0.5,
            7 : lambda x, y: y * x * 0.5,
            8 : lambda x, y: y * x * 0.6,
            9 : lambda x, y: y * x * 2  ,
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
                first = self.full_field[line[0][0], line[0][1]]
                while x < 4:
                    current = line[x]
                    nextone = line[x+1]
                    fld     = self.full_field
                    if fld[current[0], current[1]] == fld[nextone[0], nextone[1]]:
                        x += 1
                        y += 1
                    else:
                        x = 5
                yield y, int(first)

    def OneSpinStats(self, betsize=100):
        symbol_len = [0]*4
        symbols = [symbol_len] * 9
        symbol_arr = np.column_stack(symbols)
        spin_hit = False
        self.generate_field()
        for nr_wins, symbol_val in self.LineCountGenerator():
            if nr_wins > 1:
                symbol_arr[nr_wins-2, symbol_val-1] += 1
                spin_hit = True
        return symbol_arr, spin_hit


class SLotGameSimulator:

    def __init__(self):
        self.slot        = PlayingField()
        self.symbol_dict = self.slot.symbol_val_dict
        self.index_dict       = {2:'3 hits', 3:'4 hits', 4:'5 hits', 5:'6 hits'}
        self.df_columns       = ['10', 'j', 'q', 'k', 'a', 'moneybag', 'goldstack', 'diamond', 'chest']
        self.df_indexes       = ['3 hits', '4 hits', '5 hits', '6 hits']
        self.df_hitstolen     = [2, 3, 4, 5]
        self.index_len_dict   = dict(zip(self.df_indexes, self.df_hitstolen))
        self.wins_df          = None
        self.spin_data_list   = []
        self.fig, self.ax     = plt.subplots()
        self.f2,  self.ax2    = plt.subplots(nrows=2, ncols=1, figsize=(100, 100))
        self.calculator = { 
            '10'        : lambda x :   (100 * x * 0.10) ,
            'j'         : lambda x :   (100 * x * 0.75) ,
            'q'         : lambda x :   (100 * x * 0.50) ,
            'k'         : lambda x :   (100 * x * 0.55) ,
            'a'         : lambda x :   (100 * x * 1.50) ,
            'moneybag'  : lambda x :   (100 * x * 1.50) ,
            'goldstack' : lambda x :   (100 * x * 2.00) ,
            'diamond'   : lambda x :   (100 * x * 2.50) ,
            'chest'     : lambda x :   (100 * x * 2.50) ,
                        }
        #self.symbol_df        = pd.DataFrame(0, index=self.df_indexes, columns=self.df_columns, dtype=int)


    def CalculateWin(self, symbol, len):
        return self.calculator.get(symbol)(len)

    def GetWinsPerSymbol(self):
        new_df                    = self.symbol_df.apply(lambda x : self.CalculateWin(symbol=x.name, len=x), axis=0)
        self.wins_df              = new_df.apply(lambda x : self.index_len_dict.get(x.name) * x, axis=1)
        self.wins_df              = self.wins_df.transpose()
        self.wins_df['totals']    = self.wins_df.sum(axis=1)
        self.TotalWin             = self.wins_df['totals'].sum()
        self.wins_df              = self.wins_df.transpose()

        self.RTP = (self.TotalWin / self.TotalBets) * 100
        self.spin_data_list.insert(1, round(float(self.RTP), 3))
        self.spin_data_list.insert(1, int(self.TotalWin))
        print("data list here:", self.spin_data_list)
        self.totals_df = pd.DataFrame(data=self.spin_data_list, columns=['value'], index=['Total Bet (credits)', 'Total Win (credits)', 'RTP (%)', 'spins', 'Hits'])
        print(self.totals_df)
        print(self.symbol_df)
        print(self.wins_df)
        print(self.TotalWin)

    
    
    def SimulateNspins(self, n_spins=100000):
        total_bet       = 0
        lens            = [0] * 4
        symbol_stat_arr = np.column_stack([lens]*9)
        total_hits      = 0
        total_spins     = n_spins
        for x in range(n_spins):
            symbol_stats, spin_hit   = self.slot.OneSpinStats()
            symbol_stat_arr          = symbol_stat_arr + symbol_stats
            total_bet               += 100
            if spin_hit:
                total_hits += 1
        

        self.symbol_df = pd.DataFrame(data=symbol_stat_arr, index=self.df_indexes, columns=self.df_columns)
        self.TotalSpins = total_spins
        self.TotalHits  = total_hits
        self.TotalBets  = total_bet
        for x in list([int(total_bet), int(total_spins), int(total_hits)]):
            self.spin_data_list.append(x)
        self.GetWinsPerSymbol()
        print(f"{total_bet=}")


    def PlotData(self, showPlots=True, ex_cols : list[str|int] | None =None) -> None:
        self.fig.clear()
        self.ax.clear()
        # self.GetWinsPerSymbol()
        
        self.ax.axis('off')
        pd.plotting.table(ax=self.ax, data=self.totals_df, loc='center', colWidths=[0.5], colLoc='left')
        plt.draw()
        if ex_cols:
            self.symbol_df.drop(columns=ex_cols, inplace=True)
            self.wins_df.drop(columns=ex_cols, inplace=True)
        self.wins_df.plot(ax=self.ax2[0], kind="bar")
        plt.draw()
        self.symbol_df.plot(ax=self.ax2[1])
        if showPlots:
            plt.show()
            


def main():
    field = PlayingField()
    sim = SLotGameSimulator()
    sim.SimulateNspins(n_spins=10000)
    sim.PlotData(ex_cols=['10', 'j', 'moneybag'])

    
    


if __name__ == "__main__":
    main()
    

        

