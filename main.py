from Configurations import configuration

import Services.utilities as utilities
from Services.gui import gui

def initNodes():
    for _ in range(10):
        yield utilities.utilities.generateNode()

def start(ui):
    ui.renderNodes(
        initNodes()
    )

def main(x = None, y = None, event = None):
    start(ui)
    ui.loop()

ui = gui(
    configuration.GUI_WINDOW_WIDTH,
    configuration.GUI_WINDOW_HEIGHT,
    main
)

main()