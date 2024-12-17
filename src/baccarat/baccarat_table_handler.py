import numpy as np
import random
from enum import Enum, auto
from src.baccarat.baccarat_cards import Shoe, Card
from src.baccarat.baccarat_rules_handler import ActionTypes, PlayerType, ActionState, OutComeTypes, SideBets
from PySide6.QtCore import Slot, Signal, QObject


class PlayerBanker:

    def __init__(self, type : PlayerType):
        self.playertype : PlayerType = type
        self.cards_list : list[Card] = []
        self.total_value : int       = 0
        self.total_points            = None
        
    def AddCard(self, card: Card) -> None:
        """Add a card to the player or bankers cards and update the list and total values
        
        Args:
            card (Card): The card that was dealt.
        """        
        self.cards_list.append(card)
        self.card_value = card._get_value()
        self.total_value += self.card_value
        self.CalculatePoints()

    def CalculatePoints(self):
        """Calculates the points of the player/banker based on the baccarat rules.
        """
        if self.total_value <= 9:
            self.total_points = self.total_value
            return self.total_points
        else:
            self.total_value -= 10
            self.CalculatePoints()


class BaccaratTable(QObject):

    ValuesChanged   = Signal(PlayerType, name="ValuesChanged")
    PointsChanged   = Signal(PlayerType, name="PointsChanged")
    FinishedRound   = Signal(int, name="FinishedRound")
    WinnerSignal    = Signal(OutComeTypes, name="winner")
    CardDrawnSignal = Signal(Card)
    PlayerChanged   = Signal(ActionState)

    def __init__(self):
        super().__init__()
        self.shoe         = Shoe(ndecks=8)
        self.player       = PlayerBanker(PlayerType.PLAYER)
        self.banker       = PlayerBanker(PlayerType.BANKER)
        self.CurrentState = ActionState.PLAYERTURN

        self.player_cards : list[Card] = self.player.cards_list
        self.banker_cards : list[Card] = self.banker.cards_list
        self.ValuesChanged.connect(self.PointsChange)
        self.FinishedRound.connect(self.checkwinner)
        self.PlayerChanged.connect(self.printsomethingelse)
        self.WinnerSignal.connect(self.printsomething)
        self.CardDrawnSignal.connect(self.PrintCard)

    @Slot(Card)
    def PrintCard(self, signal: Card):
        print(f"A card was drawn while {self.CurrentState}, the value was {signal._get_value()}")


    @Slot(PlayerType)
    def PointsChange(self, signal):
        if signal == PlayerType.PLAYER:

            if self.player_cards[-1]._get_value() != 10:
                self.PointsChanged.emit(PlayerType.PLAYER)
        else:

            if self.banker_cards[-1]._get_value() != 10:
                self.PointsChanged.emit(PlayerType.BANKER)
    
    def DrawCard(self) -> Card | None:

        if self.CurrentState == ActionState.PLAYERTURN:
            new_card = self.shoe.getcard()
            self.CardDrawnSignal.emit(new_card)
            self.player.AddCard(new_card)
            self.player.CalculatePoints()
            return new_card
        
        elif self.CurrentState == ActionState.BANKERTURN:
            new_card = self.shoe.getcard()
            self.CardDrawnSignal.emit(new_card)
            self.banker.AddCard(new_card)
            self.banker.CalculatePoints()
            return new_card
        
        elif self.CurrentState == ActionState.FINISHED:
            self.FinishedRound.emit(1)

    @Slot(OutComeTypes)
    def printsomething(self, signal):
        if isinstance(signal, OutComeTypes):
            print(signal)
        else:
            print(f"Signal {signal}, djaai die")
            pass
    
    @Slot(int)
    def printsomethingelse(self, signal):
        if signal == 0:
            BaccaratRules().ChangeState(ActionState.FINISHED)
            print("Finished")
        elif signal == 1:
            BaccaratRules().ChangeState(ActionState.FINISHED)
            print("Also finished but with 1")
                

    @Slot(int)
    def checkwinner(self):
        player_points = self.player.CalculatePoints()
        banker_points = self.banker.CalculatePoints()
        if player_points == banker_points:
            self.WinnerSignal.emit(OutComeTypes.TIE)
        
        elif player_points > banker_points:
            self.WinnerSignal.emit(OutComeTypes.PLAYER)
        
        elif banker_points > player_points:
            self.WinnerSignal.emit(OutComeTypes.BANKER)


    def PlaceFirstCards(self) -> tuple[list[Card], list[Card]]:
        
        new_cards : list[Card] = self.shoe.getcard(n_cards=4)
        
        for i, card in enumerate(new_cards):

            if i in [0, 2]:

                self.player.AddCard(card)
                print(card._get_CardName(), card._get_value())
                self.ValuesChanged.emit(PlayerType.PLAYER)
            else:

                self.banker.AddCard(card)
                print(card._get_CardName(), card._get_value())
                self.ValuesChanged.emit(PlayerType.BANKER)
        
        print(f"Player points: {self.player.CalculatePoints()}")
        print(f"Banker points: {self.banker.CalculatePoints()}")
        

        return self.player_cards, self.banker_cards
    

    def BankerAction(self, action : ActionTypes):
        if action == ActionTypes.DRAW:
            self.DrawCard()
            BaccaratRules().ChangeState(ActionState.FINISHED)
        elif action == ActionTypes.STAND:
            BaccaratRules().ChangeState(ActionState.FINISHED)

    def PlayRound(self):
        
        self.PlaceFirstCards()
        natural_win = BaccaratRules.CheckNaturalWin(self)
        if not natural_win:
            action = BaccaratRules.DrawOrStand(self)
            if action == ActionTypes.DRAW:
                card = self.DrawCard(self)
                BaccaratRules.ChangeState(self, ActionState.BANKERTURN)
                self.BankerAction(BaccaratRules.BankerDrawOrStand(self, card._get_value()))
            else:
                BaccaratRules.ChangeState(self, ActionState.BANKERTURN)
                self.BankerAction(BaccaratRules.TwoCardActions(self))


                





class BaccaratRules(BaccaratTable):

    def __init__(self):
        super().__init__()
    
    
    def ChangeState(self, NewState : ActionState):
        self.CurrentState = NewState
        if self.CurrentState == ActionState.PLAYERTURN or self.CurrentState == ActionState.BANKERTURN:
            self.PlayerChanged.emit(NewState)
        else:
            self.FinishedRound.emit(0)

    def TwoCardActions(self, Points) -> ActionTypes:
        ActionDict = { 
            0: ActionTypes.DRAW,
            1: ActionTypes.DRAW,
            2: ActionTypes.DRAW,
            3: ActionTypes.DRAW,
            4: ActionTypes.DRAW,
            5: ActionTypes.DRAW,
            6: ActionTypes.STAND,
            7: ActionTypes.STAND,
            8: ActionTypes.NATURAL_STAND,
            9: ActionTypes.NATURAL_STAND,
        }

        return ActionDict.get(Points)

    @classmethod
    def CheckNaturalWin(self) -> bool:
        player_action =self.TwoCardActions(self.player.CalculatePoints())
        banker_action = self.TwoCardActions(self.banker.CalculatePoints())
        if banker_action == ActionTypes.NATURAL_STAND or player_action == ActionTypes.NATURAL_STAND:
            self.ChangeState(ActionState.FINISHED)
            self.FinishedRound.emit(1)
            return True
        else:
            return False


    def DrawOrStand(self):
        if self.CurrentState == ActionState.PLAYERTURN:
            points               = self.player.CalculatePoints()
            action : ActionTypes = self.TwoCardActions(points)
            return action
        
        elif self.CurrentState == ActionState.BANKERTURN:
            points               = self.banker.CalculatePoints()
            action : ActionTypes = self.TwoCardActions(points)
            return action
        
    def BankerDrawOrStand(self, PlayerThirdCard : int):

        BankerPoints = self.banker.CalculatePoints()
        banker3 = {0:ActionTypes.DRAW , 1:ActionTypes.DRAW, 2:ActionTypes.DRAW, 3:ActionTypes.DRAW, 4:ActionTypes.DRAW, 5:ActionTypes.DRAW, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.DRAW }
        banker4 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.DRAW, 3:ActionTypes.DRAW, 4:ActionTypes.DRAW, 5:ActionTypes.DRAW, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }
        banker5 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.STAND, 3:ActionTypes.STAND, 4:ActionTypes.DRAW, 5:ActionTypes.DRAW, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }
        banker6 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.STAND, 3:ActionTypes.STAND, 4:ActionTypes.STAND, 5:ActionTypes.STAND, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }
        banker7 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.STAND, 3:ActionTypes.STAND, 4:ActionTypes.STAND, 5:ActionTypes.STAND, 6:ActionTypes.STAND, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }

        BankerActionDict = { 3: banker3, 4:banker4, 5:banker5 , 6:banker6, 7:banker7}

        if BankerPoints <= 2:
            
            return ActionTypes.DRAW
        
        elif BankerPoints > 6:
            
            self.FinishedRound.emit(0)
            return ActionTypes.STAND
        
        else:
            self.FinishedRound.emit(0)
            return BankerActionDict[self.banker.CalculatePoints()][PlayerThirdCard]


if __name__ == "__main__":
    table = BaccaratTable()
    table.PlayRound()



