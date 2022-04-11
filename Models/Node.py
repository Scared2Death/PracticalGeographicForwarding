import Constants.NodeType
import Services.UtilitiesService as utilitiesService

class Node:

    __centroid = None
    __shapeRadius = None
    __broadcastRange = None
    __nodeType = None
    __nodeId = None
    __routingTable = None
    __seqNum = 0

    def __init__(self, centroid, shapeRadius, broadcastRange, nodeType, nodeId):
        self.__centroid = centroid
        self.__shapeRadius = shapeRadius
        self.__broadcastRange = broadcastRange
        self.__nodeType = nodeType
        self.__nodeId = nodeId
        self.__routingTable = {self.__nodeId: {'cost': 0, 'nextHop': None, 'seqNum': 0, 'location': centroid}}
        if nodeType == Constants.NodeType.LOCATION_AWARE:
            self.__routingTable[self.__nodeId]['location'] = centroid

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

    def getId(self):
        return self.__nodeId

    def getRoutingTable(self):
        return self.__routingTable

    def getDescription(self):

        centroidPoints = '{},{}'.format(self.__centroid.x, self.__centroid.y)

        descriptionText = 'Centroid: {} Shape Radius: {} Broadcast Range: {} .'.format(centroidPoints, self.__shapeRadius, self.__broadcastRange)
        return descriptionText

    def changePosition(self, otherNodes):
        utilitiesService.UtilitiesService.changeCentroidPosition(self, otherNodes)

    # Returns true if routing table is updated, false otherwise
    def processRoutingTableUpdate(self, message):
        updated = False
        sender = message['origin']
        routingTable = message['table']
        seqNum = message['seqNum']
        # If the sender is not in the routing table, it means that sender is out of range for self,
        # so self cannot send anything via the sender
        if sender.getId() in self.__routingTable:
            cost = self.__routingTable[sender.getId()]['cost']
            self.__routingTable[sender.getId()]['seqNum'] = seqNum
            # Iterate through the received routing table
            for dest, data in routingTable.items():
                if dest in self.__routingTable:
                    # Update this routing table
                    if cost + data['cost'] < self.__routingTable[dest]['cost']:
                        self.updateEntry(dest, cost + data['cost'], sender, data['seqNum'], data['location'])
                        updated = True
                    else:
                        updated = updated or False
                else:
                    # Save new entry
                    self.saveNewEntry(dest, cost + data['cost'], sender, data['seqNum'], data['location'])
                    updated = True
        return updated

    def saveNewEntry(self, key, cost, nextHop, seqNum, location):
        self.__routingTable[key] = {'cost': cost, 'nextHop': nextHop.getId(), 'seqNum': seqNum, 'location': location}

    def updateEntry(self, key, cost, nextHop, seqNum, location):
        self.__routingTable[key]['cost'] = cost
        self.__routingTable[key]['nextHop'] = nextHop.getId()
        self.__routingTable[key]['seqNum'] = seqNum
        self.__routingTable[key]['location'] = location

    def getSeqNum(self):
        self.__seqNum += 1
        return self.__seqNum

    def getBasicNextHop(self, packet):
        dest = packet.destId
        if self.__routingTable is None:
            return None
        elif dest in self.__routingTable:
            print('Found destination in Routing Table.')
            return self.__routingTable[dest]['nextHop']
        else:
            print('Trying to find closer node...')
            location = packet.destLocation
            distance = utilitiesService.UtilitiesService.getCentroidDistance(location, self.getCentroid())
            nextHop = None
            for nodeId, data in self.__routingTable.items():
                newDistance = utilitiesService.UtilitiesService.getCentroidDistance(location, data['location'])
                if newDistance < distance:
                    distance = newDistance
                    nextHop = data['nextHop']
                    print('id {} is closer'.format(nodeId))
                else:
                    print('id {} is not closer'.format(nodeId))
            return nextHop