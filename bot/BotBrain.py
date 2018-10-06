from helper.player import *
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
    def nextPhase(player):

        if BotBrain.CurrentState == State.BASE:  ####################################################
            if player.CarriedResources == player.CarryingCapacity:
                BotBrain.CurrentState = State.GETH

            else:
                BotBrain.CurrentState = State.GETM

        elif BotBrain.CurrentState == State.HOME:  ##################################################
            BotBrain.CurrentState = State.GETM

        elif BotBrain.CurrentState == State.GETM:  ##################################################
            if player.Position in nextToMineral():
                BotBrain.CurrentState = State.MINE

        elif BotBrain.CurrentState == State.MINE:  #################################################
            if player.CarriedResources == player.CarryingCapacity:
                BotBrain.CurrentState = State.GETH

            if player.Position not in nextToMineral():
                BotBrain.CurrentState = State.GETM

        elif BotBrain.CurrentState == State.GETH:  #################################################
            if player.Position == player.HouseLocation:
                BotBrain.CurrentState = State.UPGR

        elif BotBrain.CurrentState == State.UPGR:  #################################################
            if player.TotalResources >= neededRSC():
                BotBrain.CurrentState = State.HOME

            else:
                BotBrain.CurrentState = State.HOME

    @staticmethod
    def DoSomeThing():

        if BotBrain.CurrentState == State.HOME:
            pass

        elif BotBrain.CurrentState == State.GETM:
            pass

        elif BotBrain.CurrentState == State.MINE:
            pass

        elif BotBrain.CurrentState == State.GETH:
            pass

        elif BotBrain.CurrentState == State.UPGR:
            pass
