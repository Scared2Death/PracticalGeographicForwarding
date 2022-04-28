from Models.Centroid import Centroid

class Packet:

    srcId = 0
    srcLocation = None
    destId = 0
    destLocation = None
    message = 'hello'

    __location: Centroid = None

    def __init__(self, srcId, srcLocation, destId, destLocation, message):
        self.srcId = srcId
        self.srcLocation = srcLocation
        self.destId = destId
        self.destLocation = destLocation
        self.message = message

    def __repr__(self):
        return 'Packet (srcId = {}, srcLocation = {}, destId = {}, destLocation = {}, message = {})'.format(self.srcId, self.srcLocation, self.destId, self.destLocation, self.message)

    def getLocation(self):
        return self.__centroid

    def setLocation(self, centroid):
        self.__centroid = centroid