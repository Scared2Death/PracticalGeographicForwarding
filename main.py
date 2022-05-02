from Configurations import Configuration
from Constants import InfMode

from Models.Packet import Packet

from Services.GuiService import GuiService
from Services.NodesService import NodesService
from Services.RoutingService import RoutingService
from Services.LogService import LogService

import traceback

__nodeService : NodesService = None
__routingService : RoutingService = None

__isNewSendingInitiatable = True
__isSendingInProgress = False

__packet : Packet = None
__packetLocations = []
__nextHop = None
__routingResult : [] = None

__isRenderingINFNodes = False

__isAutomaticSimulation = Configuration.IS_AUTOMATIC_SIMULATION_ENABLED_BY_DEFAULT

def main(x = None, y = None, event = None):
    # initialization
    # reinitialization

    main.__nodeService = NodesService()
    main.__routingService = RoutingService(main.__nodeService, False)
    # main.__nodeService.printRoutingTables()

    __ui.render(main.__nodeService.getNodes().values(), __getHelperText())
    __ui.window.after(Configuration.DELAY_INTERVAL, __incurAutomaticSimulation)
    __ui.loop()

def __toggleAutomaticSimulation(event):
    global __isAutomaticSimulation
    __isAutomaticSimulation = not __isAutomaticSimulation

def __incurAutomaticSimulation():
    if __isAutomaticSimulation:
        __move()

    __ui.window.after(Configuration.DELAY_INTERVAL, __incurAutomaticSimulation)

def __move(x = None, y = None, event = None):
    global __nextHop
    global __prevNextHop
    global __isSendingInProgress
    global __isNewSendingInitiatable
    global __routingResult

    main.__nodeService.incurNodeMovements()
    main.__routingService.updateRoutingTables()

    if __isSendingInProgress:

        __routingResult = []

        if __nextHop is None:
            __prevNextHop = __packet.srcId
            __nextHop = __routing(__packet)
        else:
            __prevNextHop = __nextHop
            __nextHop = __routing(__packet, __nextHop)

        if __nextHop is not None and __nextHop != 'NAK' and __packet.destId != __nextHop:
            __packetLocations.append((__nextHop, main.__nodeService.getNodeByID(__nextHop).getCentroid()))
            # LogService.log('Next hop: {}'.format(__nextHop))
            __routingResult.append('Next hop: {}'.format(__nextHop))
            __routingResult.append(None)
        # else:
        #     if __nextHop == 'NAK':
        #         __isSendingInProgress = False
        #         __isNewSendingInitiatable = True
        #         # WIP
        #         # __initiateNakSending(__packet, __prevNextHop)
        else:
            if __packet.destId != __nextHop:
                # LogService.log('Packet is dropped :(')
                __routingResult.append('Packet is dropped :(')
                __routingResult.append(False)
            else:
                __packetLocations.append((__nextHop, main.__nodeService.getNodeByID(__nextHop).getCentroid()))
                # LogService.log('Packet is delivered at node {} :)'.format(__nextHop))
                __routingResult.append('Packet is delivered at node {} :)'.format(__nextHop))
                __routingResult.append(True)

            __isSendingInProgress = False
            __isNewSendingInitiatable = True
    else:
        if __packetLocations.count != 0:
            __packetLocations.clear()
        __routingResult = None

    __ui.render(main.__nodeService.getNodes().values(), __getHelperText(), __packetLocations, routingResult = __routingResult)

    # main.__nodeService.printRoutingTables()

def checkNewSendingInitiatability():
    global __isNewSendingInitiatable
    if not __isNewSendingInitiatable:
        LogService.log("A new sending is not initiatable . A current sending process is being carried out .")
        return False
    else:
        __isNewSendingInitiatable = False
        return True

def __initiateBasicRoutingSending(event):

    if not checkNewSendingInitiatability():
        return

    packetSendingDetails = __askForPacketSendingDetails()

    # UI WINDOW OR WHATEVER
    if packetSendingDetails is None:
        LogService.log("Wrongful inputs provided .")
        global __isNewSendingInitiatable
        __isNewSendingInitiatable = True
        return

    __packetLocations.clear()

    global __isSendingInProgress
    __isSendingInProgress = True

    main.__routingService.setInLocationProxyMode(False)
    # main.__nodeService.printRoutingTables()

    global __packet
    __packet = __createPacket(packetSendingDetails, False)
    __packetLocations.append((__packet.srcId, __packet.srcCentroid))

def __initiateLocationProxyRoutingSending(event):

    if not checkNewSendingInitiatability():
        return

    packetSendingDetails = __askForPacketSendingDetails()

    # UI WINDOW OR WHATEVER
    if packetSendingDetails is None:
        LogService.log("Wrongful inputs provided .")
        global __isNewSendingInitiatable
        __isNewSendingInitiatable = True
        return

    __packetLocations.clear()

    global __isSendingInProgress
    __isSendingInProgress = True

    main.__routingService.setInLocationProxyMode(True)
    # main.__nodeService.printRoutingTables()

    global __packet
    __packet = __createPacket(packetSendingDetails, False)
    __packetLocations.append((__packet.srcId, __packet.srcCentroid))

# WIP
def __initiateInfRoutingSending(event):

    if not checkNewSendingInitiatability():
        return

    packetSendingDetails = __askForPacketSendingDetails()

    # UI WINDOW OR WHATEVER
    if packetSendingDetails is None:
        LogService.log("Wrongful inputs provided .")
        global __isNewSendingInitiatable
        __isNewSendingInitiatable = True
        return

    __packetLocations.clear()

    global __isSendingInProgress
    __isSendingInProgress = True

    main.__routingService.setInInfMode(True)
    # main.__nodeService.printRoutingTables()

    global __packet
    __packet = __createPacket(packetSendingDetails, True)
    __packetLocations.append((__packet.srcId, __packet.srcCentroid))

# WIP
def __initiateNakSending(packet, sourceId):

    if not checkNewSendingInitiatability():
        return

    __packetLocations.clear()

    global __isSendingInProgress
    __isSendingInProgress = True

    main.__routingService.setInInfMode(True)
    # main.__nodeService.printRoutingTables()

    global __packet
    __packet = __createNakPacket(packet, True, sourceId)
    __packetLocations.append((__packet.srcId, __packet.srcCentroid))

def __routing(packet, nextHop = None):
    if nextHop is None:
        nextHop = main.__routingService.getNextHopInRoute(packet)
    else:
        nextHop = main.__routingService.getNextHopInRoute(packet, nextHop)

    return nextHop

def __turnIntermediateNodeForwardingOn(event):
    infNodes = main.__nodeService.getINFNodes().values()

    global __isRenderingINFNodes
    __isRenderingINFNodes = True

    __ui.render(infNodes, __getHelperText(), __packetLocations, __isRenderingINFNodes)

    # other todos ...

def __turnIntermediateNodeForwardingOff(event):
    global __isRenderingINFNodes
    __isRenderingINFNodes = False
    main()

__ui = GuiService(
    Configuration.GUI_WINDOW_WIDTH,
    Configuration.GUI_WINDOW_HEIGHT,
    main,
    __move,
    __initiateBasicRoutingSending,
    __initiateLocationProxyRoutingSending,
    __turnIntermediateNodeForwardingOn,
    __turnIntermediateNodeForwardingOff,
    __toggleAutomaticSimulation)

def __askForPacketSendingDetails():
    src = input('Source: ')
    # Source may or may not know its own location
    # srcCentroid => needed for visualization

    if int(src) in main.__nodeService.getNodes():
        srcLocation = main.__nodeService.getNodeByID(int(src)).getCentroid()
        srcCentroid = main.__nodeService.getNodeByID(int(src)).getCentroid()
    else:
        return None

    dest = input('Destination: ')
    # Destination location is always known, since we are using locations as addresses

    if int(dest) in main.__nodeService.getNodes():
        destLocation = main.__nodeService.getNodeByID(int(dest)).getCentroid()
    else:
        return None

    msg = input('Message: ')

    return (int(src), srcLocation, srcCentroid, int(dest), destLocation, msg)

def __createPacket(packetSendingDetails, inInfMode):
    src = packetSendingDetails[0]
    srcLocation = packetSendingDetails[1]
    srcCentroid = packetSendingDetails[2]
    dest = packetSendingDetails[3]
    destLocation = packetSendingDetails[4]
    msg = packetSendingDetails[5]

    packet = Packet(src, srcLocation, srcCentroid, dest, destLocation, msg)

    if inInfMode:
        srcNode = main.__nodeService.getNodeByID(src)
        srcNode.setInfDetailsOfPacket(packet)

    return packet

# WIP
def __createNakPacket(packet, inInfMode, sourceId):
    srcNode = main.__nodeService.getNodeByID(sourceId)
    packet = Packet(sourceId, srcNode.getLocation(), srcNode.getCentroid(), packet.srcId, packet.srcLocation, packet.message)
    packet.setNak(True)
    if inInfMode:
        packet.setInfMode(InfMode.TO_INF)
        packet.setIntermediateLocation(srcNode.getLocation())

    return packet

def __getHelperText():
    return "Restart: [{}] \n".format(Configuration.RESTART_KEY) + \
           "Move: [{}] \n".format(Configuration.MOVEMENT_KEY) + \
           "Basic routing: [{}] \n".format(Configuration.BASIC_ROUTING_KEY) + \
           "Location proxy routing: [{}] \n".format(Configuration.LOCATION_PROXY_ROUTING_KEY) + \
           "Turn intermediate node forwarding on: [{}]\n".format(Configuration.TURN_INTERMEDIATE_NODE_FORWARDING_ON_KEY) + \
           "Toggle automatic simulation: [{}]".format(Configuration.TOGGLE_AUTOMATIC_SIMULATION_KEY)

try:
    main()
except Exception as ex:
    LogService.log(traceback.format_exc())