from Services.LogService import LogService

class RoutingService:

    __nodeService = None
    __inLocationProxyMode = False
    __inInfMode = False

    def __init__(self, nodeService, inLocationProxyMode):
        self.__nodeService = nodeService
        self.__inLocationProxyMode = inLocationProxyMode
        self.updateRoutingTables()

    def setInLocationProxyMode(self, inLocationProxyMode):
        if self.__inLocationProxyMode and not inLocationProxyMode:
            self.clearRoutingTables()

        if self.__inLocationProxyMode != inLocationProxyMode:
            self.__inLocationProxyMode = inLocationProxyMode
            LogService.log('Location Proxy mode is set to: {}'.format(inLocationProxyMode))
            self.updateRoutingTables()

    def isInLocationProxyMode(self):
        return self.__inLocationProxyMode

    def setInInfMode(self, inInfMode):
        self.__inInfMode = inInfMode

    def isInInfMode(self):
        return self.__inInfMode

    def clearRoutingTables(self):
        for node in self.__nodeService.getNodes().values():
            node.resetRoutingTable()
        LogService.log('Routing Tables are cleared')

    def updateRoutingTables(self):
        for node in self.__nodeService.getNodes().values():
            self.advertiseRoutingTable(node)
        for node in self.__nodeService.getNodes().values():
            node.removeLostRoutes()
        LogService.log('Full dump update on all nodes is done')

    def advertiseRoutingTable(self, advertisedNode):
        LogService.debug('Advertising table of {}'.format(advertisedNode.getId()))
        queue = [advertisedNode]
        while queue:
            node = queue.pop(0)
            LogService.debug('\tNode popped from queue: {}'.format(node.getId()))
            neighbors = self.__nodeService.getNeighbors(node)
            node.updateNeighbors(neighbors)
            node.incrementSeqNum()
            update = {'origin': node.getId(),
                      'location': node.getLocation(),
                      'seqNum': node.getSeqNum(),
                      'table': node.getRoutingTable()}
            for neighbor in neighbors.values():
                updated = neighbor.processRoutingTableUpdate(update, self.__inLocationProxyMode)
                LogService.debug('\t\tNeighbor {} of {} updated: {}'.format(neighbor.getId(), node.getId(), updated))
                if updated:
                    queue.append(neighbor)
            LogService.debug('\tUpdated queue: {}'.format(list(map(lambda n: n.getId(), queue))))
        LogService.debug('Routing Tables after advertisement of {}'.format(advertisedNode.getId()))
        LogService.debug(self.__nodeService.printRoutingTables())

    # Finds the next hop based on the current value of __inLocationProxyMode field
    def getNextHopInRoute(self, packet, nextHop = None):
        srcNode = self.__nodeService.getNodeByID(packet.getSrcId())
        if (nextHop == None):
            return srcNode.getNextHop(packet, self.__inLocationProxyMode, self.__inInfMode)
        else:
            return self.__nodeService.getNodeByID(nextHop).getNextHop(packet, self.__inLocationProxyMode, self.__inInfMode)