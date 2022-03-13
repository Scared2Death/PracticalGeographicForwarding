from Models.centroid import centroid

from Services.utilities import utilities

class node():

    __centroid = None
    __shapeRadius = None
    __broadcastRange = None

    def __init__(self, centroid, shapeRadius, broadcastRange):
        self.centroid = centroid
        self.shapeRadius = shapeRadius
        self.broadcastRange = broadcastRange

    def getDescription(self):

        centroidPoints = '{},{}'.format(self.centroid.x, self.centroid.y)

        descriptionText = 'Centroid: {} Shape Radius: {} BroadcastRange{} .'.format(centroidPoints, self.shapeRadius, self.broadcastRange)
        return descriptionText

    def changePosition(self):
        utilities.changeCentroidPosition(self)