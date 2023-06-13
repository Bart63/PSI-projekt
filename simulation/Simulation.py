# manager for all drivers and the visualization
import math
from typing import List
from .utils import Vehicle, Destination
from .Map import Map
from .MapRenderer import MapRenderer
from .debug import plot_map
import register as rgstr
import cv2
import time

DESTINATION_REACH_DISTANCE = 1

class Simulation:
    def __init__(self, argv):
        self.map = Map(size=(500, 500), seed=0, vehicles_number=3, map_filling=0.7)
        self.destinations:List[Destination] = self.map.destinations
        self.map_renderer = MapRenderer(self.map)

    def run(self):
        print('Welcome in the Simulation!')

        self.map.add_main_vehicle(rgstr.MAIN_VEHICLE_DRIVER)
        self.main_vehicle:Vehicle = self.map.main_vehicle

        start_time = time.time()
        ticks = 0
        while True:
            if ticks % 20 == 5:
                self.map.switch_traffic_lights(1)

            self.map.move_map()
            self.try_reach_destination()

            plot_map(self.map)

            cv2.waitKey(10)
            ticks += 1

            if not len(self.destinations):
                break
        end_time = time.time()
        time_taken = end_time - start_time
        print('Distance: ', self.main_vehicle.distance)
        print('Time: ', time_taken)
        self.end_simulation()
    
    def try_reach_destination(self):
        vx, vy = self.main_vehicle.get_position()
        
        destinations = self.destinations
        if len(destinations) > 1:
            destinations = list(filter(lambda d: not d.is_last, destinations))

        destinations_positions = [d.get_position() for d in destinations]
        distances = [math.dist((vx, vy), dest) for dest in destinations_positions]
        destination_mask = map(lambda d: d < DESTINATION_REACH_DISTANCE, distances)

        for mask, destination in zip(destination_mask, destinations):
            if not mask:
                continue
            self.map.destination_reach(destination)
                
    def end_simulation(self):
        print('Simulation ended')
