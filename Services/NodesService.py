from Configurations import Configuration

from Services.UtilitiesService import UtilitiesService
from Models import Node

class NodesService:

    __nodesAreInitialized = False
    __nodes = [Node]

    def __initializeNodes(self):

        self.__nodes.clear()

        someNodeGenerationFailed = False
        for _ in range(Configuration.NUMBER_OF_NODES_TO_GENERATE + 1):

            couldGenerateNode = False

            for trial in range(Configuration.NUMBER_OF_MAXIMUM_TRIALS_AT_NODE_GENERATION + 1):

                justCreatedNode = UtilitiesService.generateNode()
                isMinimumDistanceProvided = True

                for existentNode in self.__nodes:
                    distance = UtilitiesService.getNodeDistance(justCreatedNode, existentNode)

                    if distance < Configuration.MINIMUM_NODES_DISTANCE:
                        isMinimumDistanceProvided = False
                        break

                if isMinimumDistanceProvided:
                    couldGenerateNode = True
                    break

            if couldGenerateNode:
                self.__nodes.append(justCreatedNode)
            else:
                someNodeGenerationFailed = True
                break

        if someNodeGenerationFailed:
            return False
        else:
            self.__nodesAreInitialized = True
            return True

    def getNodes(self):
        if self.__nodesAreInitialized is False:

            couldInitializeNodes = self.__initializeNodes()

            if couldInitializeNodes:
                return self.__nodes
            else:
                raise Exception("Node initialization couldn't be carried out .")

        else:
            return self.__nodes

    def incurNodeMovements(self):
        for node in self.__nodes:
            node.changePosition(self.__nodes)