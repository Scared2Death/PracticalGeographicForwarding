import math

from random import seed
from random import randint

from Models.centroid import centroid
from Models.node import node

from Configurations import configuration

class utilitiesService():

    @staticmethod
    def generateNode():

        centroid = utilitiesService.__generateCentroid(
            configuration.GUI_WINDOW_WIDTH,
            configuration.GUI_WINDOW_HEIGHT
        )
        shapeRadius = utilitiesService.__generateShapeRadius(configuration.SHAPE_RADIUS, configuration.SHAPE_RADIUS)
        broadcastRange = utilitiesService.__generateBroadcastRange(configuration.MIN_BROADCAST_RANGE, configuration.MAX_BROADCAST_RANGE)

        return node(centroid, shapeRadius, broadcastRange)

    @staticmethod
    def __generateCentroid(maxCentroidX, maxCentroidY):

        cropValue = configuration.GUI_CANVAS_CROP_PERCENTAGE / 100

        lowerBoundaryCoefficient = (0 + cropValue)
        upperBoundaryCoefficient = (1 - cropValue)

        x = randint(maxCentroidX * lowerBoundaryCoefficient, maxCentroidX * upperBoundaryCoefficient)
        y = randint(maxCentroidY * lowerBoundaryCoefficient, maxCentroidY * upperBoundaryCoefficient)

        return centroid(x, y)

    @staticmethod
    def __generateBroadcastRange(minRadius, maxRadius):
        return utilitiesService.__generateRadius(minRadius, maxRadius)

    @staticmethod
    def __generateShapeRadius(minRadius, maxRadius):
        return utilitiesService.__generateRadius(minRadius, maxRadius)

    @staticmethod
    def __generateRadius(minRadius, maxRadius):
        return randint(minRadius, maxRadius)

    @staticmethod
    def changeCentroidPosition(centroid):

        # nodes can step off the canvas

        centroidXMovement = randint(configuration.MIN_CENTROID_MOVEMENT, configuration.MAX_CENTROID_MOVEMENT)
        centroidYMovement = randint(configuration.MIN_CENTROID_MOVEMENT, configuration.MAX_CENTROID_MOVEMENT)

        centroid.x += centroidXMovement
        centroid.y += centroidYMovement

    @staticmethod
    def generateRandomInt(minValue, maxValue):
        return randint(minValue, maxValue)

    @staticmethod
    def getDistance(nodeOne: node, nodeTwo: node):

        return math.sqrt(pow(nodeOne.centroid.x - nodeTwo.centroid.x, 2) + pow(nodeOne.centroid.y - nodeTwo.centroid.y, 2))