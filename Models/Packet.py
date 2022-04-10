class Packet:

    srcId = 0
    srcLocation = None
    destId = 0
    destLocation = None
    message = 'hello'

    def __init__(self, srcId, srcLocation, destId, destLocation, message):
        self.srcId = srcId
        self.srcLocation = srcLocation
        self.destId = destId
        self.destLocation = destLocation
        self.message = message
