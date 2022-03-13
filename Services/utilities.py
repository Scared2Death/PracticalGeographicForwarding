from random import seed
from random import randint

from Models.centroid import centroid
from Models.node import node

from Configurations import configuration

class utilities():

    @staticmethod
    def generateNode(maxCentroidX, maxCentroidY, shapeRadius, broadcastRange):
        centroid = utilities.generateCentroid(maxCentroidX, maxCentroidY)

        return node(centroid, shapeRadius, broadcastRange)

    @staticmethod
    def __generateCentroid(maxCentroidX, maxCentroidY):
        seed(1)

        x = randint(0, maxCentroidX)
        y = randint(0, maxCentroidY)

        return centroid(x, y)

    @staticmethod
    def generateBroadcastRange(minRadius, maxRadius):
        return utilities.generateRadius(minRadius, maxRadius)

    @staticmethod
    def generateShapeRadius(minRadius, maxRadius):
        return utilities.generateRadius(minRadius, maxRadius)

    @staticmethod
    def __generateRadius(minRadius, maxRadius):
        seed(1)
        return randint(minRadius, maxRadius)

    @staticmethod
    def changeCentroidPosition(centroid):
        seed(1)

        # nodes can step off the canvas

        centroidXMovement = randint(configuration.MIN_CENTROID_MOVEMENT, configuration.MAX_CENTROID_MOVEMENT)
        centroidYMovement = randint(configuration.MIN_CENTROID_MOVEMENT, configuration.MAX_CENTROID_MOVEMENT)

        centroid.x += centroidXMovement
        centroid.y += centroidYMovement