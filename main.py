from Configurations import Configuration

from Services.GuiService import GuiService
from Services.NodesService import NodesService

__nodeService = None

def main(x = None, y = None, event = None):
    # initialization
    # reinitialization
    main.__nodeService = NodesService()

    __ui.renderNodes(main.__nodeService.getNodes())
    __ui.loop()

def __move(x = None, y = None, event = None):
    main.__nodeService.incurNodeMovements()
    __ui.renderNodes(main.__nodeService.getNodes())

__ui = GuiService(
    Configuration.GUI_WINDOW_WIDTH,
    Configuration.GUI_WINDOW_HEIGHT,
    main,
    __move
)

try:
    main()
except Exception as ex:
    print(ex)