from drivers.astar.AStarDriver import AStarDriver

# Main vehicle config
MAIN_VEHICLE_DRIVER = AStarDriver(40)

# Map config
WIDTH = 250
HEIGHT = 250

# Roads config
MAP_FILLING = 0.6
ROAD_PADDING = 40

# Vehicles config
NB_DUMMY_VEHICLES = 10

# Traffic lights config
TRAFFIC_LIGHTS_CHANGE_TICKS = 40
TRAFFIC_LIGHTS_CHANGE_PERC = 1

# Simulation config
SEED = 10
WAIT_MS = 10

# Vehicle speed
VEHICLE_PROGRESS_STEP = 1

# Queue padding
QUEUE_PADDING = 20