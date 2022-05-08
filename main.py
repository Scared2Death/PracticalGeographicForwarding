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

__isRepeatedRouting = False
__infExtrasData = None
__infExtrasForRendering = None
__initiateRouting = False
__isNak = False

__isAutomaticSimulation = Configuration.IS_AUTOMATIC_SIMULATION_ENABLED_BY_DEFAULT

def main(x = None, y = None, event = None):
    __resetToDefaultValues()

    main.__nodeService = NodesService()
    main.__routingService = RoutingService(main.__nodeService, False)

    __ui.render(main.__nodeService.getNodes().values(), __getHelperText())
    __ui.window.after(Configuration.DELAY_INTERVAL, __incurAutomaticSimulation)
    __ui.loop()

def __resetToDefaultValues():
    global __isNewSendingInitiatable
    global __isSendingInProgress
    global __packet
    global __packetLocations
    global __nextHop
    global __routingResult
    global __isRenderingINFNodes
    global __isRepeatedRouting
    global __infExtrasData
    global __infExtrasForRendering
    global __initiateRouting
    global __isNak

    __isNewSendingInitiatable = True
    __isSendingInProgress = False

    __packet = None
    __packetLocations = []
    __nextHop = None
    __routingResult = None

    __isRenderingINFNodes = False

    __isRepeatedRouting = False
    __infExtrasData = None
    __infExtrasForRendering = None
    __initiateRouting = False

    __isNak = False
    LogService.clearFileContents()

def __indicateRoutingReset():
    global __isNewSendingInitiatable
    global __isSendingInProgress
    global __nextHop

    __isNewSendingInitiatable = True
    __isSendingInProgress = False

    __nextHop = None

def __toggleAutomaticSimulation(event):
    global __isAutomaticSimulation
    __isAutomaticSimulation = not __isAutomaticSimulation

def __incurAutomaticSimulation():
    if __isAutomaticSimulation:
        __move()

    __ui.window.after(Configuration.DELAY_INTERVAL, __incurAutomaticSimulation)

def __move(x = None, y = None, event = None):
    global __isRenderingINFNodes
    global __nextHop
    global __isSendingInProgress
    global __isNewSendingInitiatable
    global __routingResult
    global __packet
    global __packetLocations
    global __isRepeatedRouting
    global __infExtrasForRendering
    global __infExtrasData
    global __initiateRouting
    global __isNak

    if not __isRenderingINFNodes:
        main.__nodeService.incurNodeMovements()

    main.__routingService.updateRoutingTables()

    if __isSendingInProgress:

        __routingResult = []

        if __isRepeatedRouting:
            __infExtrasForRendering = __infExtrasData
            index = len(__packetLocations) - 1
            __packetLocations = __packetLocations[index:]
            __isRepeatedRouting = False
            __isNak = __packet.isNak()
            __routingResult.append('Node {} starts routing'.format(__packet.getSrcId()))
            __routingResult.append(None)

        else:

            if not __isRenderingINFNodes and not main.__routingService.isInInfMode():
                if __nextHop is None:
                    __nextHop = __routing(__packet)
                else:
                    __nextHop = __routing(__packet, __nextHop)

                if __nextHop is not None and __packet.getDestId() != __nextHop:
                    __packetLocations.append((__nextHop, main.__nodeService.getNodeByID(__nextHop).getCentroid()))
                    LogService.log('Next hop: {}'.format(__nextHop))
                    __routingResult.append('Next hop: {}'.format(__nextHop))
                    __routingResult.append(None)
                else:
                    if __packet.getDestId() != __nextHop:
                        __routingResult.append('Packet is dropped :(')
                        __routingResult.append(False)
                        LogService.log('::::::::ROUTING FROM {} TO {} FAILED::::::::'.format(__packet.getSrcId(), __packet.getDestId()))
                    else:
                        __packetLocations.append((__nextHop, main.__nodeService.getNodeByID(__nextHop).getCentroid()))

                        msg = "Packet is delivered at node"
                        __routingResult.append('{} {} :)'.format(msg, __nextHop))
                        __routingResult.append(True)
                        LogService.log('::::::::ROUTING FROM {} TO {} COMPLETED::::::::'.format(__packet.getSrcId(), __packet.getDestId()))
                    __indicateRoutingReset()
            else:
                if __nextHop is None:
                    __prevNextHop = __packet.getSrcId()
                    __nextHop = __routing(__packet)
                else:
                    __prevNextHop = __nextHop
                    __nextHop = __routing(__packet, __nextHop)

                if __nextHop != __packet.getDestId() and __nextHop is not None and __nextHop != 'NAK':
                    __packetLocations.append((__nextHop, main.__nodeService.getNodeByID(__nextHop).getCentroid()))
                    LogService.log('Next hop: {}'.format(__nextHop))
                    __routingResult.append('Next hop: {}'.format(__nextHop))
                    __routingResult.append(None)
                else:
                    if __packet.getDestId() == __nextHop:
                        if __packet.isNak():
                            LogService.log('::::::::RETURNING PACKET FROM {} TO {} COMPLETED::::::::'.format(__packet.getSrcId(), __packet.getDestId()))

                            __packetLocations.append((__nextHop, main.__nodeService.getNodeByID(__nextHop).getCentroid()))

                            srcNode = main.__nodeService.getNodeByID(__nextHop)
                            repeat = srcNode.handleNakPacket()

                            if repeat:
                                msg = "Packet returned to source"
                                __routingResult.append('{} {}'.format(msg, __nextHop))
                                __routingResult.append(None)
                                __isRepeatedRouting = True
                                __initiateRouting = True

                                __packet = srcNode.getPacket()
                                __packetLocations.append((__packet.getSrcId(), __packet.getSrcCentroid()))

                                LogService.log('::::::::{} RESENDING TO {}::::::::'.format(__packet.getSrcId(), __packet.getDestId()))

                                __nextHop = None

                                __infExtrasData = srcNode.getInfExtras(__packet, True)
                                __infExtrasForRendering = None

                            else:
                                msg = "Nak pocket cannot be handled: too many attempts or no location info"
                                LogService.log('::::::::ROUTING FROM {} TO {} FAILED (TOO MANY ATTEMPTS OR NO LOCATION INFO)::::::::'.format(__packet.getSrcId(), __packet.getDestId()))
                                __routingResult.append('{}'.format(msg))
                                __routingResult.append(False)

                                __indicateRoutingReset()
                        else:
                            __packetLocations.append((__nextHop, main.__nodeService.getNodeByID(__nextHop).getCentroid()))
                            msg = "Packet is delivered at node"
                            LogService.log('::::::::RETURNING PACKET FROM {} TO {} COMPLETED::::::::'.format(__packet.getSrcId(), __packet.getDestId()))
                            __routingResult.append('{} {} :)'.format(msg, __nextHop))
                            __routingResult.append(True)

                            __indicateRoutingReset()
                    elif __nextHop == 'NAK':
                        if __packet.isNak():
                            msg = 'Cannot return NAK message'
                            __routingResult.append('{}'.format(msg))
                            __routingResult.append(False)
                            LogService.log('::::::::ROUTING FROM {} TO {} FAILED::::::::'.format(__packet.getSrcId(), __packet.getDestId()))
                            __indicateRoutingReset()
                        else:
                            msg = 'Returning NAK to sender.'
                            __routingResult.append('{}'.format(msg))
                            __routingResult.append(None)

                            nakSender = main.__nodeService.getNodeByID(__prevNextHop)
                            __packet = nakSender.createNakPacket(__packet)

                            __isRepeatedRouting = True
                            __initiateRouting = True

                            __packetLocations.append((__packet.getSrcId(), __packet.getSrcCentroid()))

                            __nextHop = None
                            __infExtrasData = nakSender.getInfExtras(__packet, False)
                            __infExtrasForRendering = None
                            LogService.log('::::::::{} RETURNING NAK TO {}::::::::'.format(__packet.getSrcId(), __packet.getDestId()))

                    else:
                        msg = 'Delivery failed'
                        LogService.log('::::::::ROUTING FROM {} TO {} FAILED::::::::'.format(__packet.getSrcId(), __packet.getDestId()))
                        __routingResult.append(msg)
                        __routingResult.append(False)

                        __indicateRoutingReset()
    else:
        if len(__packetLocations) != 0:
            __packetLocations.clear()
            __infExtrasData = None
            __infExtrasForRendering = None
        __routingResult = None

    __ui.render(main.__nodeService.getNodes().values(), __getHelperText(), __packetLocations,
                routingResult = __routingResult,
                infExtrasForRendering = __infExtrasForRendering, isNak = __isNak)

    LogService.debug('::::::::ROUTING TABLES::::::::\n{}\n:::::::::::::::::::::::::'.format(main.__nodeService.printRoutingTables()))

def checkNewSendingInitiatability():
    global __isNewSendingInitiatable
    if not __isNewSendingInitiatable:
        LogService.log("A new sending is not initiatable. A current sending process is being carried out.")
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
        LogService.log("Wrongful inputs provided.")
        global __isNewSendingInitiatable
        __isNewSendingInitiatable = True
        return

    __packetLocations.clear()

    global __isSendingInProgress
    __isSendingInProgress = True

    main.__routingService.setInLocationProxyMode(False)

    global __packet
    __packet = __createPacket(packetSendingDetails, False)
    __packetLocations.append((__packet.getSrcId(), __packet.getSrcCentroid()))

    global __routingResult
    __routingResult = []
    __routingResult.append('Node {} starts routing'.format(__packet.getSrcId()))
    __routingResult.append(None)

    global __isNak
    __isNak = __packet.isNak()

    LogService.log('::::::::{} SENDING TO {} IN BASIC MODE::::::::'.format(__packet.getSrcId(), __packet.getDestId()))

    __ui.render(main.__nodeService.getNodes().values(), __getHelperText(), __packetLocations,
                routingResult = __routingResult)

def __initiateLocationProxyRoutingSending(event):

    if not checkNewSendingInitiatability():
        return

    packetSendingDetails = __askForPacketSendingDetails()

    # UI WINDOW OR WHATEVER
    if packetSendingDetails is None:
        LogService.log("Wrongful inputs provided.")
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

    global __routingResult
    __routingResult = []
    __routingResult.append('Node {} starts routing'.format(__packet.getSrcId()))
    __routingResult.append(None)

    global __isNak
    __isNak = __packet.isNak()

    LogService.log('::::::::{} SENDING TO {} IN LOCATION PROXY MODE::::::::'.format(__packet.getSrcId(), __packet.getDestId()))
    __ui.render(main.__nodeService.getNodes().values(), __getHelperText(), __packetLocations,
                routingResult = __routingResult)

# WIP
def __initiateInfRoutingSending(event):

    if not checkNewSendingInitiatability():
        return

    packetSendingDetails = __askForPacketSendingDetails()
    # UI WINDOW OR WHATEVER
    if packetSendingDetails is None:
         LogService.log("Wrongful inputs provided.")
         global __isNewSendingInitiatable
         __isNewSendingInitiatable = True
         return

    __packetLocations.clear()

    global __isSendingInProgress
    __isSendingInProgress = True

    # if not False, inf cannot be demonstrated, because in inf mode, all aware nodes are propagated
    # global __isRenderingINFNodes
    if __isRenderingINFNodes:
        main.__routingService.setInLocationProxyMode(False)
    main.__routingService.setInInfMode(True)
    # main.__nodeService.printRoutingTables()

    global __packet
    __packet = __createPacket(packetSendingDetails, True)
    __packetLocations.append((__packet.getSrcId(), __packet.getSrcCentroid()))

    global __routingResult
    __routingResult = []
    __routingResult.append('Node {} starts routing'.format(__packet.getSrcId()))
    __routingResult.append(None)

    global __isNak
    __isNak = __packet.isNak()

    LogService.log('::::::::{} SENDING TO {} IN INF MODE::::::::'.format(__packet.getSrcId(), __packet.getDestId()))
    __ui.render(main.__nodeService.getNodes().values(), __getHelperText(), __packetLocations,
                routingResult = __routingResult)

def __routing(packet, nextHop = None):
    if nextHop is None:
        nextHop = main.__routingService.getNextHopInRoute(packet)
    else:
        nextHop = main.__routingService.getNextHopInRoute(packet, nextHop)

    return nextHop

def __turnIntermediateNodeForwardingOn(event):
    __resetToDefaultValues()
    infNodes = main.__nodeService.getINFNodes().values()

    global __isRenderingINFNodes
    __isRenderingINFNodes = True

    __ui.render(infNodes, __getHelperText(), __packetLocations, __isRenderingINFNodes)

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

    return (int(src), srcLocation, srcCentroid, int(dest), destLocation)

def __createPacket(packetSendingDetails, inInfMode):
    src = packetSendingDetails[0]
    srcLocation = packetSendingDetails[1]
    srcCentroid = packetSendingDetails[2]
    dest = packetSendingDetails[3]
    destLocation = packetSendingDetails[4]

    packet = Packet(src, srcLocation, srcCentroid, dest, destLocation)

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