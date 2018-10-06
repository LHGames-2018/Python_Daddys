from helper import *
from bot.BotBrain import *


class Bot:
    def __init__(self):
        self.brain = BotBrain

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo
        self.brain.nextPhase(self.PlayerInfo)
        print(self.brain.CurrentState)


    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """

        return self.brain.DoSomeThing(self.PlayerInfo, gameMap)


    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
