from math import inf

import Services.UtilitiesService as utilitiesService

from Constants import NodeType, InfMode
from Models.Centroid import Centroid
from Models.Packet import Packet
from Services.LogService import LogService
from Configurations import Configuration

class Node:

    __centroid = None
    __shapeRadius = None
    __broadcastRange = None
    __nodeType = None
    __nodeId = None
    __neighbors = None
    __routingTable = None
    __seqNum = 0
    __proxy = None
    __proxyId = None
    __radius = 0
    __infTable = {}
    __packet = None
    __attempt = 0

    def __init__(self, centroid, shapeRadius, broadcastRange, nodeType, nodeId):
        self.__centroid = centroid
        self.__shapeRadius = shapeRadius
        self.__broadcastRange = broadcastRange
        self.__nodeType = nodeType
        self.__nodeId = nodeId
        self.__neighbors = {}
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

    def getPacket(self):
        return self.__packet

    def setPacket(self, packet):
        self.__packet = packet

    def setAttempt(self, attempt):
        self.__attempt = attempt

    def getProxy(self):
        return self.__proxy

    def incrementSeqNum(self):
        # Sequence numbers defined by the originating Mobile Hosts are defined to be even numbers, and sequence numbers generated to indicate (inf) metrics are odd numbers.
        self.__seqNum += 2
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

    def resetRoutingTable(self):
        self.__routingTable = {NodeType.LOCATION_AWARE: {}, NodeType.LOCATION_IGNORANT: {}}
        self.__routingTable[self.__nodeType][self.__nodeId] = {'cost': 0, 'nextHop': None, 'seqNum': 0, 'location': None, 'radius': 0}
        if self.__nodeType == NodeType.LOCATION_AWARE:
            self.__routingTable[self.__nodeType][self.__nodeId]['location'] = self.__centroid
        self.__proxy = None
        self.__proxyId = None
        self.__radius = 0

    def resetInfTable(self):
        self.__infTable = {}

    # Returns true if routing table is updated, false otherwise
    def processRoutingTableUpdate(self, message, withLocationProxy):
        updated = False
        senderId = message['origin']
        routingTable = message['table']
        LogService.debug('\t\tNode {} is processing table of {}'.format(self.getId(), senderId))
        for nodeType, table in routingTable.items():
            LogService.debug('\t\t{} nodes:'.format(nodeType))
            for dest, data in table.items():
                newCost = data['cost'] + 1
                newSeqNum = data['seqNum']
                newLocation = data['location']
                newRadius = data['radius'] if data['radius'] == 0 else data['radius'] - 1
                inRoutingTable = dest in self.__routingTable[nodeType]
                mustSave = newCost <= Configuration.MAX_HOPS or (withLocationProxy and (nodeType == NodeType.LOCATION_AWARE or data['radius'] > 0))
                notSelf = dest != self.__nodeId
                if inRoutingTable and notSelf:
                    LogService.debug('\t\tDest {} is in routing table and not self'.format(dest))
                    lostRoute = data['cost'] == float(inf) and self.__routingTable[nodeType][dest]['nextHop'] == senderId
                    currentSeqNum = self.__routingTable[nodeType][dest]['seqNum']
                    currentCost = self.__routingTable[nodeType][dest]['cost']
                    currentRadius = self.__routingTable[nodeType][dest]['radius']
                    improvedCost = newCost < currentCost
                    updatedRadius = currentRadius < data['radius'] - 1
                    if lostRoute:
                        self.__routingTable[nodeType][dest]['cost'] = float(inf)
                        updatedCost = currentCost != float(inf)
                        updated = updated or updatedCost
                        LogService.debug('\t\t\tDest {} is lost route (cost updated {})'.format(dest, updatedCost))
                    elif newSeqNum > currentSeqNum:
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        # If a new sequence number for a route is received, but the metric stays the same, that would be unlikely to be considered as a significant change.
                        updated = updated or improvedCost or updatedRadius
                        LogService.debug('\t\t\tSeq number is updated (cost is better {}, radius is updated {})'.format(dest, improvedCost, updatedRadius))
                    elif newSeqNum == currentSeqNum and improvedCost:
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        updated = updated or True
                        LogService.debug('\t\t\tFound better route to {} (cost updated {})'.format(dest, improvedCost))
                    elif withLocationProxy and updatedRadius:
                        # If the current radius is smaller than the recieved radius minus one, the radius must be updated, otherwise the route will not be propagated to the proxy
                        self.updateEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                        updated = updated or True
                        LogService.debug('\t\t\tRadius update of {} in proxy mode'.format(dest))
                    else:
                        updated = updated or False
                elif mustSave and notSelf:
                    self.saveNewEntry(nodeType, dest, newCost, senderId, newSeqNum, newLocation, newRadius)
                    updated = updated or True
                    LogService.debug('\t\t\tRoute to {} must be saved'.format(dest))

                if withLocationProxy and self.isLocationIgnorant() and nodeType == NodeType.LOCATION_AWARE:
                    radius = self.__routingTable[nodeType][dest]['cost']
                    proxyLocation = self.__routingTable[nodeType][dest]['location']
                    proxySaved = self.setProxy(proxyLocation, radius, dest)
                    updated = updated or proxySaved
                    LogService.debug('\t\t\tProxy for {} is saved {}'.format(dest, proxySaved))
        return updated

    def setProxy(self, proxyLocation, radius, proxyId):
        if self.__proxy is None or self.__radius > radius or self.__radius == 0:
            self.__proxy = proxyLocation
            self.__proxyId = proxyId
            self.__radius = radius
            self.__routingTable[self.__nodeType][self.__nodeId]['radius'] = radius
            LogService.debug('\t\t\tFound new Location Proxy {} for {} - radius {}'.format(proxyId, self.__nodeId, radius))
            return True
        else:
            return False

    # When a node originates a packet, it checks to see if there is an entry for the packet’s destination in the INF table.
    # If so, the packet’s INF mode is set to TO-INF, and the intermediate location is copied into the packet header from
    # the INF table. If there is no entry in the INF table, the INF mode is set to NO-INF.
    def setInfDetailsOfPacket(self):
        if self.__packet.getDestId() in self.__infTable:
            self.__packet.setInfMode(InfMode.TO_INF)
            self.__packet.setIntermediateLocation(self.__infTable[self.__packet.getDestId()])
            LogService.log('INF details are set: {} - {}'.format(self.__packet.getInfMode(), self.__packet.getIntermediateLocation()))
        else:
            self.__packet.setInfMode(InfMode.NO_INF)
            LogService.log('INF details are set: {}'.format(self.__packet.getInfMode()))

    def __setIntermediateLocation(self):
        if self.getLocation() is not None:
            radiusRatio = 1/4 if self.__attempt < Configuration.MAX_ATTEMPTS / 2 else 1/2
            intermediateLocation = utilitiesService.UtilitiesService.getIntermediateLocation(self.getLocation(), self.__packet.getDestLocation(), radiusRatio)
            self.__infTable[self.__packet.getDestId()] = intermediateLocation
            LogService.log('New Intermediate location for destination {}: {}'.format(self.__packet.getDestId(), intermediateLocation))
            self.setInfDetailsOfPacket()
            return True
        else:
            return False

    # packet must be passed here because NAK packet is not saved by node
    def getInfExtras(self, packet, showCircleAndLine):
        if packet.getInfMode() == InfMode.TO_INF:
            radiusRatio = 1/4 if self.__attempt < 5 else 1/2
            locationA = Centroid(self.getLocation().x, self.getLocation().y)
            locationB = Centroid(packet.getDestLocation().x, packet.getDestLocation().y)
            extras = utilitiesService.UtilitiesService.calculateInfExtras(locationA,
                                                                          locationB, radiusRatio,
                                                                          packet.getIntermediateLocation(), showCircleAndLine)
            return extras
        return None

    def createNakPacket(self, packet):
        nakPacket = Packet(self.__nodeId, self.getLocation(), self.getCentroid(), packet.getSrcId(), packet.getSrcLocation(),
                        InfMode.NO_INF, None, True)
        if packet.getInfMode() == InfMode.FROM_INF and packet.getIntermediateLocation() != self.getLocation():
            nakPacket.setInfMode(InfMode.TO_INF)
            nakPacket.setIntermediateLocation(packet.getIntermediateLocation())
        LogService.log('NAK Packet created {}'.format(nakPacket))
        return nakPacket

    def handleNakPacket(self):
        LogService.log('Node {} is handling NAK packet, node location: {} (proxy: {})'.format(self.__nodeId, self.getLocation(), self.__proxyId))
        if self.__attempt < Configuration.MAX_ATTEMPTS:
            self.__attempt += 1
            result = self.__setIntermediateLocation()
            if not result:
                LogService.log('Cannot set intermediate location')
            return result

        LogService.log('No more attempts')
        self.__packet = None
        self.__attempt = 0
        return False

    def getNextHop(self, packet, inLocationProxyMode, inInfMode):
        if inInfMode:
            return self.__getInfNextHop(packet, inLocationProxyMode)
        elif inLocationProxyMode:
            return self.__getLocationProxyNextHop(packet, None)
        else:
            return self.__getBasicNextHop(packet, None)

    def __getBasicNextHop(self, packet, intermediateLocation):
        dest = float(inf) if intermediateLocation is not None else packet.getDestId()
        if dest == float(inf):
            LogService.log('Finding next hop based on Intermediate Location: {}'.format(intermediateLocation))
        else:
            LogService.log('Finding next hop based on destination ID: {}'.format(dest))

        if self.__routingTable is None:
            return None
        elif dest == self.__nodeId:
            return self.__nodeId
        elif dest in self.__routingTable[NodeType.LOCATION_AWARE]:
            LogService.log('Found destination in Routing Table.')
            return self.__routingTable[NodeType.LOCATION_AWARE][dest]['nextHop']
        elif dest in self.__routingTable[NodeType.LOCATION_IGNORANT]:
            LogService.log('Found destination in Routing Table.')
            return self.__routingTable[NodeType.LOCATION_IGNORANT][dest]['nextHop']
        elif self.isLocationAware():
            LogService.log('Finding neighbor closest to the destination.')
            destLocation = intermediateLocation if intermediateLocation is not None else packet.getDestLocation()
            distance = utilitiesService.UtilitiesService.getCentroidDistance(destLocation, self.getLocation())
            nextHop = None
            LogService.log('Own distance from destination: {}'.format(distance))
            # Only location aware nodes can be used
            for nodeId, data in self.__routingTable[NodeType.LOCATION_AWARE].items():
                if nodeId != self.__nodeId:
                    newDistance = utilitiesService.UtilitiesService.getCentroidDistance(destLocation, data['location'])
                    LogService.log('Distance of Node {} from destination: {}'.format(data['nextHop'], newDistance))
                    if newDistance < distance:
                        distance = newDistance
                        nextHop = data['nextHop']
            if nextHop is not None:
                LogService.log('Node {} is closer to the destination'.format(nextHop))
            else:
                LogService.log('No node is closer to the destination')
            return nextHop
        else:
            return None

    def __getLocationProxyNextHop(self, packet, intermediateLocation):
        dest = float(inf) if intermediateLocation is not None else packet.getDestId()
        if dest == float(inf):
            LogService.log('Finding next hop based on Intermediate Location: {}'.format(intermediateLocation))
        else:
            LogService.log('Finding next hop based on destination ID: {}'.format(dest))
        nextHop = None
        if self.__routingTable is None:
            return None
        elif dest == self.__nodeId:
            return self.__nodeId
        elif dest in self.__routingTable[NodeType.LOCATION_AWARE]:
            LogService.log('Found destination in Routing Table.')
            return self.__routingTable[NodeType.LOCATION_AWARE][dest]['nextHop']
        elif dest in self.__routingTable[NodeType.LOCATION_IGNORANT]:
            LogService.log('Found destination in Routing Table.')
            return self.__routingTable[NodeType.LOCATION_IGNORANT][dest]['nextHop']
        elif self.getLocation() is not None:
            LogService.log('Finding neighbor closest to the destination.')
            destLocation = intermediateLocation if intermediateLocation is not None else packet.getDestLocation()
            distance = utilitiesService.UtilitiesService.getCentroidDistance(destLocation, self.getLocation())
            LogService.log('Own distance from destination: {}'.format(distance))
            for nodeType, table in self.__routingTable.items():
                for nodeId, data in self.__routingTable[nodeType].items():
                    if data['location'] is not None and nodeId != self.__nodeId:
                        newDistance = utilitiesService.UtilitiesService.getCentroidDistance(destLocation, data['location'])
                        LogService.log('Distance of Node {} from destination: {}'.format(data['nextHop'], newDistance))
                        if newDistance < distance:
                            distance = newDistance
                            nextHop = data['nextHop']
            if nextHop is not None:
                LogService.log('Node {} is closer to the destination'.format(nextHop))
            else:
                LogService.log('No node is closer to the destination')
        return nextHop

    # When a node forwards a packet,
    # it makes its forwarding decision based on the packet’s INF mode. If the packet is in the TO-INF mode, the packet is
    # forwarded to the intermediate location; otherwise, the packet is forwarded to the destination location.
    def __getInfNextHop(self, packet, inLocationProxyMode):
        if packet.getInfMode() == InfMode.TO_INF:
            LogService.log('Packet is in TO_INF mode.')
            nextHop = self.__getNextHopForInfNextHop(packet, inLocationProxyMode, packet.getIntermediateLocation())

            # If a node forwarding a TO-INF packet has no neighbor closer than itself to the intermediate point, it switches the
            # packet to FROM-INF mode. From then on, the packet’s real destination is used to make forwarding decisions.
            if nextHop is None:
                packet.setInfMode(InfMode.FROM_INF)
                LogService.log('Packet is set to FROM_INF mode.')
                packet.setIntermediateLocation(self.getLocation())
                nextHop = self.__getNextHopForInfNextHop(packet, inLocationProxyMode, None)
        else:
            LogService.log('Packet is in mode: {}'.format(packet.getInfMode()))
            nextHop = self.__getNextHopForInfNextHop(packet, inLocationProxyMode, None)

        return nextHop if nextHop is not None else "NAK"

    def __getNextHopForInfNextHop(self, packet, inLocationProxyMode, intermediateLocation):
        if inLocationProxyMode:
            LogService.log('Finding INF next hop in Location Proxy mode.')
            return self.__getLocationProxyNextHop(packet, intermediateLocation)
        else:
            LogService.log('Finding INF next hop in Basic mode.')
            return self.__getBasicNextHop(packet, intermediateLocation)

    def updateNeighbors(self, newNeighbors):
        LogService.debug('\tNeighbors of {} before update {}'.format(self.__nodeId, self.__neighbors.keys()))
        LogService.debug('\tActual neighbors {}'.format(newNeighbors.keys()))
        for nodeId, node in self.__neighbors.items():
            if nodeId not in newNeighbors:
                self.__routingTable[node.getType()][nodeId]['cost'] = float(inf)
                self.updateRoutingTableWithLostNeighbor(nodeId)
        self.__neighbors = newNeighbors

    # When the link breaks, an (inf) metric route should be advertised for it, as well as for the routes that depend on it
    def updateRoutingTableWithLostNeighbor(self, lostNeighbor):
        for type, table in self.__routingTable.items():
            for dest, data in table.items():
                if data['nextHop'] == lostNeighbor:
                    data['cost'] = float(inf)
                    LogService.debug('\tRoute to node {} in table of {} is lost'.format(dest, self.__nodeId))

    def removeLostRoutes(self):
        removed = False
        for nodeType in list(self.__routingTable.keys()):
            for dest in list(self.__routingTable[nodeType].keys()):
                if self.__routingTable[nodeType][dest]['cost'] == float(inf):
                    del self.__routingTable[nodeType][dest]
                    removed = True
                    LogService.debug('\tRemoved {} from table of {}'.format(dest, self.__nodeId))
        return removed

    def checkNetworkBelonging(self, otherNodes):

        hasAnyIntersection = False

        for otherNode in otherNodes:

            if self == otherNode:
                continue
            else:
                hasAnyIntersection = utilitiesService.UtilitiesService.checkNodeIntersection(self, otherNode)

                if hasAnyIntersection:
                    break;

        return hasAnyIntersection