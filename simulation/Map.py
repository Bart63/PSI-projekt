from .utils import Vehicle, Crossroad, CrossroadsGenerator, DestinationsGenerator, Destination
from drivers import DummyDriver
from typing import List

import numpy as np


class Map:
    def __init__(self, size: tuple[int, int], seed: int, road_padding=50, map_filling=1, vehicles_number=10, driver=DummyDriver):
        self.vehicles: List[Vehicle] = []
        self.main_vehicle: Vehicle = None
        self.crossroads: List[Crossroad] = []
        self.width, self.height = size
        self.rng = np.random.default_rng(seed)
        self.road_padding = road_padding
        self.last_destination = None

        crossroad_generator = CrossroadsGenerator(self.width, self.height, self.road_padding, map_filling, self.rng)
        self.crossroads = crossroad_generator.generate_crossroads()
        crossroad_generator.connect_crossroads(self.crossroads)

        self.destinations = DestinationsGenerator.create(self.crossroads, self.rng).generate(10)

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

    def __random_append_vehicle(self, vehicle):
        cr:Crossroad = self.rng.choice(self.crossroads)
        dirs = cr.get_connection_directions()
        di = self.rng.choice(dirs)
        cr.enqueue_vehicle(vehicle, di)

    def __add_vehicles(self, vehicles_number):
        for id_ in range(vehicles_number):
            vehicle = Vehicle(id_, driver=DummyDriver())
            self.vehicles.append(vehicle)
            self.__random_append_vehicle(vehicle)
    
    def add_main_vehicle(self, driver):
        vehicle = Vehicle(len(self.vehicles), driver=driver, main_vehicle=True)
        self.main_vehicle = vehicle
        self.vehicles.append(vehicle)
        self.__random_append_vehicle(vehicle)
        self.__add_last_destination(vehicle)
    
    def __add_last_destination(self, main_vehicle):
        self.last_destination = Destination(id=len(self.destinations), x=main_vehicle.x, y=main_vehicle.y, is_last=True)
        self.destinations.append(self.last_destination)

    def destination_reach(self, destination:Destination):
        self.destinations.remove(destination)
