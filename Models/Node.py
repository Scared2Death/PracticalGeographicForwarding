import Services.UtilitiesService as utilitiesService

class Node:

    __centroid = None
    __shapeRadius = None
    __broadcastRange = None
    __nodeType = None

    def __init__(self, centroid, shapeRadius, broadcastRange, nodeType):
        self.__centroid = centroid
        self.__shapeRadius = shapeRadius
        self.__broadcastRange = broadcastRange
        self.__nodeType = nodeType

    def getCentroid(self):
        return self.__centroid

    def setCentroid(self, centroid):
        self.__centroid = centroid

    def getShapeRadius(self):
        return self.__shapeRadius

    def getBroadcastRange(self):
        return self.__broadcastRange

    def getType(self):
        return self.__nodeType

    def getDescription(self):

        centroidPoints = '{},{}'.format(self.__centroid.x, self.__centroid.y)

        descriptionText = 'Centroid: {} Shape Radius: {} Broadcast Range: {} .'.format(centroidPoints, self.__shapeRadius, self.__broadcastRange)
        return descriptionText

    def changePosition(self, otherNodes):
        utilitiesService.UtilitiesService.changeCentroidPosition(self, otherNodes)