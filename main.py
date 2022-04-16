from Configurations import Configuration
from Models.Packet import Packet
from Services.GuiService import GuiService
from Services.NodesService import NodesService
from Services.RoutingService import RoutingService
from Services.LogService import LogService

import traceback

__nodeService = None
__routingService = None

def main(x = None, y = None, event = None):
    # initialization
    # reinitialization
    main.__nodeService = NodesService()
    main.__routingService = RoutingService(main.__nodeService)
    main.__routingService.updateRoutingTables()
    main.__nodeService.printRoutingTables()
    __ui.renderNodes(main.__nodeService.getNodes().values())
    __ui.loop()

def __move(x = None, y = None, event = None):
    main.__nodeService.incurNodeMovements()
    main.__routingService.updateRoutingTables()
    __ui.renderNodes(main.__nodeService.getNodes().values())
    main.__nodeService.printRoutingTables()

# for testing purposes
def __basicRouting(event):
    LogService.log('\nBasic Forwarding\n')
    main.__routingService.forwardBasic(__createPacket())

# for testing purposes
def __locationProxyRouting(event):
    LogService.log('\nLocation Proxy Forwarding\n')
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

__ui = GuiService(
    Configuration.GUI_WINDOW_WIDTH,
    Configuration.GUI_WINDOW_HEIGHT,
    main,
    __move,
    __basicRouting,
    __locationProxyRouting,
    __turnLocationProxyOn,
    __turnLocationProxyOff
)

def __createPacket():
    src = input('Source: ')
    # Source may or may not know its own location
    srcLocation = main.__nodeService.getNodes()[int(src)].getLocation()
    dest = input('Destination: ')
    # Destination location is always known, since we are using locations as addresses
    destLocation = main.__nodeService.getNodes()[int(dest)].getCentroid()
    msg = input('Message: ')
    return Packet(int(src), srcLocation, int(dest), destLocation, msg)

try:
    main()
except Exception as ex:
    LogService.log(traceback.format_exc())