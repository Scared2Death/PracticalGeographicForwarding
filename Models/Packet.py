from Constants import InfMode

class Packet:

    __srcId = 0
    __srcLocation = None
    __srcCentroid = None
    __destId = 0
    __destLocation = None
    __message = 'hello'
    __infMode = InfMode.NO_INF
    __intermediateLocation = None
    # todo: NakPackage class
    __nak = False

    def __init__(self, srcId, srcLocation, srcCentroid, destId, destLocation, message):
        self.srcId = srcId
        self.srcLocation = srcLocation
        self.srcCentroid = srcCentroid
        self.destId = destId
        self.destLocation = destLocation
        self.message = message

    def __repr__(self):
        return 'Packet (srcId = {}, srcLocation = {}, srcCentroid = {}, destId = {}, destLocation = {}, message = {})'.format(self.srcId, self.srcLocation, self.srcCentroid, self.destId, self.destLocation, self.message)

    def setInfMode(self, infMode):
        self.__infMode = infMode

    def getInfMode(self):
        return self.__infMode

    def setIntermediateLocation(self, intermediateLocation):
        self.__intermediateLocation = intermediateLocation

    def getIntermediateLocation(self):
        return self.__intermediateLocation

    def getDestLocation(self):
        return self.__destLocation

    def setNak(self, nak):
        self.__nak = nak

    def isNak(self):
        return self.__nak