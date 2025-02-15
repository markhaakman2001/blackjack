from src.baccarat.BaccaratBank import BaccaratBank
from src.blackjack.gui_shoehand import BlackJackBank
from src.SlotMachine.slot_generator import BankAccount

def UpdateBalanceAfterChanges(baccaratbank : BaccaratBank, blackjackbank : BlackJackBank, slotbank : BankAccount, amounts : list[float]):
    BacAmount  = amounts[0]
    BjAmount   = amounts[1]
    SlotAmount = float(amounts[2]) * 100
    baccaratbank.funds = BacAmount
    blackjackbank.funds = BjAmount
    slotbank._FundsCredits_ = SlotAmount
    
