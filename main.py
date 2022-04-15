from Configurations import Configuration
from Models.Packet import Packet
from Services.GuiService import GuiService
from Services.NodesService import NodesService
from Services.RoutingService import RoutingService
from Services.LogService import LogService

import traceback

__nodeService = None

def main(x = None, y = None, event = None):
    # initialization
    # reinitialization
    main.__nodeService = NodesService()
    main.__nodeService.setWithLocProxy(True)
    main.__nodeService.getNodes()
    main.__nodeService.printRoutingTables()
    __ui.renderNodes(main.__nodeService.getNodes().values())
    __ui.loop()

def __move(x = None, y = None, event = None):
    main.__nodeService.incurNodeMovements()
    __ui.renderNodes(main.__nodeService.getNodes().values())
    main.__nodeService.printRoutingTables()


# for testing purposes
def __basicRouting(event):
    src = input('source: ')
    # Source may or may not know its own location
    srcLocation = main.__nodeService.getNodes()[int(src)].getLocation()
    dest = input('dest: ')
    # Destination location is always known, since we are using locations as addresses
    destLocation = main.__nodeService.getNodes()[int(dest)].getCentroid()
    msg = input('msg: ')
    packet = Packet(int(src), srcLocation, int(dest), destLocation, msg)
    RoutingService.forwardBasic(main.__nodeService, packet)


__ui = GuiService(
    Configuration.GUI_WINDOW_WIDTH,
    Configuration.GUI_WINDOW_HEIGHT,
    main,
    __move,
    __basicRouting
)

try:
    main()
except Exception as ex:
    LogService.log(traceback.format_exc())