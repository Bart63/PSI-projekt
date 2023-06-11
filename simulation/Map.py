from .utils import Vehicle, Crossroad, CrossroadsGenerator
from drivers import DummyDriver
from typing import List

import numpy as np


class Map:
    def __init__(self, size: tuple[int, int], seed: int, road_padding=50, map_filling=.7, vehicles_number=10, driver=DummyDriver):
        self.vehicles: List[Vehicle] = []
        self.crossroads: List[Crossroad] = []
        self.width, self.height = size
        self.rng = np.random.default_rng(seed)
        self.road_padding = road_padding

        crossroad_generator = CrossroadsGenerator(self.width, self.height, self.road_padding, map_filling, self.rng)
        self.crossroads = crossroad_generator.generate_crossroads()
        crossroad_generator.connect_crossroads(self.crossroads)

        self.__add_vehicles(vehicles_number)

        from .debug import plot_map
        plot_map(self)

    def __add_vehicles(self, vehicles_number):
        for id_ in range(vehicles_number):
            # TODO spawn points need to be counted and orientation according to the roads
            vehicle = Vehicle(id_, spawn_x=0, spawn_y=0, driver=DummyDriver())
            self.vehicles.append(vehicle)
