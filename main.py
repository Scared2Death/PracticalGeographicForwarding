from Configurations import Configuration

from Models.Packet import Packet

from Services.GuiService import GuiService
from Services.NodesService import NodesService
from Services.RoutingService import RoutingService
from Services.LogService import LogService

import traceback

__nodeService : NodesService = None
__routingService : RoutingService = None

__isNewSendingInitiatable = True
packetLocations = []

__isAutomaticSimulation = Configuration.IS_AUTOMATIC_SIMULATION_ENABLED_BY_DEFAULT

def main(x = None, y = None, event = None):
    # initialization
    # reinitialization

    main.__nodeService = NodesService()
    main.__routingService = RoutingService(main.__nodeService)
    main.__routingService.updateRoutingTables()
    main.__nodeService.printRoutingTables()

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
    main.__nodeService.incurNodeMovements()
    main.__routingService.updateRoutingTables()

    __ui.render(main.__nodeService.getNodes().values(), __getHelperText())

    # main.__nodeService.printRoutingTables()

def __basicRouting(event):
    packetSendingDetails = __askForPacketSendingDetails()
    packet = __createPacket(packetSendingDetails)
    # LogService.log('\nBasic Forwarding\n')

    packetLocations.clear()

    nextHop = main.__routingService.getBasicForwardNextHop(packet)
    while nextHop is not None and packet.destId != nextHop:
        LogService.log('Next hop: {}'.format(nextHop))
        nextHop = main.__routingService.getBasicForwardNextHop(packet, nextHop)

    if packet.destId != nextHop:
        LogService.log('Packet is dropped :(')
    else:
        LogService.log('Packet is delivered at node {} :)'.format(nextHop))

def __locationProxyRouting(event):
    packetSendingDetails = __askForPacketSendingDetails()
    packet = __createPacket(packetSendingDetails)
    # LogService.log('\nLocation Proxy Forwarding\n')
    routingResults = main.__routingService.forwardLocationProxy(packet)


def __turnLocationProxyOn(event):
    main.__nodeService.setWithLocationProxy(True)
    LogService.log('Location Proxy mode is on')
    main.__routingService.updateRoutingTables()
    main.__nodeService.printRoutingTables()

def __turnLocationProxyOff(event):
    main.__nodeService.setWithLocationProxy(False)
    LogService.log('Location Proxy mode is off')
    main.__routingService.clearRoutingTables()
    main.__routingService.updateRoutingTables()
    main.__nodeService.printRoutingTables()

def __turnIntermediateNodeForwardingOn(event):

    infNodes = main.__nodeService.getINFNodes().values()

    isRenderingINFNodes = True
    __ui.render(infNodes, __getHelperText(), isRenderingINFNodes)

    # other todos ...

__ui = GuiService(
    Configuration.GUI_WINDOW_WIDTH,
    Configuration.GUI_WINDOW_HEIGHT,
    main,
    __move,
    __basicRouting,
    __locationProxyRouting,
    __turnLocationProxyOn,
    __turnLocationProxyOff,
    __turnIntermediateNodeForwardingOn,
    __toggleAutomaticSimulation)

def __askForPacketSendingDetails():
    src = input('Source: ')
    # Source may or may not know its own location
    srcLocation = main.__nodeService.getNodes()[int(src)].getLocation()
    dest = input('Destination: ')
    # Destination location is always known, since we are using locations as addresses
    destLocation = main.__nodeService.getNodes()[int(dest)].getCentroid()
    msg = input('Message: ')

    return (int(src), srcLocation, int(dest), destLocation, msg)

def __createPacket(packetSendingDetails):
    src = packetSendingDetails[0]
    srcLocation = packetSendingDetails[1]
    dest = packetSendingDetails[2]
    destLocation = packetSendingDetails[3]
    msg = packetSendingDetails[4]

    packet = Packet(src, srcLocation, dest, destLocation, msg)
    packet.setLocation(srcLocation)

    return packet

def __getHelperText():
    return "Restart: [{}] \n".format(Configuration.RESTART_KEY) + \
           "Move: [{}] \n".format(Configuration.MOVEMENT_KEY) + \
           "Basic routing: [{}] \n".format(Configuration.BASIC_ROUTING_KEY) + \
           "Location proxy routing: [{}] \n".format(Configuration.LOCATION_PROXY_ROUTING_KEY) + \
           "Turn location proxy on: [{}] \n".format(Configuration.LOCATION_PROXY_ON_KEY) + \
           "Turn location proxy off: [{}]\n".format(Configuration.LOCATION_PROXY_OFF_KEY) + \
           "Turn intermediate node forwarding on: [{}]\n".format(Configuration.INTERMEDIATE_NODE_FORWARDING_KEY) + \
           "Toggle automatic simulation: [{}]".format(Configuration.TOGGLE_AUTOMATIC_SIMULATION_KEY)

try:
    main()
except Exception as ex:
    LogService.log(traceback.format_exc())