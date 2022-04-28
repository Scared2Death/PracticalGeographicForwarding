from Configurations import Configuration

from Models.Packet import Packet

from Services.GuiService import GuiService
from Services.NodesService import NodesService
from Services.RoutingService import RoutingService
from Services.LogService import LogService

import traceback

__nodeService : NodesService = None
__routingService : RoutingService = None

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

# for testing purposes
def __basicRouting(event):
    # LogService.log('\nBasic Forwarding\n')

    main.__routingService.forwardBasic(__createPacket())

# for testing purposes
def __locationProxyRouting(event):
    # LogService.log('\nLocation Proxy Forwarding\n')
    main.__routingService.forwardLocationProxy(__createPacket())

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

def __createPacket():
    src = input('Source: ')
    # Source may or may not know its own location
    srcLocation = main.__nodeService.getNodes()[int(src)].getLocation()
    dest = input('Destination: ')
    # Destination location is always known, since we are using locations as addresses
    destLocation = main.__nodeService.getNodes()[int(dest)].getCentroid()
    msg = input('Message: ')

    packet = Packet(int(src), srcLocation, int(dest), destLocation, msg)
    packet.setCentroid(srcLocation)

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