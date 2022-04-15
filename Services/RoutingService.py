class RoutingService:

    @staticmethod
    def initRoutingTables(nodeService):
        for node in nodeService.getNodes().values():
            neighbors = nodeService.getNeighbors(node)
            for neighbor in neighbors:
                neighborId = neighbor.getId()
                radius = neighbor.getRadius() if neighbor.getRadius() == 0 else neighbor.getRadius() - 1
                node.saveNewEntry(neighbor.getType(), neighborId, 1, neighborId, 0, neighbor.getLocation(), radius)

    @staticmethod
    def updateRoutingTables(nodeService, withLocProxy):
        updated = False
        for node in nodeService.getNodes().values():
            neighbors = nodeService.getNeighbors(node)
            # Increment sequence number during first dump only to avoid infinite loop
            node.incrementSeqNum()
            update = {'origin': node.getId(),
                      'location': node.getLocation(),
                      'seqNum': node.getSeqNum(),
                      'table': node.getRoutingTable()}
            for neighbor in neighbors:
                updated = updated or neighbor.processRoutingTableUpdate(update, withLocProxy)
        done = not updated
        while not done:
            updated = False
            for node in nodeService.getNodes().values():
                neighbors = nodeService.getNeighbors(node)
                update = {'origin': node.getId(),
                          'table': node.getRoutingTable(),
                          'seqNum': node.getSeqNum(),
                          'location': node.getLocation()}
                for neighbor in neighbors:
                    updated = updated or neighbor.processRoutingTableUpdate(update, withLocProxy)
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
