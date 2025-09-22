from enum import Enum, auto


class BlackJackSideBets():

    class TwentyOnePlusThree(Enum):
        TRIPS_SUITED    = 100
        STRAIGHT_FLUSH  = 40
        TRIPS_NORMAL    = 30
        STRAIGHT_NORMAL = 10
        FLUSH           = 5
    
    class Pairs(Enum):

        PERFECT_PAIR = 25
        COLOR_PAIR   = 12
        MIXED_PAIR   = 6


if __name__ == "__main__":
    print(BlackJackSideBets.TwentyOnePlusThree.TRIPS_SUITED.value)