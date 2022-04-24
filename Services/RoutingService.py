import Configurations.Configuration
from Services.LogService import LogService
from Services.UtilitiesService import UtilitiesService
from Services.GuiService import GuiService

from Constants import NodeType

class RoutingService:

    __nodeService = None

    def __init__(self, nodeService):
        self.__nodeService = nodeService

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
        # LogService.log('Advertising table of {}'.format(advertisedNode.getId()))
        queue = [advertisedNode]
        while queue:
            node = queue.pop(0)
            # LogService.log('\t\tNode popped from queue: {}'.format(node.getId()))
            neighbors = self.__nodeService.getNeighbors(node)
            node.updateNeighbors(neighbors)
            node.incrementSeqNum()
            update = {'origin': node.getId(),
                      'location': node.getLocation(),
                      'seqNum': node.getSeqNum(),
                      'table': node.getRoutingTable()}
            for neighbor in neighbors.values():
                updated = neighbor.processRoutingTableUpdate(update, self.__nodeService.isWithLocationProxy())
                # LogService.log('\t\t\tNeighbor {} of {} updated: {}'.format(neighbor.getId(), node.getId(), updated))
                if updated:
                    queue.append(neighbor)
            # LogService.log('\t\tUpdated queue: {}'.format(queue))
        # LogService.log('Routing Tables after advertisement of {}'.format(advertisedNode.getId()))
        # self.__nodeService.printRoutingTables()

    # Basic Routing
    def forwardBasic(self, packet):
        srcId = packet.srcId
        destId = packet.destId
        srcNode = self.__nodeService.getNodes()[srcId]

        # TEMP DELAY -> PERHAPS SHOULD BE SYNCHRONIZED WITH THE MOVEMENTS INCURRED
        self.__delayExecution()
        # NOW WHEN A SENDING IS INITIATED, NO MOVEMENT OF THE NODES OCCUR, I GUESS, THOUGH IT GENERALLY HAPPENS I THINK

        # PACKET VISUALIZATION / RENDERING SO THAT THE ROUTE TAKEN CAN BE TRACKED

        nextHop = srcNode.getBasicNextHop(packet)
        while nextHop is not None and destId != nextHop:
            LogService.log('Next hop: {}'.format(nextHop))

            # SHOULD VISUALIZE / RENDER THE NEXT HOP
            nextHop = self.__nodeService.getNodes()[nextHop].getBasicNextHop(packet)

            self.__delayExecution()
        if destId != nextHop:
            LogService.log('Packet is dropped :(')
        else:
            LogService.log('Packet is delivered at node {} :)'.format(nextHop))

    # Location Proxy Routing
    def forwardLocationProxy(self, packet):
        srcId = packet.srcId
        destId = packet.destId
        srcNode = self.__nodeService.getNodes()[srcId]

        # TEMP DELAY -> PERHAPS SHOULD BE SYNCHRONIZED WITH THE MOVEMENTS INCURRED
        self.__delayExecution()

        # NOW WHEN A SENDING IS INITIATED, NO MOVEMENT OF THE NODES OCCUR, I GUESS, THOUGH IT GENERALLY HAPPENS I THINK

        # PACKET VISUALIZATION / RENDERING SO THAT THE ROUTE TAKEN CAN BE TRACKED

        nextHop = srcNode.getLocationProxyNextHop(packet)
        while nextHop is not None and destId != nextHop:
            LogService.log('Next hop: {}'.format(nextHop))

            # SHOULD VISUALIZE / RENDER THE NEXT HOP
            nextHop = self.__nodeService.getNodes()[nextHop].getLocationProxyNextHop(packet)

            self.__delayExecution()
        if destId != nextHop:
            LogService.log('Packet dropped :(')
        else:
            LogService.log('Packet is delivered at node {} :)'.format(nextHop))

    def __delayExecution(self):
        UtilitiesService.delayExecution()