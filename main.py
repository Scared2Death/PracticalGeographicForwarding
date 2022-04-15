import traceback
from Configurations import Configuration
from Models.Packet import Packet

from Services.GuiService import GuiService
from Services.NodesService import NodesService
from Services.RoutingService import RoutingService

__nodeService = None

def main(x = None, y = None, event = None):
    # initialization
    # reinitialization
    main.__nodeService = NodesService()
    RoutingService.initRoutingTables(main.__nodeService)
    RoutingService.updateRoutingTables(main.__nodeService, False)
    main.__nodeService.printRoutingTables()
    __ui.renderNodes(main.__nodeService.getNodes().values())
    __ui.loop()

def __move(x = None, y = None, event = None):
    main.__nodeService.incurNodeMovements()
    RoutingService.updateRoutingTables(main.__nodeService, False)
    __ui.renderNodes(main.__nodeService.getNodes().values())


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
    print(traceback.format_exc())