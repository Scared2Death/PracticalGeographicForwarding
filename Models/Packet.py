class Packet:

    __srcId = 0
    __srcLocation = None
    __srcCentroid = None
    __destId = 0
    __destLocation = None
    __message = 'hello'

    def __init__(self, srcId, srcLocation, srcCentroid, destId, destLocation, message):
        self.srcId = srcId
        self.srcLocation = srcLocation
        self.srcCentroid = srcCentroid
        self.destId = destId
        self.destLocation = destLocation
        self.message = message

    def __repr__(self):
        return 'Packet (srcId = {}, srcLocation = {}, srcCentroid = {}, destId = {}, destLocation = {}, message = {})'.format(self.srcId, self.srcLocation, self.srcCentroid, self.destId, self.destLocation, self.message)