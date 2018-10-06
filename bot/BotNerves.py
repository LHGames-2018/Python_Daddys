from helper import *

class BotNerves:


    def mine(self, my_pos, mine_pos):
        return create_collect_action(mine_pos - my_pos)

    def go_mine(self, gameMap, PlayerInfo):
        goal = self.__select_mine__(gameMap, PlayerInfo)
        return self.__move_to__(PlayerInfo.Position, goal)

    def go_home(selfself, PlayerInfo):
        return self.__move_to__(PlayerInfo.Position, PlayerInfo.HouseLocation)

    def __select_mine__(self, gameMap, PlayerInfo):
        resources = []
        for tile_array in gameMap.tiles:
            for tile in tile_array:
                if tile.TileContent == TileContent.Resource:
                    resources.append(tile.Position)

        myPos = PlayerInfo.Position

        resources.sort(key=lambda x: Point.Distance(myPos, x))

        return resources[0]

    def __move_to__(self, myPos, goal):
        if myPos.y != goal.y:
            if myPos.y - goal.y > 0:
                return create_move_action(Point(0, -1))
            else:
                return create_move_action(Point(0, 1))
        else:
            if myPos.x - goal.x > 0:
                return create_move_action(Point(-1, 0))
            else:
                return create_move_action(Point(1, 0))
