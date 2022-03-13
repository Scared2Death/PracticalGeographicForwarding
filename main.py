from tkinter import *

from Configurations import configuration

import Services.utilities as utilities

def __renderGUIWindow():
    guiWindow = Tk(className="Simulation")

    guiWindowScale = '{}{}{}'.format(configuration.GUI_WINDOW_WIDTH, "x", configuration.GUI_WINDOW_HEIGHT)
    guiWindow.geometry(guiWindowScale)

    myCanvas = Canvas(guiWindow)
    myCanvas.pack()

    myCanvas.create_oval(10, 20, 50, 80)

    guiWindow.mainloop()

def __initializeNodes():
    for i in range(utilities.utilities.generateRandomInt(10, 25)):
        node = utilities.utilities.generateNode()
        nodeDescription = node.getDescription()
        print(nodeDescription)

__initializeNodes()
__renderGUIWindow()