from tkinter import *

from Configurations import Configuration
from Constants import NodeType

from Models.Packet import Packet

class GuiService:

    def __init__(self, width, height, start, move, basicRouting, locationProxyRouting, turnLocationProxyOn, turnLocationProxyOff,     toggleAutomaticSimulation):

        self.window = Tk()

        self.window.title(Configuration.GUI_WINDOW_TITLE)
        self.window.geometry('{}{}{}'.format(width, "x", height))
        self.window.resizable(False, False)

        self.canvas = Canvas(self.window)
        self.canvas.pack(fill = BOTH, expand = 1)

        self.window.bind(Configuration.RESTART_KEY, start)
        self.window.bind(Configuration.MOVEMENT_KEY, move)
        self.window.bind(Configuration.BASIC_ROUTING_KEY, basicRouting)
        self.window.bind(Configuration.LOCATION_PROXY_ROUTING_KEY, locationProxyRouting)
        self.window.bind(Configuration.LOCATION_PROXY_ON_KEY, turnLocationProxyOn)
        self.window.bind(Configuration.LOCATION_PROXY_OFF_KEY, turnLocationProxyOff)
        self.window.bind(Configuration.TOGGLE_AUTOMATIC_SIMULATION_KEY, toggleAutomaticSimulation)

    def loop(self):
        self.window.mainloop()

    def render(self, nodes, helperText: str):
        # packet: Packet

        # # INITIAL SOMETHING
        # def renderPacket(self, packet: Packet):
        #     self.drawCircle(
        #         packet.getCentroid().x,
        #         packet.getCentroid().y,
        #         Configuration.PACKET_SHAPE_RADIUS,
        #         f=Configuration.PACKET_FILL_COLOR
        #     )

        self.canvas.delete("all")

        for node in nodes:

            isPartOfSomeNetwork = False

            if node.checkNetworkBelonging(nodes):
                nodeShapeFillColor = Configuration.NODE_SHAPE_IN_NETWORK_FILL_COLOR
                nodeBroadcastRangeFillColor = Configuration.NODE_BROADCAST_RANGE_OUTLINE_COLOR
                isPartOfSomeNetwork = True
            else:
                nodeShapeFillColor = Configuration.NODE_SHAPE_OUT_OF_NETWORK_FILL_COLOR
                nodeBroadcastRangeFillColor = Configuration.NODE_BROADCAST_RANGE_OUT_OF_NETWORK_OUTLINE_COLOR

            # NODE SHAPE
                self.drawCircle(
                    node.getCentroid().x,
                    node.getCentroid().y,
                    node.getShapeRadius(),
                    f = nodeShapeFillColor,
                )

            # NODE BROADCAST RANGE
            self.drawCircle(
                node.getCentroid().x,
                node.getCentroid().y,
                node.getBroadcastRange(),
                c = nodeBroadcastRangeFillColor
            )

            textColor = Configuration.WRONGLY_INITIALIZED_NODE_COLOR

            if not isPartOfSomeNetwork:
                textColor = Configuration.LOCATION_AWARE_NODE_COLOR
            else:
                if node.getType() == NodeType.LOCATION_AWARE:
                    textColor = Configuration.LOCATION_AWARE_NODE_COLOR
                elif node.getType() == NodeType.LOCATION_IGNORANT:
                    textColor = Configuration.LOCATION_IGNORANT_NODE_COLOR

            # NODE ID
            self.canvas.create_text(
                node.getCentroid().x,
                node.getCentroid().y,
                fill = textColor,
                font = Configuration.FONT,
                # text = chr(node.getId())
                # for testing purposes
                text = node.getId()
            )

            # SOME HELPER TEXT
            self.canvas.create_text(
                Configuration.HELPER_TEXT_X_DIRECTION_DISPLACEMENT,
                Configuration.HELPER_TEXT_Y_DIRECTION_DISPLACEMENT,
                fill = Configuration.HELPER_TEXT_COLOR,
                font = Configuration.FONT,
                text = helperText
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