from helper import *
from .pathFinder import astar

DANGER_ZONE = 3

class BotNerves:

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

        return PlayerInfo.Position.Distance(BotNerves.closest_enemy) < DANGER_ZONE

    @staticmethod
    def _next_upgrade_cost(PlayerInfo):
        return 10000

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

        resources.sort(key=lambda x: Point.Distance(myPos, x))

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
        chemin = astar(gameMap,myPos, goal)

        return chemin[1] - chemin[0]

