from helper.gamemap import GameMap
from helper.storageHelper import StorageHelper
import json as json_helper
import helper.tile


class BotMap:
    KEY = "Map"
    mapData = {}
    otherHouse = []
    shops = []

    def __init__(self):
        pass

    def addGameMap(self, gameMap, houseLocation):
        for key, value in self.mapData.items():
            value["date"] += 1

        for tile_array in gameMap.tiles:
            for tile in tile_array:
                if tile.TileContent == helper.TileContent.House and tile.Position != houseLocation:
                    print("new other house ", tile.Position)
                    self.otherHouse.append(tile)
                elif tile.TileContent == helper.TileContent.Shop:
                    print("new shop ", tile.Position)
                    self.shops.append(tile)

                self.mapData[tile.Position.__str__()] = {"value": tile.TileContent.value, "date": 0}

        StorageHelper.write(self.KEY, self.mapData)

    def loadMap(self):
        try :
            self.mapData = StorageHelper.read(self.KEY)
            print("length map : ", len(self.mapData))
        except KeyError:
            print("key eroor")
