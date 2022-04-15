from Services.LogService import LogService

class RoutingService:

    @staticmethod
    def advertiseRoutingTable(node, nodeService, withLocProxy):
        # LogService.log('-- generated node {}'.format(node.getId()))
        queue = [node]
        while queue:
            node = queue.pop(0)
            # LogService.log('------ node popped {}'.format(node.getId()))
            neighbors = nodeService.getNeighbors(node)
            node.incrementSeqNum()
            update = {'origin': node.getId(),
                      'location': node.getLocation(),
                      'seqNum': node.getSeqNum(),
                      'table': node.getRoutingTable()}
            for neighbor in neighbors:
                updated = neighbor.processRoutingTableUpdate(update, withLocProxy)
                # LogService.log('---------- neighbor {} updated {}'.format(neighbor.getId(), updated))
                if updated:
                    queue.append(neighbor)
            # LogService.log('------ updated queue {}'.format(queue))

    # Basic Routing
    @staticmethod
    def forwardBasic(nodeService, packet):
        srcId = packet.srcId
        destId = packet.destId
        srcNode = nodeService.getNodes()[srcId]
        nextHop = srcNode.getBasicNextHop(packet)
        while nextHop is not None and destId != nextHop:
            LogService.log('Next hop: {}'.format(nextHop))
            nextHop = nodeService.getNodes()[nextHop].getBasicNextHop(packet)
        if destId != nextHop:
            LogService.log('Packet dropped :(')
        else:
            LogService.log('Packet delivered :)')