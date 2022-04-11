from tkinter import *

from Configurations import Configuration
from Constants import NodeType

class GuiService:

    def __init__(self, width, height, start, move, basicRouting):

        self.window = Tk()
        self.window.title(Configuration.GUI_WINDOW_TITLE)
        self.window.geometry('{}{}{}'.format(width, "x", height))
        self.window.resizable(False, False)

        self.canvas = Canvas(self.window)
        self.canvas.pack(fill = BOTH, expand = 1)

        self.window.bind(Configuration.RESTART_KEY, start)
        self.window.bind(Configuration.MOVEMENT_KEY, move)
        self.window.bind(Configuration.BASIC_ROUTING_KEY, basicRouting)

    def loop(self):
        self.window.mainloop()

    def renderNodes(self, nodes):
        self.canvas.delete("all")
        for node in nodes:
            self.drawCircle(
                node.getCentroid().x,
                node.getCentroid().y,
                node.getShapeRadius(),
                f = Configuration.INNER_NODE_FILL_COLOR,
            )
            self.drawCircle(
                node.getCentroid().x,
                node.getCentroid().y,
                node.getBroadcastRange(),
                c = Configuration.OUTER_NODE_FILL_COLOR
            )

            textColor = Configuration.WRONGLY_INITIALIZED_NODE_COLOR

            if node.getType() == NodeType.LOCATION_AWARE:
                textColor = Configuration.LOCATION_AWARE_NODE_COLOR
            else:
                textColor = Configuration.LOCATION_IGNORANT_NODE_COLOR

            self.canvas.create_text(
                node.getCentroid().x,
                node.getCentroid().y,
                fill = textColor,
                font = Configuration.FONT,
                # text = chr(node.getId())
                # for testing purposes
                text = node.getId()
            )

    def drawCircle(self, x, y, r, c = Configuration.NODE_OUTLINE_DEFAULT_COLOR, f = Configuration.NODE_FILL_DEFAULT_COLOR):
        return self.canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill = f,
            outline = c
        )