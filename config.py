from drivers.SPED.SPED import SPED

# Main vehicle config
MAIN_VEHICLE_DRIVER = SPED()

# Map config
WIDTH = 400
HEIGHT = 400

# Roads config
MAP_FILLING = 0.8
ROAD_PADDING = 50

# Number of destinations 
NB_DESTINATIONS = 5

# Vehicles config
NB_DUMMY_VEHICLES = 100

# Traffic lights config
TRAFFIC_LIGHTS_CHANGE_TICKS = 40
TRAFFIC_LIGHTS_CHANGE_PERC = 50

# Simulation config
SEED = 0
WAIT_MS = 10

# Vehicle speed
VEHICLE_PROGRESS_STEP = 1

# Queue padding
QUEUE_PADDING = 20