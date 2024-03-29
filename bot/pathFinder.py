from enum import Enum
from helper.structs import Point
from helper.tile import TileContent

class Node:
    def __init__(self, parent=None, position=None, tileType=None):
        self.parent = parent
        self.position = position

        self.g = 0  # Distance entre le noeud courant et la position de départ
        self.h = 0  # H is the heuristic — estimated distance from the current node to the end node.
        self.f = 0  # Coût total du noeud

    def __eq__(self, other):
        return self.position == other.position


def astar(map, start, goal):
    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0

    goalNode = Node(None, goal)
    goalNode.g = goalNode.h = goalNode.f = 0

    openList = []
    closedList = []

    openList.append(startNode)

    while len(openList) > 0:
        currentNode = openList[0]
        currentIndex = 0

        for index, item in enumerate(openList):
            if item.f < currentNode.f:  # prochain noeud qui à le plus petit coût
                currentNode = item
                currentIndex = index

        openList.pop(currentIndex)
        closedList.append(currentNode)

        if currentNode == goalNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            cost = 0
            for pos in path[::-1]:
                if pos == start or pos == goal:
                    continue

                if map.getTileAt(pos) == TileContent.Wall:
                    cost += 5
                else:
                    cost += 1
            return path[::-1], cost  # Return reversed path

        children = []
        for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Carrés adajacents
            # Get node position
            nodePosition = Point(currentNode.position.x + newPosition[0], currentNode.position.y + newPosition[1])

            # Si c'est une tuile marchable (lave et ressources, peut-être les maisons des autres joueurs?)

            currentContent = map.getTileAt(Point(nodePosition.x, nodePosition.y))
            if currentContent == TileContent.Lava:
                continue
            # ne prends pas en compte les tuiles de ressources sauf si c'est le but
            if currentContent == TileContent.Resource and nodePosition != goal:
                continue
            if currentContent == TileContent.House and nodePosition != goal:
                continue
            # Check if node is already in list
            if Node(currentNode, nodePosition) in closedList:
                continue
            # Create new node
            newNode = Node(currentNode, nodePosition)

            # Append
            children.append(newNode)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closedChild in closedList:
                if child == closedChild:
                    continue

            # Create the f, g, and h values
            child.g = currentNode.g + 1
            child.h = ((child.position.x - goalNode.position.x) ** 2) + ((child.position.y - goalNode.position.y) ** 2)
            child.f = child.g + child.h

            # Ajout du poids des objets brisables
            if map.getTileAt(Point(child.position.x, child.position.y)) == TileContent.Wall:
                child.f += 5

            # Child is already in the open list
            for openNode in openList:
                if child == openNode and child.g > openNode.g:
                    continue


            # Add the child to the open list
            openList.append(child)