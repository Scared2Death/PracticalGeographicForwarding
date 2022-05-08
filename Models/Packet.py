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
    __nak = False

    def __init__(self, srcId, srcLocation, srcCentroid, destId, destLocation,
                 infMode = InfMode.NO_INF, intermediateLocation = None, nak = False):
        self.__srcId = srcId
        self.__srcLocation = srcLocation
        self.__srcCentroid = srcCentroid
        self.__destId = destId
        self.__destLocation = destLocation
        self.__infMode = infMode
        self.__intermediateLocation = intermediateLocation
        self.__nak = nak

    def __repr__(self):
        return 'Packet (srcId = {}, srcLocation = {}, srcCentroid = {}, destId = {}, destLocation = {}, message = {}, intermediateLocation = {}, nak = {})'.format(self.__srcId, self.__srcLocation, self.__srcCentroid, self.__destId, self.__destLocation, self.__message, self.__intermediateLocation, self.__nak)

    def getSrcId(self):
        return self.__srcId

    def getSrcLocation(self):
        return self.__srcLocation

    def getDestId(self):
        return self.__destId

    def getDestLocation(self):
        return self.__destLocation

    def getSrcCentroid(self):
        return self.__srcCentroid

    def getMessage(self):
        return self.__message

    def setInfMode(self, infMode):
        self.__infMode = infMode

    def getInfMode(self):
        return self.__infMode

    def setIntermediateLocation(self, intermediateLocation):
        self.__intermediateLocation = intermediateLocation

    def getIntermediateLocation(self):
        return self.__intermediateLocation

    def setNak(self, nak):
        self.__nak = nak

    def isNak(self):
        return self.__nak