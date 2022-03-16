from random import seed
from random import randint

from Models.centroid import centroid
from Models.node import node

from Configurations import configuration

class utilities():

    @staticmethod
    def generateNode():

        centroid = utilities.__generateCentroid(
            configuration.GUI_WINDOW_WIDTH,
            configuration.GUI_WINDOW_HEIGHT
        )
        shapeRadius = utilities.__generateShapeRadius(configuration.MIN_SHAPE_RADIUS, configuration.MAX_SHAPE_RADIUS)
        broadcastRange = utilities.__generateBroadcastRange(configuration.MIN_BROADCAST_RANGE, configuration.MAX_BROADCAST_RANGE)

        return node(centroid, shapeRadius, broadcastRange)

    @staticmethod
    def __generateCentroid(maxCentroidX, maxCentroidY):

        x = randint(100, maxCentroidX - 200)
        y = randint(100, maxCentroidY - 200)

        return centroid(x, y)

    @staticmethod
    def __generateBroadcastRange(minRadius, maxRadius):
        return utilities.__generateRadius(minRadius, maxRadius)

    @staticmethod
    def __generateShapeRadius(minRadius, maxRadius):
        return utilities.__generateRadius(minRadius, maxRadius)

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