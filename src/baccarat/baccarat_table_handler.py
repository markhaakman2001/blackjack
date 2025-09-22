from baccarat.baccarat_cards import Shoe, Card, Color
from baccarat.baccarat_rules_handler import ActionTypes, PlayerType, ActionState, OutComeTypes
from ErrorFiles.BankingErrors import BankingErrorChecker
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
    
    def Replay(self):
        self.cards_list = []
        self.total_value = 0
        self.total_points = None

class BaccaratTable(QObject):

    ValuesChanged   = Signal(PlayerType, name="ValuesChanged")
    PointsChanged   = Signal(PlayerType, name="PointsChanged")
    FinishedRound   = Signal(int, name="FinishedRound")
    SideBetWin      = Signal(int, name="SideBetWin")
    WinnerSignal    = Signal(OutComeTypes, name="winner")
    CardDrawnSignal = Signal(Card)
    FirstAnimSignal = Signal(name="Animations")
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
        self.CardDrawnSignal.connect(self.PrintCard)

    @Slot(Card)
    def PrintCard(self, signal: Card):
        print(f"A card was drawn while {self.CurrentState}, the value was {signal._get_value()}")

    @Slot(int)
    def PrintSideBetWin(self, signal: int):
        print(f"A sidebet was won with signal {signal}")


    @Slot(PlayerType)
    def PointsChange(self, signal):
        if signal == PlayerType.PLAYER:
            self.player.CalculatePoints()
            self.PointsChanged.emit(PlayerType.PLAYER)
        else:
            self.banker.CalculatePoints()
            self.PointsChanged.emit(PlayerType.BANKER)
    
    
    def DrawCard(self) -> Card | None:

        if self.CurrentState == ActionState.PLAYERTURN:
            new_card = self.shoe.getcard()
            self.CardDrawnSignal.emit(new_card)
            self.ValuesChanged.emit(PlayerType.PLAYER)
            self.player.AddCard(new_card)
            self.player.CalculatePoints()
            print(f"Player pulled {new_card._get_value()}")
            return new_card
        
        elif self.CurrentState == ActionState.BANKERTURN:
            new_card = self.shoe.getcard()
            self.CardDrawnSignal.emit(new_card)
            self.ValuesChanged.emit(PlayerType.BANKER)
            self.banker.AddCard(new_card)
            self.banker.CalculatePoints()
            print(f"Banker pulled {new_card._get_value()}")
            return new_card
        
        elif self.CurrentState == ActionState.FINISHED:
            self.FinishedRound.emit(1)

    @Slot(OutComeTypes)
    def printsomething(self, signal):
        if isinstance(signal, OutComeTypes):
            print(signal)
            print(f" Player total {self.player.CalculatePoints()} \n banker total {self.banker.CalculatePoints()}")
        else:
            print(f"Signal {signal}, djaai die")
            pass
    
    @Slot(int)
    def printsomethingelse(self, signal):
        if signal == 0:
            self.RuleChecker.ChangeState(ActionState.FINISHED)
            print("Finished")
        elif signal == 1:
            self.RuleChecker.ChangeState(ActionState.FINISHED)
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
        
        self.FirstAnimSignal.emit()
        return self.player_cards, self.banker_cards
    

    def BankerAction(self, action : ActionTypes):
        if action == ActionTypes.DRAW:
            self.DrawCard()
            self.RuleChecker.ChangeState(ActionState.FINISHED)
        elif action == ActionTypes.STAND:
            self.RuleChecker.ChangeState(ActionState.FINISHED)

    @BankingErrorChecker._CheckForPlacedBets
    def PlayRound(self, *args):
        self.RuleChecker = BaccaratRules(self)
        self.PlaceFirstCards()
        natural_win = self.RuleChecker.CheckNaturalWin()
        if not natural_win:
            action = self.RuleChecker.DrawOrStand()
            if action == ActionTypes.DRAW:
                card = self.DrawCard()
                self.RuleChecker.ChangeState(ActionState.BANKERTURN)
                print(self.CurrentState)
                print("test")
                self.BankerAction(self.RuleChecker.BankerDrawOrStand(card._get_value()))
            else:
                self.RuleChecker.ChangeState(ActionState.BANKERTURN)
                points = self.banker.CalculatePoints()
                self.BankerAction(self.RuleChecker.TwoCardActions(points))

    def ResetTable(self):
        self.player.Replay()
        self.banker.Replay()
        self.player_cards : list[Card] = self.player.cards_list
        self.banker_cards : list[Card] = self.banker.cards_list
        self.CurrentState              = ActionState.ResetState


class BaccaratRules:

    def __init__(self, Class : BaccaratTable):
        self.bac = Class
    
    def ChangeState(self, NewState : ActionState):
        self.bac.CurrentState = NewState
        if self.bac.CurrentState == ActionState.PLAYERTURN or self.bac.CurrentState == ActionState.BANKERTURN:
            self.bac.PlayerChanged.emit(NewState)
        else:
            self.bac.FinishedRound.emit(0)

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

    def CheckNaturalWin(self) -> bool:
        player_action = self.TwoCardActions(self.bac.player.CalculatePoints())
        banker_action = self.TwoCardActions(self.bac.banker.CalculatePoints())
        if banker_action == ActionTypes.NATURAL_STAND or player_action == ActionTypes.NATURAL_STAND:
            self.ChangeState(ActionState.FINISHED)
            self.bac.FinishedRound.emit(1)
            return True
        else:
            print("No natural win")
            return False


    def DrawOrStand(self):
        if self.bac.CurrentState == ActionState.PLAYERTURN:
            points               = self.bac.player.CalculatePoints()
            action : ActionTypes = self.TwoCardActions(points)
            return action
        
        elif self.bac.CurrentState == ActionState.BANKERTURN:
            points               = self.bac.banker.CalculatePoints()
            action : ActionTypes = self.TwoCardActions(points)
            return action
        
    def BankerDrawOrStand(self, PlayerThirdCard : int):
        
        if PlayerThirdCard >= 10:
                PlayerThirdCard -= 10

        BankerPoints = self.bac.banker.CalculatePoints()
        banker3 = {0:ActionTypes.DRAW , 1:ActionTypes.DRAW, 2:ActionTypes.DRAW, 3:ActionTypes.DRAW, 4:ActionTypes.DRAW, 5:ActionTypes.DRAW, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.DRAW }
        banker4 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.DRAW, 3:ActionTypes.DRAW, 4:ActionTypes.DRAW, 5:ActionTypes.DRAW, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }
        banker5 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.STAND, 3:ActionTypes.STAND, 4:ActionTypes.DRAW, 5:ActionTypes.DRAW, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }
        banker6 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.STAND, 3:ActionTypes.STAND, 4:ActionTypes.STAND, 5:ActionTypes.STAND, 6:ActionTypes.DRAW, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }
        banker7 = {0:ActionTypes.STAND , 1:ActionTypes.STAND, 2:ActionTypes.STAND, 3:ActionTypes.STAND, 4:ActionTypes.STAND, 5:ActionTypes.STAND, 6:ActionTypes.STAND, 7:ActionTypes.DRAW, 8:ActionTypes.STAND, 9:ActionTypes.STAND }

        BankerActionDict = { 3: banker3, 4:banker4, 5:banker5 , 6:banker6, 7:banker7}

        if BankerPoints <= 2:
            
            return ActionTypes.DRAW
        
        elif BankerPoints > 6:
            
            self.bac.FinishedRound.emit(0)
            return ActionTypes.STAND
        
        else:
            self.bac.FinishedRound.emit(0)
            
            return BankerActionDict[self.bac.banker.CalculatePoints()][PlayerThirdCard]

    def CheckBaccaratSideBets(self):
        BankerCards = self.bac.banker_cards
        PlayerCards = self.bac.player_cards
        if BankerCards[0]._get_CardColor() == BankerCards[1]._get_CardColor():
            self.bac.SideBetWin.emit(0)
        if PlayerCards[0]._get_CardColor() == PlayerCards[1]._get_CardColor():
            self.bac.SideBetWin.emit(1)

if __name__ == "__main__":
    table = BaccaratTable()
    table.PlayRound()



