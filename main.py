from Configurations import configuration

from Services.guiService import guiService
from Services.nodesService import nodesService

def __start():
    __ui.renderNodes(nodesService().getNodes())

def main(x = None, y = None, event = None):
    __start()
    __ui.loop()

__ui = guiService(
    configuration.GUI_WINDOW_WIDTH,
    configuration.GUI_WINDOW_HEIGHT,
    main
)

try:
    main()
except Exception as ex:
    print(ex)