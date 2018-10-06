from helper import *
import math

class Bot:
    def __init__(self):
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """

        def move_to_goal(myPos, goal):
                if myPos.x == goal.x:
                    if myPos.y - goal.y > 0:
                        return create_move_action(Point(0, -1))
                    else:
                        return create_move_action(Point(0, 1))
                else:
                    if myPos.x - goal.x > 0:
                        return create_move_action(Point(-1, 0))
                    else:
                        return create_move_action(Point(1, 0))

        if self.PlayerInfo.CarriedRessources == self.PlayerInfo.CarryingCapacity:
            return move_to_goal(self.PlayerInfo.Position, self.PlayerInfo.HouseLocation)
        else:
            ressources = []
            for tile_array in gameMap.tiles:
                for tile in tile_array:
                    if tile.TileContent == TileContent.Ressource:
                        ressources.append(tile.position)
            
            myPos = self.PlayerInfo.Position


            ressources.sort(key = lambda x: Point.distance(myPos,x))

            goal = ressources[0]

            if Point.distance(myPos, goal) == 1:
                return create_collect_action(goal - myPos)
            else:    
                return move_to_goal(myPos, goal)



        # Write your bot here. Use functions from aiHelper to instantiate your actions.
        return create_move_action(Point(0, 1))

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
