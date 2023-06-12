from .utils import Vehicle, Crossroad, CrossroadsGenerator, DestinationsGenerator
from drivers import DummyDriver
from typing import List
from multiprocessing import Process

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

        self.destinations = self.destinations = DestinationsGenerator.create(self.crossroads, self.rng).generate(10)

        self.__add_vehicles(vehicles_number)

    def move_map(self):
        for cr in self.crossroads:
            cr.move_vehicles()
    
    def switch_traffic_lights(self, perc_change:float = 1):
        perc_change = min(max(perc_change, 0), 1)
        nb_crossroads = int(perc_change*len(self.crossroads))
        crossroads = self.rng.choice(self.crossroads, nb_crossroads, replace=False)
        for cr in crossroads:
            cr.switch_traffic_lights()

    def __add_vehicles(self, vehicles_number):
        for id_ in range(vehicles_number):
            vehicle = Vehicle(id_, driver=DummyDriver())
            self.vehicles.append(vehicle)
            cr = self.rng.choice(self.crossroads)
            dirs = cr.get_connection_directions()
            di = self.rng.choice(dirs)
            cr.enqueue_vehicle(vehicle, di)
