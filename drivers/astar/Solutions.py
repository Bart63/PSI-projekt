from simulation.api import API
from utils import *

class Solutions():
    def __init__(self, start_crossroad_pos: tuple[float, float]) -> None:
        self.visited_crossroads_ids = [API.crossroads_pos_list.index(start_crossroad_pos)]
        self.cost = 0

        self.points_to_visit = deep_copy(API.destinations_pos_list)
        if API.final_destination_pos in self.points_to_visit:
            self.points_to_visit.remove(API.final_destination_pos)

        self.returns_to_start = False
        self.directions = []