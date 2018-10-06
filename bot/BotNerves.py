from helper import *

class BotNerves:
    def __init__(self):
        self.next_upgrade = None;

    def mine(self, my_pos, mine_pos):
        return create_collect_action(mine_pos - my_pos)

    def go_mine(self, gameMap, PlayerInfo):
        goal = self._select_mine(gameMap, PlayerInfo)
        return self._move_to(PlayerInfo.Position, goal)

    def go_home(self, PlayerInfo):
        return self._move_to(PlayerInfo.Position, PlayerInfo.HouseLocation)

    def check_if_can_upgrade(self, PlayerInfo):
        self._select_next_upgrade(PlayerInfo)
        return PlayerInfo.TotalRessources > self._next_upgrade_cost(PlayerInfo)

    def purchase_upgrade(self, PlayerInfo):
        self._select_next_upgrade(PlayerInfo)
        return create_upgrade_action(self.next_upgrade)

    def _next_upgrade_cost(self, PlayerInfo):
        return 10000

    def _select_next_upgrade(self, PlayerInfo):
        self.next_upgrade = UpgradeType.CollectingSpeed

    def _select_mine(self, gameMap, PlayerInfo):
        resources = []
        for tile_array in gameMap.tiles:
            for tile in tile_array:
                if tile.TileContent == TileContent.Resource:
                    resources.append(tile.Position)

        myPos = PlayerInfo.Position

        resources.sort(key=lambda x: Point.Distance(myPos, x))

        return resources[0]

    def _move_to(self, myPos, goal):
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
