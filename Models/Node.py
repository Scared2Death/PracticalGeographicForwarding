import Services.UtilitiesService as utilitiesService

from Constants import NodeType
from Services.LogService import LogService
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
    __proxyId = None
    __radius = 0

    def __init__(self, centroid, shapeRadius, broadcastRange, nodeType, nodeId):
        self.__centroid = centroid
        self.__shapeRadius = shapeRadius
        self.__broadcastRange = broadcastRange
        self.__nodeType = nodeType
        self.__nodeId = nodeId
        self.__routingTable = {NodeType.LOCATION_AWARE: {}, NodeType.LOCATION_IGNORANT: {}}
        self.__routingTable[nodeType][nodeId] = {'cost': 0, 'nextHop': None, 'seqNum': 0, 'location': None, 'radius': 0}
        if nodeType == NodeType.LOCATION_AWARE:
            self.__routingTable[NodeType.LOCATION_AWARE][nodeId]['location'] = centroid

    def __repr__(self):
        if self.__nodeType == NodeType.LOCATION_IGNORANT:
            return 'Node (id = {}, type = {}, proxyLocation = {}, proxy = {}, seqNum = {})'.format(self.__nodeId, self.__nodeType, self.getLocation(), self.__proxyId, self.__seqNum)
        else:
            return 'Node (id = {}, type = {}, location = {}, seqNum = {})'.format(self.__nodeId, self.__nodeType, self.getLocation(), self.__seqNum)

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

    def isLocationAware(self):
        return self.__nodeType == NodeType.LOCATION_AWARE

    def isLocationIgnorant(self):
        return self.__nodeType == NodeType.LOCATION_IGNORANT

    def getId(self):
        return self.__nodeId

    def getRoutingTable(self):
        return self.__routingTable

    def setRoutingTable(self, table):
        self.__routingTable = table

    def getSeqNum(self):
        return self.__seqNum

    def incrementSeqNum(self):
        # Sequence numbers defined by the originating Mobile Hosts are defined to be even numbers, and sequence numbers generated to indicate cm metrics are odd numbers.
        self.__seqNum += 1
        self.__routingTable[self.__nodeType][self.__nodeId]['seqNum'] = self.__seqNum

    def getLocation(self):
        return self.__centroid if self.__nodeType == NodeType.LOCATION_AWARE else self.__proxy

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
    def processRoutingTableUpdate(self, message, withLocationProxy):
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
                mustSave = newCost <= Configuration.MAX_HOPS or (withLocationProxy and (nodeType == NodeType.LOCATION_AWARE or data['radius'] > 0))
                notSelf = dest != self.__nodeId
                if inRoutingTable and notSelf:
                    currentSeqNum = self.__routingTable[nodeType][dest]['seqNum']
                    currentCost = self.__routingTable[nodeType][dest]['cost']
                    currentRadius = self.__routingTable[nodeType][dest]['radius']

                    if newSeqNum > currentSeqNum:
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        # If a new sequence number for a route is received, but the metric stays the same, that would be unlikely to be considered as a significant change.
                        updated = updated or newCost < currentCost or currentRadius + 1 < data['radius']
                    elif newSeqNum == currentSeqNum and newCost < currentCost:
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        updated = updated or True
                    # Not sure what the condition should be here
                    elif withLocationProxy and currentRadius + 1 < data['radius']:
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        updated = updated or True
                    else:
                        updated = updated or False
                elif mustSave and notSelf:
                    self.saveNewEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                    updated = updated or True

                if withLocationProxy and self.isLocationIgnorant() and nodeType == NodeType.LOCATION_AWARE:
                    radius = self.__routingTable[nodeType][dest]['cost']
                    proxyLocation = self.__routingTable[nodeType][dest]['location']
                    proxySaved = self.setProxy(proxyLocation, radius, dest)
                    updated = updated or proxySaved
        return updated

    def setProxy(self, proxyLocation, radius, proxyId):
        if self.__proxy is None or self.__radius > radius or self.__radius == 0:
            self.__proxy = proxyLocation
            self.__proxyId = proxyId
            self.__radius = radius
            self.__routingTable[self.__nodeType][self.__nodeId]['radius'] = radius
            LogService.log('Found Location Proxy {} for {} - radius {}'.format(proxyId, self.__nodeId, radius))
            return True
        else:
            return False

    def getBasicNextHop(self, packet):
        dest = packet.destId
        if self.__routingTable is None:
            return None
        elif dest in self.__routingTable[NodeType.LOCATION_AWARE]:
            LogService.log('Found destination in Routing Table.')
            return self.__routingTable[NodeType.LOCATION_AWARE][dest]['nextHop']
        elif dest in self.__routingTable[NodeType.LOCATION_IGNORANT]:
            LogService.log('Found destination in Routing Table.')
            return self.__routingTable[NodeType.LOCATION_IGNORANT][dest]['nextHop']
        elif self.isLocationAware():
            LogService.log('Trying to find node in the routing table that is physically closer to the destination...')
            location = packet.destLocation
            distance = utilitiesService.UtilitiesService.getCentroidDistance(location, self.getLocation())
            nextHop = None
            # Only location aware nodes can be used
            for nodeId, data in self.__routingTable[NodeType.LOCATION_AWARE].items():
                newDistance = utilitiesService.UtilitiesService.getCentroidDistance(location, data['location'])
                if newDistance < distance:
                    distance = newDistance
                    nextHop = data['nextHop']
                    LogService.log('id {} is closer'.format(nodeId))
                else:
                    LogService.log('id {} is not closer'.format(nodeId))
            return nextHop
        else:
            return None

    def getLocationProxyNextHop(self, packet):
        dest = packet.destId
        if self.__routingTable is None:
            return None
        elif dest in self.__routingTable[NodeType.LOCATION_AWARE]:
            LogService.log('Found destination in Routing Table.')
            return self.__routingTable[NodeType.LOCATION_AWARE][dest]['nextHop']
        elif dest in self.__routingTable[NodeType.LOCATION_IGNORANT]:
            LogService.log('Found destination in Routing Table.')
            return self.__routingTable[NodeType.LOCATION_IGNORANT][dest]['nextHop']
        else:
            LogService.log('Trying to find node in the routing table that is physically closer to the destination...')
            location = packet.destLocation
            distance = utilitiesService.UtilitiesService.getCentroidDistance(location, self.getLocation())
            nextHop = None
            for nodeType, table in self.__routingTable.items():
                for nodeId, data in self.__routingTable[nodeType].items():
                    if data['location'] is not None:
                        newDistance = utilitiesService.UtilitiesService.getCentroidDistance(location, data['location'])
                        if newDistance < distance:
                            distance = newDistance
                            nextHop = data['nextHop']
                            LogService.log('id {} is closer'.format(nodeId))
                        else:
                            LogService.log('id {} is not closer'.format(nodeId))
            return nextHop
