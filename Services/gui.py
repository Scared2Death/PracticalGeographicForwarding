from tkinter import *
import random

class gui():

    def __init__(self, width, height, start):
        self.window = Tk(className="Simulation")
        self.window.geometry(
            '{}{}{}'.format(width, "x", height)
        )
        self.canvas = Canvas(self.window)
        self.canvas.pack(fill = BOTH, expand = 1)
        self.window.bind_all("<Return>", start)

    def loop(self):
        self.window.mainloop()

    def renderNodes(self, nodes):
        self.canvas.delete("all")
        i = 65
        for node in nodes:
            self.circle(
                node.centroid.x,
                node.centroid.y,
                node.broadcastRange,
                c = "#ccc"
            )
            self.circle(
                node.centroid.x,
                node.centroid.y,
                node.shapeRadius,
                f = "#fff"
            )
            self.canvas.create_text(
                node.centroid.x,
                node.centroid.y,
                fill = "green" if random.choice([True, False]) else "black",
                font = "Arial 21 bold",
                text = chr(i)
            )
            i = i + 1

    def circle(self, x, y, r, c = "#000", f = ""):
        return self.canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill = f,
            outline = c
        )