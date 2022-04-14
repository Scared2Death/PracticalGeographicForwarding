import Constants.NodeType
import Services.UtilitiesService as utilitiesService
from Configurations import Configuration

class Node:

    __centroid = None
    __shapeRadius = None
    __broadcastRange = None
    __nodeType = None
    __nodeId = None
    __routingTable = None
    __seqNum = 0
    __proxy = None
    __radius = 0

    def __init__(self, centroid, shapeRadius, broadcastRange, nodeType, nodeId):
        self.__centroid = centroid
        self.__shapeRadius = shapeRadius
        self.__broadcastRange = broadcastRange
        self.__nodeType = nodeType
        self.__nodeId = nodeId
        self.__routingTable = {Constants.NodeType.LOCATION_AWARE: {}, Constants.NodeType.LOCATION_IGNORANT: {}}
        self.__routingTable[nodeType][nodeId] = {'cost': 0, 'nextHop': None, 'seqNum': 0, 'location': None, 'radius': 0}
        if nodeType == Constants.NodeType.LOCATION_AWARE:
            self.__routingTable[Constants.NodeType.LOCATION_AWARE][nodeId]['location'] = centroid

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

    def getSeqNum(self):
        return self.__seqNum

    def incrementSeqNum(self):
        self.__seqNum += 1
        self.__routingTable[self.__nodeType][self.__nodeId]['seqNum'] = self.__seqNum

    def getLocation(self):
        return self.__centroid if self.__nodeType == Constants.NodeType.LOCATION_AWARE else None

    def getRadius(self):
        return self.__radius

    def getDescription(self):

        centroidPoints = '{},{}'.format(self.__centroid.x, self.__centroid.y)

        descriptionText = 'Centroid: {} Shape Radius: {} Broadcast Range: {} .'.format(centroidPoints, self.__shapeRadius, self.__broadcastRange)
        return descriptionText

    def changePosition(self, otherNodes):
        utilitiesService.UtilitiesService.changeCentroidPosition(self, otherNodes)

    def saveNewEntry(self, nodeType, key, cost, nextHopId, seqNum, location, radius):
        self.__routingTable[nodeType][key] = {'cost': cost, 'nextHop': nextHopId, 'seqNum': seqNum, 'location': location, 'radius': radius}

    def updateEntry(self, nodeType, key, cost, nextHopId, seqNum, location, radius):
        self.__routingTable[nodeType][key]['cost'] = cost
        self.__routingTable[nodeType][key]['nextHop'] = nextHopId
        self.__routingTable[nodeType][key]['seqNum'] = seqNum
        self.__routingTable[nodeType][key]['location'] = location
        self.__routingTable[nodeType][key]['radius'] = radius

    # Returns true if routing table is updated, false otherwise
    def processBasicRoutingTableUpdate(self, message):
        updated = False
        senderId = message['origin']
        routingTable = message['table']

        for nodeType, table in routingTable.items():
            for dest, data in table.items():
                newCost = data['cost'] + 1
                newSeqNum = data['seqNum']
                newLocation = data['location']
                newRadius = data['radius']

                inRoutingTable = dest in self.__routingTable[nodeType]
                notSelf = dest != self.__nodeId

                if inRoutingTable and notSelf:
                    currentSeqNum = self.__routingTable[nodeType][dest]['seqNum']
                    currentCost = self.__routingTable[nodeType][dest]['cost']

                    if newSeqNum > currentSeqNum:
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        updated = True
                    elif newSeqNum == currentSeqNum and newCost < currentCost:
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        updated = True
                    else:
                        updated = updated or False
                elif newCost <= Configuration.MAX_HOPS and notSelf:
                    # Save new entry if it is within the max hop count
                    self.saveNewEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                    updated = True
        return updated

    def getBasicNextHop(self, packet):
        dest = packet.destId
        if self.__routingTable is None:
            return None
        elif dest in self.__routingTable[Constants.NodeType.LOCATION_AWARE]:
            print('Found destination in Routing Table.')
            return self.__routingTable[Constants.NodeType.LOCATION_AWARE][dest]['nextHop']
        elif dest in self.__routingTable[Constants.NodeType.LOCATION_IGNORANT]:
            print('Found destination in Routing Table.')
            return self.__routingTable[Constants.NodeType.LOCATION_IGNORANT][dest]['nextHop']
        elif self.getLocation() is not None:
            print('Trying to find node in the routing table that is physically closer to the destination...')
            location = packet.destLocation
            distance = utilitiesService.UtilitiesService.getCentroidDistance(location, self.getLocation())
            nextHop = None
            # Only location aware nodes can be used
            for nodeId, data in self.__routingTable[Constants.NodeType.LOCATION_AWARE].items():
                newDistance = utilitiesService.UtilitiesService.getCentroidDistance(location, data['location'])
                if newDistance < distance:
                    distance = newDistance
                    nextHop = data['nextHop']
                    print('id {} is closer'.format(nodeId))
                else:
                    print('id {} is not closer'.format(nodeId))
            return nextHop
        else:
            return None

    def processLocProxyRoutingTableUpdate(self, message):
        updated = False
        senderId = message['origin']
        routingTable = message['table']

        for nodeType, table in routingTable.items():
            for dest, data in table.items():
                newCost = data['cost'] + 1
                newSeqNum = data['seqNum']
                newLocation = data['location']
                newRadius = data['radius'] if data['radius'] == 0 else data['radius'] - 1
                inRoutingTable = dest in self.__routingTable[nodeType]
                # Save new entry if it is within the max hop count / save all location aware nodes / save entries with non zero radius
                mustSave = newCost <= Configuration.MAX_HOPS or nodeType == Constants.NodeType.LOCATION_AWARE or newRadius != 0
                notSelf = dest != self.__nodeId

                if inRoutingTable and notSelf:
                    currentSeqNum = self.__routingTable[nodeType][dest]['seqNum']
                    currentCost = self.__routingTable[nodeType][dest]['cost']
                    if newSeqNum > currentSeqNum:
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        updated = True
                    elif newSeqNum == currentSeqNum and newCost < currentCost:
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        updated = True
                    else:
                        updated = updated or False
                elif inRoutingTable and mustSave and notSelf:
                    self.saveNewEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                    updated = True
                self.setProxy(nodeType, newLocation, newCost)
            return updated

    def setProxy(self, nodeType, proxyLocation, radius):
        if  nodeType == Constants.NodeType.LOCATION_AWARE and self.__nodeType == Constants.NodeType.LOCATION_IGNORANT and (self.__proxy is None or self.__radius > radius):
            self.__proxy = proxyLocation
            self.__radius = radius