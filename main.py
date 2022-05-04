from Configurations import Configuration

from Models.Packet import Packet

from Services.GuiService import GuiService
from Services.NodesService import NodesService
from Services.RoutingService import RoutingService
from Services.LogService import LogService

from tkinter import simpledialog

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

    # due to reinitialization
    __reset()

    main.__nodeService = NodesService()
    main.__routingService = RoutingService(main.__nodeService, False)
    # main.__nodeService.printRoutingTables()

    __ui.render(main.__nodeService.getNodes().values(), __getHelperText())
    __ui.window.after(Configuration.DELAY_INTERVAL, __incurAutomaticSimulation)
    __ui.loop()

def __reset():
    global __isNewSendingInitiatable
    global __isSendingInProgress
    global __packet
    global __packetLocations
    global __nextHop
    global __routingResult
    global __isRenderingINFNodes

    __isNewSendingInitiatable = True
    __isSendingInProgress = False

    __packet = None
    __packetLocations = []
    __nextHop = None
    __routingResult = None

    __isRenderingINFNodes = False

def __toggleAutomaticSimulation(event):
    global __isAutomaticSimulation
    __isAutomaticSimulation = not __isAutomaticSimulation

def __incurAutomaticSimulation():
    if __isAutomaticSimulation:
        __move()

    __ui.window.after(Configuration.DELAY_INTERVAL, __incurAutomaticSimulation)

def __move(x = None, y = None, event = None):
    global __nextHop
    global __isSendingInProgress
    global __isNewSendingInitiatable
    global __routingResult

    main.__nodeService.incurNodeMovements()
    main.__routingService.updateRoutingTables()

    if __isSendingInProgress:

        __routingResult = []

        if __nextHop is None:
            __prevNextHop = __packet.getSrcId()
            __nextHop = __routing(__packet)
        else:
            __prevNextHop = __nextHop
            __nextHop = __routing(__packet, __nextHop)

        if __nextHop is not None and __nextHop != 'NAK' and __packet.getDestId() != __nextHop:
            __packetLocations.append((__nextHop, main.__nodeService.getNodeByID(__nextHop).getCentroid()))
            LogService.log('Next hop: {}'.format(__nextHop))
            __routingResult.append('Next hop: {}'.format(__nextHop))
            __routingResult.append(None)
        else:
            if __nextHop == 'NAK':
                __routingResult.append('Packet is returned to sender.')
                # todo
            elif __packet.getDestId() != __nextHop:
                LogService.log('Packet is dropped :(')
                __routingResult.append('Packet is dropped :(')
                __routingResult.append(False)
            else:
                __packetLocations.append((__nextHop, main.__nodeService.getNodeByID(__nextHop).getCentroid()))
                LogService.log('Packet is delivered at node {} :)'.format(__nextHop))
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
    __packetLocations.append((__packet.getSrcId(), __packet.getSrcCentroid()))

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
    __packetLocations.append((__packet.getSrcId(), __packet.getSrcCentroid()))

# WIP
def __initiateInfRoutingSending(event):

    # if not checkNewSendingInitiatability():
    #     return
    #
    packetSendingDetails = __askForPacketSendingDetails()
    #
    # # UI WINDOW OR WHATEVER
    # if packetSendingDetails is None:
    #     LogService.log("Wrongful inputs provided .")
    #     global __isNewSendingInitiatable
    #     __isNewSendingInitiatable = True
    #     return
    #
    # __packetLocations.clear()
    #
    # global __isSendingInProgress
    # __isSendingInProgress = True

    main.__routingService.setInInfMode(True)
    # main.__nodeService.printRoutingTables()

    # global __packet
    # __packet = __createPacket(packetSendingDetails, True)
    # __packetLocations.append((__packet.getSrcId(), __packet.getSrcCentroid()))

    packet = __createPacket(packetSendingDetails, True)
    __doInfRouting(packet)

def __doInfRouting(packet):
    isNak = packet.isNak()
    prevHop = packet.getSrcId()
    nextHop = __routing(packet)
    while nextHop != packet.getDestId() and nextHop is not None and nextHop != 'NAK':
        prevHop = nextHop
        nextHop = __routing(packet, nextHop)
        LogService.log('NextHop {}'.format(nextHop))

    if nextHop == packet.getDestId():
        if isNak:
            LogService.log('Packet returned to source.')
            srcNode = main.__nodeService.getNodeByID(nextHop)
            repeat = srcNode.handleNakPacket()
            if repeat:
                __doInfRouting(srcNode.getPacket())
            else:
                LogService.log('Too many failed attempts.')
        else:
            LogService.log('Packet delivered.')
    elif nextHop == 'NAK':
        if isNak:
            LogService.log('Cannot return NAK message')
        else:
            LogService.log('Return NAK to sender.')
            nakSender = main.__nodeService.getNodeByID(prevHop)
            nakPacket = nakSender.createNakPacket(packet)
            __doInfRouting(nakPacket)
    else:
        LogService.log('Delivery failed')

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
    Configuration.MAIN_WINDOW_WIDTH,
    Configuration.MAIN_WINDOW_HEIGHT,
    main,
    __move,
    __initiateBasicRoutingSending,
    __initiateLocationProxyRoutingSending,
    __initiateInfRoutingSending,
    __turnIntermediateNodeForwardingOn,
    __turnIntermediateNodeForwardingOff,
    __toggleAutomaticSimulation)

def __askForPacketSendingDetails():
    src = simpledialog.askstring(
        "From",
        "Enter source node ID",
        parent = __ui.window
    )
    # Source may or may not know its own location
    # srcCentroid => needed for visualization

    if int(src) in main.__nodeService.getNodes():
        srcLocation = main.__nodeService.getNodeByID(int(src)).getCentroid()
        srcCentroid = main.__nodeService.getNodeByID(int(src)).getCentroid()
    else:
        return None

    dest = simpledialog.askstring(
        "To",
        "Enter destination node ID",
        parent = __ui.window
    )
    # Destination location is always known, since we are using locations as addresses

    if int(dest) in main.__nodeService.getNodes():
        destLocation = main.__nodeService.getNodeByID(int(dest)).getCentroid()
    else:
        return None

    msg = simpledialog.askstring(
        "Message",
        "Enter message to send",
        parent = __ui.window
    )

    return (int(src), srcLocation, srcCentroid, int(dest), destLocation, msg)

def __createPacket(packetSendingDetails, inInfMode):
    src = packetSendingDetails[0]
    srcLocation = packetSendingDetails[1]
    srcCentroid = packetSendingDetails[2]
    dest = packetSendingDetails[3]
    destLocation = packetSendingDetails[4]
    msg = packetSendingDetails[5]

    packet = Packet(src, srcLocation, srcCentroid, dest, destLocation, msg)

    srcNode = main.__nodeService.getNodeByID(src)
    srcNode.setPacket(packet)
    if inInfMode:
        srcNode.setInfDetailsOfPacket()
        srcNode.setAttempt(1)

    return packet

def __getHelperText():
    return "{}  Restart\n\n".format(Configuration.RESTART_KEY_DISPLAY) + \
           "{}  Move\n\n".format(Configuration.MOVEMENT_KEY_DISPLAY) + \
           "{}  Turn INF on\n\n".format(Configuration.TURN_INTERMEDIATE_NODE_FORWARDING_ON_KEY_DISPLAY) + \
           "{}  Send (Basic)\n\n".format(Configuration.BASIC_ROUTING_KEY_DISPLAY) + \
           "{}  Send (Location proxy)\n\n".format(Configuration.LOCATION_PROXY_ROUTING_KEY_DISPLAY) + \
           "{}  Send (INF)\n\n".format(Configuration.INF_ROUTING_KEY_DISPLAY) + \
           "{}  Toggle automatic".format(Configuration.TOGGLE_AUTOMATIC_SIMULATION_KEY_DISPLAY)

try:
    main()
except Exception as ex:
    LogService.log(traceback.format_exc())