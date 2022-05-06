from tkinter import *
import tkinter

from Configurations import Configuration
from Constants import NodeType

class GuiService:
    def __init__(self, width, height, start, move, basicRouting, locationProxyRouting, infRouting, turnIntermediateNodeForwardingOn, turnIntermediateNodeForwardingOff, toggleAutomaticSimulation):

        self.window = Tk()

        self.logWindow = Toplevel(self.window)
        self.logWindow.geometry('{}{}{}'.format(Configuration.LOG_WINDOW_WIDTH, "x", Configuration.LOG_WINDOW_HEIGHT))
        self.logWindow.title(Configuration.LOG_WINDOW_TITLE)
        self.logTextArea = Text(self.logWindow, height = Configuration.LOG_TEXT_AREA_WIDTH, width = Configuration.LOG_TEXT_AREA_HEIGHT, font=(Configuration.LOG_TEXT_AREA_FONT, Configuration.LOG_TEXT_AREA_FONTSIZE))
        self.logTextArea.pack()
        self.logWindowToggle = True

        self.window.after(0, lambda: self.window.focus_force())

        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()

        x = int((screenWidth / 2) - (width / 2))
        y = int((screenHeight / 2) - (height / 2))

        self.window.title(Configuration.MAIN_WINDOW_TITLE)
        self.window.geometry('{}{}{}{}{}{}{}'.format(width, "x", height, "+", x, "+", y))
        self.window.resizable(False, False)

        self.canvas = Canvas(self.window)
        self.canvas.pack(fill = BOTH, expand = 1)

        self.window.bind(Configuration.TOGGLE_LOGWINDOW_KEY, self.__toggleLogWindow)
        self.window.bind(Configuration.RESTART_KEY, start)
        self.window.bind(Configuration.MOVEMENT_KEY, move)
        self.window.bind(Configuration.BASIC_ROUTING_KEY, basicRouting)
        self.window.bind(Configuration.LOCATION_PROXY_ROUTING_KEY, locationProxyRouting)
        self.window.bind(Configuration.INF_ROUTING_KEY, infRouting)
        self.window.bind(Configuration.TURN_INTERMEDIATE_NODE_FORWARDING_ON_KEY, turnIntermediateNodeForwardingOn)
        self.window.bind(Configuration.TURN_INTERMEDIATE_NODE_FORWARDING_OFF_KEY, turnIntermediateNodeForwardingOff)
        self.window.bind(Configuration.TOGGLE_AUTOMATIC_SIMULATION_KEY, toggleAutomaticSimulation)

    def __toggleLogWindow(self, event):
        self.logWindowToggle = not self.logWindowToggle
        if self.logWindowToggle:
            self.logWindow.deiconify()
            self.window.after(0, lambda: self.window.focus_force())
        else:
            self.logWindow.withdraw()
            

    def loop(self):
        self.window.mainloop()

    def render(self, nodes, helperText : str, packetLocations : [] = None, isRenderingINFNodes = False, routingResult : [] = None):

        self.canvas.delete("all")

        with open(Configuration.LOG_FILE_NAME) as f:
            lines = f.readlines()
            f.close()
            self.logTextArea.insert(END, lines)
            self.logTextArea.see(END)

        # SOME HELPER TEXT
        id = self.canvas.create_text(
            Configuration.HELPER_TEXT_X_DIRECTION_DISPLACEMENT,
            Configuration.HELPER_TEXT_Y_DIRECTION_DISPLACEMENT,
            fill = Configuration.HELPER_TEXT_COLOR,
            font = Configuration.HELPER_TEXT_FONT,
            text = helperText,
            anchor = Configuration.TEXT_ANCHOR
        )

        bbox = self.canvas.bbox(id)
        rect = self.canvas.create_rectangle(
            bbox[0] - 10,
            bbox[1] - 10,
            bbox[2] + 10,
            bbox[3] + 10,
            fill = Configuration.HELPER_TEXT_RECTANGLE_FILL,
            outline = Configuration.HELPER_TEXT_RECTANGLE_OUTLINE,
        )
        self.canvas.tag_lower(rect, id)

        # NODES
        for node in nodes:

            isPartOfSomeNetwork = False

            if not isRenderingINFNodes:
                if node.checkNetworkBelonging(nodes):
                    nodeShapeFillColor = Configuration.NODE_IN_NETWORK_SHAPE_FILL_COLOR
                    nodeBroadcastRangeFillColor = Configuration.NODE_BROADCAST_RANGE_OUTLINE_COLOR
                    isPartOfSomeNetwork = True
                else:
                    nodeShapeFillColor = Configuration.NODE_OUT_OF_NETWORK_SHAPE_FILL_COLOR
                    nodeBroadcastRangeFillColor = Configuration.NODE_OUT_OF_NETWORK_BROADCAST_RANGE_OUTLINE_COLOR

            else:
                nodeShapeFillColor = Configuration.INF_NODE_SHAPE_FILL_COLOR
                nodeBroadcastRangeFillColor = Configuration.INF_NODE_BROADCAST_RANGE_OUTLINE_COLOR

            # NODE SHAPE
            self.__drawCircle(
                node.getCentroid().x,
                node.getCentroid().y,
                node.getShapeRadius(),
                f = nodeShapeFillColor
            )

            # NODE BROADCAST RANGE
            self.__drawCircle(
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
                font = Configuration.HELPER_TEXT_FONT,
                # text = chr(node.getId())
                # for testing purposes
                text = node.getId()
            )

        # PACKETS
        if packetLocations is not None and len(packetLocations) >= 2:

            # PACKET SOURCE LOCATION
            self.__drawCircle(
                packetLocations[0][1].x,
                packetLocations[0][1].y,
                Configuration.PACKET_SHAPE_RADIUS,
                Configuration.PACKET_OUTLINE_COLOR
            )

            for index, packetLocation in enumerate(packetLocations):
                if index != len(packetLocations) - 1:
                    self.canvas.create_line(
                        packetLocations[index][1].x,
                        packetLocations[index][1].y,
                        packetLocations[index + 1][1].x,
                        packetLocations[index + 1][1].y
                    )

        # ROUTING LOG TEXT
        if routingResult is not None:

            match routingResult[1]:
                case None:
                    textColor = Configuration.ROUTING_LOG_TEXT_COLOR
                case True:
                    textColor = Configuration.SUCCESS_TEXT_COLOR
                case False:
                    textColor = Configuration.FAILURE_TEXT_COLOR

            self.canvas.create_text(
                Configuration.ROUTING_LOG_TEXT_X_DIRECTION_DISPLACEMENT,
                Configuration.ROUTING_LOG_TEXT_Y_DIRECTION_DISPLACEMENT,
                fill = textColor,
                font = Configuration.ROUTING_LOG_TEXT_FONT,
                text = routingResult[0],
                anchor = Configuration.TEXT_ANCHOR
            )

    def __drawCircle(self, x, y, r, c = Configuration.NODE_OUTLINE_DEFAULT_COLOR, f = Configuration.NODE_FILL_DEFAULT_COLOR, alpha = None):
        return self.canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill = f,
            outline = c
        )