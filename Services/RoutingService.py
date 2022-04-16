from Services.LogService import LogService
from Constants import NodeType

class RoutingService:

    __nodeService = None

    def __init__(self, nodeService):
        self.__nodeService = nodeService

    def clearRoutingTables(self):
        for node in self.__nodeService.getNodes().values():
            routingTable = {NodeType.LOCATION_AWARE: {}, NodeType.LOCATION_IGNORANT: {}}
            routingTable[node.getType()][node.getId()] = {'cost': 0, 'nextHop': None, 'seqNum': 0, 'location': None, 'radius': 0}
            if node.getType() == NodeType.LOCATION_AWARE:
                routingTable[node.getType()][node.getId()]['location'] = node.getCentroid()
            node.setRoutingTable(routingTable)
        LogService.log('Routing Tables are cleared')

    def updateRoutingTables(self):
        for node in self.__nodeService.getNodes().values():
            self.advertiseRoutingTable(node)
        LogService.log('Full dump update on all nodes is done')

    def advertiseRoutingTable(self, node):
        # LogService.log('-- generated node {}'.format(node.getId()))
        queue = [node]
        while queue:
            node = queue.pop(0)
            # LogService.log('------ node popped {}'.format(node.getId()))
            neighbors = self.__nodeService.getNeighbors(node)
            node.incrementSeqNum()
            update = {'origin': node.getId(),
                      'location': node.getLocation(),
                      'seqNum': node.getSeqNum(),
                      'table': node.getRoutingTable()}
            for neighbor in neighbors:
                updated = neighbor.processRoutingTableUpdate(update, self.__nodeService.isWithLocationProxy())
                # LogService.log('---------- neighbor {} updated {}'.format(neighbor.getId(), updated))
                if updated:
                    queue.append(neighbor)
            # LogService.log('------ updated queue {}'.format(queue))

    # Basic Routing
    def forwardBasic(self, packet):
        srcId = packet.srcId
        destId = packet.destId
        srcNode = self.__nodeService.getNodes()[srcId]
        nextHop = srcNode.getBasicNextHop(packet)
        while nextHop is not None and destId != nextHop:
            LogService.log('Next hop: {}'.format(nextHop))
            nextHop = self.__nodeService.getNodes()[nextHop].getBasicNextHop(packet)
        if destId != nextHop:
            LogService.log('Packet is dropped :(')
        else:
            LogService.log('Packet is delivered at node {} :)'.format(nextHop))

    # Location Proxy Routing
    def forwardLocationProxy(self, packet):
        srcId = packet.srcId
        destId = packet.destId
        srcNode = self.__nodeService.getNodes()[srcId]
        nextHop = srcNode.getLocationProxyNextHop(packet)
        while nextHop is not None and destId != nextHop:
            LogService.log('Next hop: {}'.format(nextHop))
            nextHop = self.__nodeService.getNodes()[nextHop].getLocationProxyNextHop(packet)
        if destId != nextHop:
            LogService.log('Packet dropped :(')
        else:
            LogService.log('Packet is delivered at node {} :)'.format(nextHop))