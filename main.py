from tkinter import *

from Configurations import configuration

def renderGUIWindow():
    guiWindow = Tk(className="Simulation")

    guiWindowScale = '{}{}{}'.format(configuration.GUI_WINDOW_WIDTH, "x", configuration.GUI_WINDOW_HEIGHT)
    guiWindow.geometry(guiWindowScale)

    myCanvas = Canvas(guiWindow)
    myCanvas.pack()

    myCanvas.create_oval(10, 20, 50, 80)

    guiWindow.mainloop()


renderGUIWindow()