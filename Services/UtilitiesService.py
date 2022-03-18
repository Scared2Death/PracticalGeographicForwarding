import math

from random import randint

from Models.Centroid import Centroid
from Models.Node import Node

from Configurations import Configuration
from Constants import NodeType

class UtilitiesService:

    @staticmethod
    def generateNode():

        centroid = UtilitiesService.__generateCentroid(Configuration.GUI_WINDOW_WIDTH, Configuration.GUI_WINDOW_HEIGHT)
        shapeRadius = UtilitiesService.__generateShapeRadius(Configuration.SHAPE_RADIUS, Configuration.SHAPE_RADIUS)
        broadcastRange = UtilitiesService.__generateBroadcastRange(Configuration.MIN_BROADCAST_RANGE, Configuration.MAX_BROADCAST_RANGE)
        nodeType = UtilitiesService.__getNodeType()

        return Node(centroid, shapeRadius, broadcastRange, nodeType)

    @staticmethod
    def __generateCentroid(maxCentroidX, maxCentroidY):

        cropValue = Configuration.GUI_CANVAS_CROP_PERCENTAGE / 100

        lowerBoundaryCoefficient = (0 + cropValue)
        upperBoundaryCoefficient = (1 - cropValue)

        x = randint(maxCentroidX * lowerBoundaryCoefficient, maxCentroidX * upperBoundaryCoefficient)
        y = randint(maxCentroidY * lowerBoundaryCoefficient, maxCentroidY * upperBoundaryCoefficient)

        return Centroid(x, y)

    @staticmethod
    def changeCentroidPosition(node: Node):

        # nodes can step off the canvas

        centroidXMovement = randint(Configuration.MIN_CENTROID_MOVEMENT, Configuration.MAX_CENTROID_MOVEMENT)
        centroidYMovement = randint(Configuration.MIN_CENTROID_MOVEMENT, Configuration.MAX_CENTROID_MOVEMENT)

        node.getCentroid().x += centroidXMovement
        node.getCentroid().y += centroidYMovement

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
    def getDistance(nodeOne: Node, nodeTwo: Node):
        return math.sqrt(pow(nodeOne.getCentroid().x - nodeTwo.getCentroid().x, 2) + pow(nodeOne.getCentroid().y - nodeTwo.getCentroid().y, 2))