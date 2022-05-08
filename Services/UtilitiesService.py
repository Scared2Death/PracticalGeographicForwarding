import random
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

        centroid = UtilitiesService.__generateCentroid(Configuration.MAIN_WINDOW_WIDTH, Configuration.MAIN_WINDOW_HEIGHT)
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

        for index, coordinatePair in enumerate(Configuration.INF_NODE_COORDINATES):

            centroid = Centroid(coordinatePair[0], coordinatePair[1])
            shapeRadius = Configuration.INF_NODE_SHAPE_RADIUS

            match index:
                case 0:
                    broadcastRange = Configuration.INF_NODE_1_BROADCASTRANGE
                case 1:
                    broadcastRange = Configuration.INF_NODE_2_BROADCASTRANGE
                case 2:
                    broadcastRange = Configuration.INF_NODE_3_BROADCASTRANGE
                case 3:
                    broadcastRange = Configuration.INF_NODE_4_BROADCASTRANGE
                case 4:
                    broadcastRange = Configuration.INF_NODE_5_BROADCASTRANGE
                case 5:
                    broadcastRange = Configuration.INF_NODE_6_BROADCASTRANGE
                case 6:
                    broadcastRange = Configuration.INF_NODE_7_BROADCASTRANGE

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
    def getMidPoint(centroidOne: Centroid, centroidTwo: Centroid):
        x = (centroidOne.x + centroidTwo.x) / 2
        y = (centroidOne.y + centroidTwo.y) / 2
        return Centroid(x,y)

    @staticmethod
    def getIntermediateLocation(centroidOne: Centroid, centroidTwo: Centroid, radiusRatio):
        radius = UtilitiesService.getCentroidDistance(centroidOne, centroidTwo) * radiusRatio
        midPoint = UtilitiesService.getMidPoint(centroidOne, centroidTwo)
        centerX = midPoint.x
        centerY = midPoint.y
        minX = centerX - radius
        maxX = centerX + radius
        minY = centerY - radius
        maxY = centerY + radius

        output = Centroid(0, 0)
        while True:
            output.x = random.uniform(minX, maxX)
            output.y = random.uniform(minY, maxY)
            if math.sqrt(pow(output.x - centerX, 2) + pow(output.y - centerY, 2)) <= radius:
                return output

    @staticmethod
    def calculateInfExtras(centroidOne: Centroid, centroidTwo: Centroid, radiusRatio):
        radius = UtilitiesService.getCentroidDistance(centroidOne, centroidTwo) * radiusRatio
        midPoint = UtilitiesService.getMidPoint(centroidOne, centroidTwo)
        return {'circle': {'radius': radius, 'center': midPoint}, 'line': {'a': centroidOne, 'b': centroidTwo}}

    @staticmethod
    def delayExecution(timeInterval):
        time.sleep(timeInterval)