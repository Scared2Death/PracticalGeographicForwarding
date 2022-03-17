from Configurations import configuration

from Services.utilitiesService import utilitiesService

class nodesService():

    __nodesAreInitialized = False
    __nodes = []

    @staticmethod
    def __initializeNodes():

        someNodeGenerationFailed = False
        for _ in range(configuration.NUMBER_OF_NODES_TO_GENERATE + 1):

            couldGenerateNode = False

            for trial in range(configuration.NUMBER_OF_MAXIMUM_TRIALS_AT_NODE_GENERATION + 1):

                justCreatedNode = utilitiesService.generateNode()
                isMinimumDistanceProvided = True

                for existentNode in nodesService.__nodes:
                    distance = utilitiesService.getDistance(justCreatedNode, existentNode)

                    if distance < configuration.MINIMUM_NODE_GENERATION_DISTANCE:
                        isMinimumDistanceProvided = False
                        break

                if isMinimumDistanceProvided:
                    couldGenerateNode = True
                    break

            if couldGenerateNode:
                nodesService.__nodes.append(justCreatedNode)
            else:
                someNodeGenerationFailed = True
                break

        if someNodeGenerationFailed:
            return False
        else:
            nodesService.__nodesAreInitialized = True
            return True

    @staticmethod
    def getNodes():
        if nodesService.__nodesAreInitialized is False:

            couldInitializeNodes = nodesService.__initializeNodes()

            if couldInitializeNodes:
                return nodesService.__nodes
            else:
                raise Exception("Node initialization couldn't be carried out .")