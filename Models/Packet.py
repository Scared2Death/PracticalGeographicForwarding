from Models.Centroid import Centroid

class Packet:

    srcId = 0
    srcLocation = None
    destId = 0
    destLocation = None
    message = 'hello'

    __centroid: Centroid = None

    def __init__(self, srcId, srcLocation, destId, destLocation, message):
        self.srcId = srcId
        self.srcLocation = srcLocation
        self.destId = destId
        self.destLocation = destLocation
        self.message = message

    def getCentroid(self):
        return self.__centroid

    def setCentroid(self, centroid):
        self.__centroid = centroid