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
            BotBrain.CurrentState = State.WALK
            return  # get to mine

        elif BotBrain.CurrentState == State.HOME:  ##################################################
            BotBrain.CurrentState = State.GETM
            return  # get to mine

        elif BotBrain.CurrentState == State.GETM:  ##################################################
            if player.Position in nextToMineral():
                BotBrain.CurrentState = State.MINE
                return  # mine

            else:
                return  # walk to mineral

        elif BotBrain.CurrentState == State.MINE:  #################################################
            if player.CarriedResources == player.CarryingCapacity:
                BotBrain.CurrentState = State.GETH
                return  # walk to home

            else:
                return  # mine

        elif BotBrain.CurrentState == State.GETH:  #################################################
            if player.Position == player.HouseLocation:
                BotBrain.CurrentState = State.UPGR
                return  # upgrade

            else:
                return  # walk to home

        elif BotBrain.CurrentState == State.UPGR:  #################################################
            if player.TotalResources >= neededRSC():
                BotBrain.CurrentState = State.HOME
                return  # buy upgrage

            else:
                BotBrain.CurrentState = State.HOME
                return  # nothing

