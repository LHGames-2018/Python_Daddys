from helper import *
from .pathFinder import astar

DANGER_ZONE = 8
LEVEL_COST = [10000,15000,25000,50000,100000]

class BotNerves:

    upgrade_order = [4, 4, 1, 4, 2, 1, 4]
    next_upgrade = None
    closest_mine = None
    closest_enemy = None

    @staticmethod
    def mine(PlayerInfo):
        return create_collect_action(BotNerves.closest_mine - PlayerInfo.Position)

    @staticmethod
    def go_mine(gameMap, PlayerInfo):
        BotNerves._select_mine(gameMap, PlayerInfo)
        return BotNerves._move_to(PlayerInfo.Position, BotNerves.closest_mine, gameMap)

    @staticmethod
    def go_home(PlayerInfo, gameMap):
        return BotNerves._move_to(PlayerInfo.Position, PlayerInfo.HouseLocation, gameMap)

    @staticmethod
    def go_mrdr(PlayerInfo, gameMap):
        return BotNerves._move_to(PlayerInfo.Position, PlayerInfo.Position + Point(0,4), gameMap)

    @staticmethod
    def go_enemy(gameMap, PlayerInfo):
        BotNerves._update_closest_enemy(gameMap, PlayerInfo)
        return BotNerves._move_to(PlayerInfo.Position, BotNerves.closest_enemy, gameMap)

    @staticmethod
    def check_if_can_upgrade(PlayerInfo):
        BotNerves._select_next_upgrade(PlayerInfo)
        return PlayerInfo.TotalResources > BotNerves._next_upgrade_cost(PlayerInfo)

    @staticmethod
    def purchase_upgrade(PlayerInfo):
        return create_upgrade_action(BotNerves.next_upgrade)

    @staticmethod
    def nextToMineral(gameMap, PlayerInfo):
        BotNerves._select_mine(gameMap, PlayerInfo)
        point = [Point(0,1), Point(0.-1), Point(1,0), Point(-1,0)]
        return [x + BotNerves.closest_mine for x in point]

    @staticmethod
    def nextToEnemy(gameMap, PlayerInfo):
        BotNerves._update_closest_enemy(gameMap, PlayerInfo)
        if BotNerves.closest_enemy is None:
            return False

        point = [Point(0,1), Point(0.-1), Point(1,0), Point(-1,0)]
        return PlayerInfo.Position in [x + BotNerves.closest_enemy for x in point]

    @staticmethod
    def attack(PlayerInfo, gameMap):
        return create_attack_action(BotNerves._get_direction(PlayerInfo.Position, BotNerves.closest_enemy, gameMap))

    @staticmethod
    def is_near_enemy(gameMap, PlayerInfo):
        BotNerves._update_closest_enemy(gameMap, PlayerInfo)
        if BotNerves.closest_enemy is None:
            return False

        return Point.Distance(PlayerInfo.Position, BotNerves.closest_enemy) < DANGER_ZONE

    @staticmethod
    def _next_upgrade_cost(PlayerInfo):
        return LEVEL_COST[PlayerInfo.getUpgradeLevel(BotNerves.next_upgrade)]

    @staticmethod
    def _select_next_upgrade(PlayerInfo):
        BotNerves.next_upgrade = UpgradeType.CollectingSpeed

    @staticmethod
    def _update_closest_enemy(gameMap, PlayerInfo):
        enemies = []
        myPos = PlayerInfo.Position

        for tile_array in gameMap.tiles:
            for tile in tile_array:
                if tile.TileContent == TileContent.Player and tile.Position != myPos:
                    enemies.append(tile.Position)

        enemies.sort(key=lambda x: Point.Distance(myPos, x))

        BotNerves.closest_enemy = enemies[0] if len(enemies) > 0 else None

    @staticmethod
    def _select_mine(gameMap, PlayerInfo):
        resources = []
        for tile_array in gameMap.tiles:
            for tile in tile_array:
                if tile.TileContent == TileContent.Resource:
                    resources.append(tile.Position)

        myPos = PlayerInfo.Position

        def get_score(x):
            _, score = astar(gameMap,myPos, x)
            return score

        resources.sort(key=get_score)

        BotNerves.closest_mine =  resources[0]

    @staticmethod
    def _move_to(myPos, goal, gameMap):
        direction = BotNerves._get_direction(myPos, goal, gameMap)
        type = gameMap.getTileAt(myPos + direction)
        if type == TileContent.Wall:
            return create_attack_action(direction)
        elif type == TileContent.Resource:
            return create_collect_action(direction)
        else:
            return  create_move_action(direction)

    @staticmethod
    def _get_direction(myPos, goal, gameMap):
        chemin, score = astar(gameMap,myPos, goal)

        return chemin[1] - chemin[0]

    @staticmethod
    def determine_next_upgrade(PlayerInfo):
        return BotNerves.upgrade_order[sum(PlayerInfo)]
