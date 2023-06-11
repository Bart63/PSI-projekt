from random import choice, random
import numpy as np
from .Crossroad import Crossroad
from .Destination import Destination

from typing import List

class DestinationsGenerator:
    def __init__(self, crossroads: Crossroad, rng):
        self.crossroads = crossroads
        self.rng:np.random.Generator = rng

    @classmethod
    def create(cls, crossroads, rng):
        instance = cls(crossroads, rng)
        return instance
    
    def generate(self, nb_destinations: int) -> List[Destination]:
        chosen_crossroads:List[Crossroad] = self.rng.choice(self.crossroads, size=nb_destinations)
        chosen_roads = map(lambda cr: (cr, self.rng.choice(cr.get_connections())), chosen_crossroads)
        destinations = [Destination(point['x'], point['y']) for point in map(self.extract_points, chosen_roads)]
        return destinations

    def extract_points(self, road):
        x_min, x_max = sorted([road[0].x, road[1].x])
        y_min, y_max = sorted([road[0].y, road[1].y])
        x = int(self.rng.random() * (x_max-x_min) + x_min)
        y = int(self.rng.random() * (y_max-y_min) + y_min)
        return {
            'x': x,
            'y': y
        }
