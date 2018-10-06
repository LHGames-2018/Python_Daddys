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

    def __init__(self):
        pass

    @staticmethod
    def nextPhase(PlayerInfo, gameMap):

        if BotBrain.CurrentState == State.BASE:  ####################################################
            if PlayerInfo.CarriedResources == PlayerInfo.CarryingCapacity:
                BotBrain.CurrentState = State.GETH

            else:
                BotBrain.CurrentState = State.GETM

        elif BotBrain.CurrentState == State.HOME:  ##################################################
            BotBrain.CurrentState = State.GETM

        elif BotBrain.CurrentState == State.GETM:  ##################################################
            if PlayerInfo.Position in BotNerves.nextToMineral(gameMap, PlayerInfo):
                BotBrain.CurrentState = State.MINE

        elif BotBrain.CurrentState == State.MINE:  #################################################
            if PlayerInfo.CarriedResources == PlayerInfo.CarryingCapacity:
                BotBrain.CurrentState = State.GETH

            if PlayerInfo.Position not in BotNerves.nextToMineral(gameMap, PlayerInfo):
                BotBrain.CurrentState = State.GETM

        elif BotBrain.CurrentState == State.GETH:  #################################################
            if PlayerInfo.Position == PlayerInfo.HouseLocation:
                BotBrain.CurrentState = State.UPGR

        elif BotBrain.CurrentState == State.UPGR:  #################################################
            if BotNerves.check_if_can_upgrade(PlayerInfo):
                BotBrain.CurrentState = State.HOME

            else:
                BotBrain.CurrentState = State.HOME

    @staticmethod
    def DoSomeThing(PlayerInfo, gameMap):

        if BotBrain.CurrentState == State.HOME:
            pass

        elif BotBrain.CurrentState == State.GETM:
            return BotNerves.go_mine(gameMap, PlayerInfo)

        elif BotBrain.CurrentState == State.MINE:
            return BotNerves.mine(PlayerInfo)

        elif BotBrain.CurrentState == State.GETH:
            return BotNerves.go_home(PlayerInfo, gameMap)

        elif BotBrain.CurrentState == State.UPGR:
            return BotNerves.purchase_upgrade(PlayerInfo)
