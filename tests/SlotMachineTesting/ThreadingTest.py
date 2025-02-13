from tests.SlotMachineTesting.TestSlot import PlayingField, Reels
import threading
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtCore import QTimer

class SLotGameSimulator:

    def __init__(self):
        self.slot        = PlayingField()
        self.symbol_dict = self.slot.symbol_val_dict
        self.index_dict       = {2:'3 hits', 3:'4 hits', 4:'5 hits', 5:'6 hits'}
        self.df_columns       = ['10', 'j', 'q', 'k', 'a', 'moneybag', 'goldstack', 'diamond', 'chest']
        self.df_indexes       = ['3 hits', '4 hits', '5 hits', '6 hits']
        self.df_hitstolen     = [2, 3, 4, 5]
        self.index_len_dict   = dict(zip(self.df_indexes, self.df_hitstolen))
        self.TotalBets  = 0
        self.TotalHits  = 0
        self.TotalSpins = 0
        self.TotalWin   = 0
        self.RTP        = 0
        self.DataList   = [self.TotalBets, self.TotalWin, self.RTP, self.TotalSpins, self.TotalHits]
        self.wins_df          = None
        self.spin_data_list   = []
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

    def StartSpins(self, n_spins=100000):
        self._spin_thread = threading.Thread(
            target=self.SimulateNspins,
            kwargs={"n_spins":n_spins},
        )
        self._spin_thread.setDaemon = True
        self._spin_thread.start()
        
        plt.figure(num="Thread plot")
        plt.ion()
        while self._spin_thread.is_alive:
            plt.clf()
            plt.plot(self.symbol_df)
            plt.draw_if_interactive()
            plt.pause(0.1)


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
        #print("data list here:", self.spin_data_list)
        self.totals_df = pd.DataFrame(data=[self.TotalBets, self.TotalWin, self.RTP, self.TotalSpins, self.TotalHits], columns=['value'], index=['Total Bet (credits)', 'Total Win (credits)', 'RTP (%)', 'spins', 'Hits'])

    
    
    def SimulateNspins(self, n_spins=100000):
        total_bet       = 0
        lens            = [0] * 4
        symbol_stat_arr = np.column_stack([lens]*9)
        total_hits      = 0
        total_spins     = n_spins
        self.TotalBets  = 0
        self.TotalHits  = 0
        self.TotalSpins = n_spins
        self.TotalWin   = 0
        self.RTP        = 0
        self.DataList   = [self.TotalBets, self.TotalWin, self.RTP, self.TotalSpins, self.TotalHits]
        for x in range(n_spins):
            symbol_stats, spin_hit        = self.slot.OneSpinStats()
            symbol_stat_arr               = symbol_stat_arr + symbol_stats
            self.TotalBets               += 100
            self.symbol_df = pd.DataFrame(data=symbol_stat_arr, index=self.df_indexes, columns=self.df_columns)
            if spin_hit:
                self.TotalHits += 1

            self.GetWinsPerSymbol()
            #print(f"{total_bet=}")


    # def PlotData(self, showPlots=True, ex_cols : list[str|int] | None =None) -> None:
    #     self.fig.clear()
    #     self.ax.clear()
    #     # self.GetWinsPerSymbol()
        
    #     self.ax.axis('off')
    #     pd.plotting.table(ax=self.ax, data=self.totals_df, loc='center', colWidths=[0.5], colLoc='left')
    #     plt.draw()
    #     if ex_cols:
    #         self.symbol_df.drop(columns=ex_cols, inplace=True)
    #         self.wins_df.drop(columns=ex_cols, inplace=True)
    #     self.wins_df.plot(ax=self.ax2[0], kind="bar")
    #     plt.draw()
    #     self.symbol_df.plot(ax=self.ax2[1])
    #     if showPlots:
    #         plt.show()


def main():
    sim = SLotGameSimulator()
    sim.StartSpins(1000000)

if __name__ == "__main__":
    main()