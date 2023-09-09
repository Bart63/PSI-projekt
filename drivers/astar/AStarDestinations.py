# example implementation of driver
from simulation.api import API
from drivers.Driver import Driver
from simulation.utils.Direction import Direction
from .PathNode import PathNode

class AStartDestinations():
    def __init__(self):
        super().__init__()
        PathNode.all_destinations_number = len(API.destinations_pos_list)
        print(PathNode.all_destinations_number)