class RoutingService:

    @staticmethod
    def initRoutingTables(nodeService):
        for node in nodeService.getNodes().values():
            neighbors = nodeService.getNeighbors(node)
            for neighbor in neighbors:
                node.saveNewEntry(neighbor.getId(), 1, neighbor, 0, neighbor.getCentroid())

    @staticmethod
    def updateRoutingTables(nodeService):
        done = False
        while not done:
            updated = False
            for node in nodeService.getNodes().values():
                neighbors = nodeService.getNeighbors(node)
                update = {'origin': node,
                          'table': node.getRoutingTable(),
                          'seqNum': node.getSeqNum(),
                          'location': node.getCentroid()}
                for neighbor in neighbors:
                    updated = updated or neighbor.processRoutingTableUpdate(update)
            done = not updated

    # Basic Routing
    @staticmethod
    def forwardBasic(nodeService, packet):
        srcId = packet.srcId
        destId = packet.destId
        srcNode = nodeService.getNodes()[srcId]
        nextHop = srcNode.getBasicNextHop(packet)
        while nextHop is not None and destId != nextHop:
            print('Next hop: {}'.format(nextHop))
            nextHop = nodeService.getNodes()[nextHop].getBasicNextHop(packet)

        if destId != nextHop:
            print('Packet dropped:(')
        else:
            print('Packet delivered:)')