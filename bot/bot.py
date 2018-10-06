from helper import *
from bot.BotBrain import *
import math
from .pathFinder import astar
from . BotMap import BotMap


class Bot:
    def __init__(self):
        self.brain = BotBrain
        self.botMap = BotMap()
        self.PlayerInfo = None

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.botMap.loadMap()
        self.PlayerInfo = playerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        self.botMap.addGameMap(gameMap, self.PlayerInfo.HouseLocation)
        self.brain.nextPhase(self.PlayerInfo, gameMap)
        print(self.brain.CurrentState)
        return self.brain.DoSomeThing(self.PlayerInfo, gameMap)
        
    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
