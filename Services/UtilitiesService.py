from random import randint

from Models.Centroid import Centroid
from Models.Node import Node

from Configurations import Configuration
from Constants import NodeType

import math
import time

class UtilitiesService:

    @staticmethod
    def generateNode():

        centroid = UtilitiesService.__generateCentroid(Configuration.GUI_WINDOW_WIDTH, Configuration.GUI_WINDOW_HEIGHT)
        shapeRadius = UtilitiesService.__generateShapeRadius(Configuration.NODE_SHAPE_RADIUS, Configuration.NODE_SHAPE_RADIUS)
        broadcastRange = UtilitiesService.__generateBroadcastRange(Configuration.MIN_BROADCAST_RANGE, Configuration.MAX_BROADCAST_RANGE)
        nodeType = UtilitiesService.__getNodeType()
        nodeId = Configuration.BASE_NODE_ID
        # probably not a great idea
        Configuration.BASE_NODE_ID += 1

        return Node(centroid, shapeRadius, broadcastRange, nodeType, nodeId)

    @staticmethod
    def generateINFNodes():

        infNodes : {int: Node} = {}
        for coordinatePair in Configuration.INF_NODE_COORDINATES:

            centroid = Centroid(coordinatePair[0], coordinatePair[1])
            shapeRadius = Configuration.INF_NODE_SHAPE_RADIUS
            broadcastRange = Configuration.INF_NODE_BROADCAST_RANGE_RADIUS
            nodeType = NodeType.LOCATION_AWARE
            nodeId = Configuration.BASE_NODE_ID

            infNode = Node(centroid, shapeRadius, broadcastRange, nodeType, nodeId)

            infNodes[nodeId] = infNode

            Configuration.BASE_NODE_ID += 1

        return infNodes

    @staticmethod
    def __generateCentroid(maxCentroidX, maxCentroidY):

        cropValue = Configuration.GUI_CANVAS_CROP_PERCENTAGE / 100

        lowerBoundaryCoefficient = (0 + cropValue)
        upperBoundaryCoefficient = (1 - cropValue)

        x = randint(maxCentroidX * lowerBoundaryCoefficient, maxCentroidX * upperBoundaryCoefficient)
        y = randint(maxCentroidY * lowerBoundaryCoefficient, maxCentroidY * upperBoundaryCoefficient)

        return Centroid(x, y)

    @staticmethod
    def changeCentroidPosition(node: Node, otherNodes: list[Node]):

        for x in range(Configuration.NUMBER_OF_MAXIMUM_MOVEMENT_TRIAL_PER_NODE):

            couldMakeAMovement = True

            # nodes can step off the canvas

            centroidXMovement = randint(Configuration.MIN_CENTROID_MOVEMENT, Configuration.MAX_CENTROID_MOVEMENT)
            centroidYMovement = randint(Configuration.MIN_CENTROID_MOVEMENT, Configuration.MAX_CENTROID_MOVEMENT)

            wouldBeCreatedCentroidX = node.getCentroid().x + centroidXMovement
            wouldBeCreatedCentroidY = node.getCentroid().y + centroidYMovement
            wouldBeCreatedCentroid = Centroid(wouldBeCreatedCentroidX, wouldBeCreatedCentroidY)

            for otherNode in otherNodes:
                if (node == otherNode):
                    continue

                distance = UtilitiesService.getCentroidDistance(wouldBeCreatedCentroid, otherNode.getCentroid())

                if distance < Configuration.MINIMUM_NODES_DISTANCE:
                    couldMakeAMovement = False
                    break

            if (couldMakeAMovement):
                node.getCentroid().x = wouldBeCreatedCentroidX
                node.getCentroid().y = wouldBeCreatedCentroidY
                break

    @staticmethod
    def __generateShapeRadius(minRadius, maxRadius):
        return UtilitiesService.__generateRadius(minRadius, maxRadius)

    @staticmethod
    def __generateBroadcastRange(minRadius, maxRadius):
        return UtilitiesService.__generateRadius(minRadius, maxRadius)

    @staticmethod
    def __generateRadius(minRadius, maxRadius):
        return randint(minRadius, maxRadius)

    @staticmethod
    def __getNodeType():
        generatedRandomInt = UtilitiesService.generateRandomInt(1, 100)

        if generatedRandomInt <= Configuration.RATIO_OF_LOCATION_AWARE_NODES:
            return NodeType.LOCATION_AWARE
        else:
            return NodeType.LOCATION_IGNORANT

    @staticmethod
    def generateRandomInt(minValue, maxValue):
        return randint(minValue, maxValue)

    @staticmethod
    def getNodeDistance(nodeOne: Node, nodeTwo: Node):
        return math.sqrt(pow(nodeOne.getCentroid().x - nodeTwo.getCentroid().x, 2) + pow(nodeOne.getCentroid().y - nodeTwo.getCentroid().y, 2))

    @staticmethod
    def getCentroidDistance(centroidOne: Centroid, centroidTwo: Centroid):
        return math.sqrt(pow(centroidOne.x - centroidTwo.x, 2) + pow(centroidOne.y - centroidTwo.y, 2))

    @staticmethod
    def checkNodeIntersection(nodeOne: Node, nodeTwo: Node):

        centroidDistance = UtilitiesService.getCentroidDistance(nodeOne.getCentroid(), nodeTwo.getCentroid())
        hasIntersection = centroidDistance < (nodeOne.getBroadcastRange() + nodeTwo.getBroadcastRange())

        return hasIntersection

    @staticmethod
    def delayExecution(timeInterval):
        time.sleep(timeInterval)