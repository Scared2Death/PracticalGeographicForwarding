GUI_WINDOW_TITLE = "Practical Geographic Forwarding"

GUI_WINDOW_WIDTH = 1250
GUI_WINDOW_HEIGHT = 600

HELPER_TEXT_X_DIRECTION_DISPLACEMENT = 125
HELPER_TEXT_Y_DIRECTION_DISPLACEMENT = 75

NODE_SHAPE_RADIUS = 25
PACKET_SHAPE_RADIUS = 10

INF_NODE_SHAPE_RADIUS = 25
INF_NODE_BROADCAST_RANGE_RADIUS = 30
INF_NODE_COORDINATES : {int : int} = {
    50 : 50,
    100 : 100
}

MINIMUM_NODES_DISTANCE = NODE_SHAPE_RADIUS * 2

MIN_BROADCAST_RANGE = 50
MAX_BROADCAST_RANGE = 150

MIN_CENTROID_MOVEMENT = -10
MAX_CENTROID_MOVEMENT = 10

NUMBER_OF_NODES_TO_GENERATE = 10

# %
GUI_CANVAS_CROP_PERCENTAGE = 20

FONT = "Arial 10"
HELPER_TEXT_COLOR = "gray"

LOCATION_AWARE_NODE_COLOR = "black"
LOCATION_IGNORANT_NODE_COLOR = "red"
WRONGLY_INITIALIZED_NODE_COLOR = "purple"

NODE_IN_NETWORK_SHAPE_FILL_COLOR = "#fff"
NODE_BROADCAST_RANGE_OUTLINE_COLOR = "#ccc"
NODE_OUT_OF_NETWORK_SHAPE_FILL_COLOR = "#F0C2C4"
NODE_OUT_OF_NETWORK_BROADCAST_RANGE_OUTLINE_COLOR = "#F0C2C4"

INF_NODE_SHAPE_FILL_COLOR = "#fff"
INF_NODE_BROADCAST_RANGE_OUTLINE_COLOR = "#ccc"

NODE_OUTLINE_DEFAULT_COLOR = "#000"
NODE_FILL_DEFAULT_COLOR = ""

PACKET_FILL_COLOR = "red"

NUMBER_OF_MAXIMUM_TRIALS_AT_NODE_GENERATION = 50
NUMBER_OF_MAXIMUM_MOVEMENT_TRIAL_PER_NODE = 10

# KEYS
RESTART_KEY = "<Return>"
MOVEMENT_KEY = "m"
BASIC_ROUTING_KEY = "b"
LOCATION_PROXY_ROUTING_KEY = "l"
LOCATION_PROXY_ON_KEY = "i"
LOCATION_PROXY_OFF_KEY = "o"
TOGGLE_AUTOMATIC_SIMULATION_KEY = "a"
INTERMEDIATE_NODE_FORWARDING_KEY = "f"

# %
RATIO_OF_LOCATION_AWARE_NODES = 60

# NODE ID CODES
BASE_NODE_ID = 65

# BASIC ROUTING
MAX_HOPS = 2

LOG_TO_CONSOLE = True
LOG_TO_FILE = False

BASE_LOG_FILE_NAME = "Network Logs"

# SECONDS
DELAY_INTERVAL = 1000

IS_AUTOMATIC_SIMULATION_ENABLED_BY_DEFAULT = False