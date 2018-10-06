from helper.player import *
from bot.BotNerves import *
from enum import Enum

class State(Enum):
    BASE = 0

    MINE = 1
    GETM = 2
    GETH = 3
    HOME = 4
    UPGR = 5


class BotBrain:
    CurrentState = State.BASE
    nerve = BotNerves()

    def __init__(self):
        pass

    @staticmethod
    def nextPhase(PlayerInfo):

        if BotBrain.CurrentState == State.BASE:  ####################################################
            if PlayerInfo.CarriedResources == PlayerInfo.CarryingCapacity:
                BotBrain.CurrentState = State.GETH

            else:
                BotBrain.CurrentState = State.GETM

        elif BotBrain.CurrentState == State.HOME:  ##################################################
            BotBrain.CurrentState = State.GETM

        elif BotBrain.CurrentState == State.GETM:  ##################################################
            if PlayerInfo.Position in BotBrain.nerve.nextToMineral():
                BotBrain.CurrentState = State.MINE

        elif BotBrain.CurrentState == State.MINE:  #################################################
            if PlayerInfo.CarriedResources == PlayerInfo.CarryingCapacity:
                BotBrain.CurrentState = State.GETH

            if PlayerInfo.Position not in BotBrain.nerve.nextToMineral():
                BotBrain.CurrentState = State.GETM

        elif BotBrain.CurrentState == State.GETH:  #################################################
            if PlayerInfo.Position == PlayerInfo.HouseLocation:
                BotBrain.CurrentState = State.UPGR

        elif BotBrain.CurrentState == State.UPGR:  #################################################
            if BotBrain.nerve.check_if_can_upgrade(PlayerInfo):
                BotBrain.CurrentState = State.HOME

            else:
                BotBrain.CurrentState = State.HOME

    @staticmethod
    def DoSomeThing(PlayerInfo, gameMap):

        if BotBrain.CurrentState == State.HOME:
            pass

        elif BotBrain.CurrentState == State.GETM:
            return BotBrain.nerve.go_mine(gameMap, PlayerInfo)

        elif BotBrain.CurrentState == State.MINE:
            return BotBrain.nerve.mine(PlayerInfo)

        elif BotBrain.CurrentState == State.GETH:
            return BotBrain.nerve.go_home(PlayerInfo)

        elif BotBrain.CurrentState == State.UPGR:
            return BotBrain.nerve.purchase_upgrade(PlayerInfo)
