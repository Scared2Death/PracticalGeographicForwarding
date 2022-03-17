from tkinter import *

import random

from Configurations import configuration

class guiService():

    def __init__(self, width, height, start):
        self.window = Tk(className = "simulation")
        self.window.title(configuration.GUI_WINDOW_TITLE)
        self.window.geometry(
            '{}{}{}'.format(width, "x", height)
        )
        self.window.resizable(False, False)
        self.canvas = Canvas(self.window)
        self.canvas.pack(fill = BOTH, expand = 1)
        self.window.bind_all("<Return>", start)

    def loop(self):
        self.window.mainloop()

    def renderNodes(self, nodes):
        self.canvas.delete("all")
        # A
        i = 65
        for node in nodes:
            self.drawCircle(
                node.centroid.x,
                node.centroid.y,
                node.shapeRadius,
                f = "#fff"
            )
            self.drawCircle(
                node.centroid.x,
                node.centroid.y,
                node.broadcastRange,
                c = "#ccc"
            )

            self.canvas.create_text(
                node.centroid.x,
                node.centroid.y,
                fill = configuration.LOCATION_IGNORANT_NODE_COLOR if random.choice([True, False]) else configuration.LOCATION_AWARE_NODE_COLOR,
                font = configuration.FONT,
                text = chr(i)
            )
            i = i + 1

    def drawCircle(self, x, y, r, c ="#000", f =""):
        return self.canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill = f,
            outline = c
        )