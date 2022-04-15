class RoutingService:

    @staticmethod
    def advertiseRoutingTable(node, nodeService, withLocProxy):
        # print('-- generated node {}'.format(node.getId()))
        queue = [node]
        while queue:
            node = queue.pop(0)
            # print('------ node popped {}'.format(node.getId()))
            neighbors = nodeService.getNeighbors(node)
            node.incrementSeqNum()
            update = {'origin': node.getId(),
                      'location': node.getLocation(),
                      'seqNum': node.getSeqNum(),
                      'table': node.getRoutingTable()}
            for neighbor in neighbors:
                updated = neighbor.processRoutingTableUpdate(update, withLocProxy)
                # print('---------- neighbor {} updated {}'.format(neighbor.getId(), updated))
                if updated:
                    queue.append(neighbor)
            # print('------ updated queue {}'.format(queue))

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
