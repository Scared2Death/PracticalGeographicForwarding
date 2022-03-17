from Configurations import configuration

from Services.utilitiesService import utilitiesService

class nodesService():

    __nodesAreInitialized = False
    __nodes = []

    def __initializeNodes(self):

        self.__nodes.clear()

        someNodeGenerationFailed = False
        for _ in range(configuration.NUMBER_OF_NODES_TO_GENERATE + 1):

            couldGenerateNode = False

            for trial in range(configuration.NUMBER_OF_MAXIMUM_TRIALS_AT_NODE_GENERATION + 1):

                justCreatedNode = utilitiesService.generateNode()
                isMinimumDistanceProvided = True

                for existentNode in self.__nodes:
                    distance = utilitiesService.getDistance(justCreatedNode, existentNode)

                    if distance < configuration.MINIMUM_NODE_GENERATION_DISTANCE:
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