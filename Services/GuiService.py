from tkinter import *

from Configurations import Configuration
from Constants import NodeType

class GuiService:

    def __init__(self, width, height, start, move):

        self.window = Tk()
        self.window.title(Configuration.GUI_WINDOW_TITLE)
        self.window.geometry('{}{}{}'.format(width, "x", height))
        self.window.resizable(False, False)

        self.canvas = Canvas(self.window)
        self.canvas.pack(fill = BOTH, expand = 1)

        self.window.bind(Configuration.RESTART_KEY, start)
        self.window.bind(Configuration.MOVEMENT_KEY, move)

    def loop(self):
        self.window.mainloop()

    def renderNodes(self, nodes):
        self.canvas.delete("all")
        # A
        i = 65
        for node in nodes:
            self.drawCircle(
                node.getCentroid().x,
                node.getCentroid().y,
                node.getShapeRadius(),
                f = "#fff"
            )
            self.drawCircle(
                node.getCentroid().x,
                node.getCentroid().y,
                node.getBroadcastRange(),
                c = "#ccc"
            )

            fillColor = Configuration.WRONGLY_INITIALIZED_NODE_COLOR

            if node.getType() == NodeType.LOCATION_AWARE:
                fillColor = Configuration.LOCATION_AWARE_NODE_COLOR
            else:
                fillColor = Configuration.LOCATION_IGNORANT_NODE_COLOR

            self.canvas.create_text(
                node.getCentroid().x,
                node.getCentroid().y,
                fill = fillColor,
                font = Configuration.FONT,
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