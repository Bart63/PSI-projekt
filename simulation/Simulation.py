# manager for all drivers and the visualization
import math
from typing import List
from .utils import Vehicle, Destination
from .Map import Map
from .MapRenderer import MapRenderer
from .debug import plot_map
from .api import API
import config as cfg
import cv2
import time
from .utils.YamlConfigParser import set_yaml_config

DESTINATION_REACH_DISTANCE = 1


class Simulation:
    def __init__(self, driver_name: str, test_no: int, test_type: str):
        self.main_vehicle = None
        if driver_name != "" and test_no != -1:
            set_yaml_config('configurations.yaml', driver_name, test_no, test_type)
        self.map = Map(size=(cfg.WIDTH, cfg.HEIGHT), seed=cfg.SEED, vehicles_number=cfg.NB_DUMMY_VEHICLES,
                       map_filling=cfg.MAP_FILLING, road_padding=cfg.ROAD_PADDING, nb_destinations=cfg.NB_DESTINATIONS)
        self.destinations: List[Destination] = self.map.destinations
        self.map_renderer = MapRenderer(self.map)
        self.set_init_api_values()
        self.simulation_running = False

    def run(self):
        print('Welcome in the Simulation!')
        self.simulation_running = True

        self.map.add_main_vehicle(cfg.MAIN_VEHICLE_DRIVER)
        self.main_vehicle: Vehicle = self.map.main_vehicle
        self.set_final_dest_api_value()

        start_time = time.time()
        ticks = 0
        while self.simulation_running:
            if ticks % cfg.TRAFFIC_LIGHTS_CHANGE_TICKS == 0:
                self.map.switch_traffic_lights(cfg.TRAFFIC_LIGHTS_CHANGE_PERC)

            self.update_rest_api_values()

            if ticks == 0:
                self.on_simulation_start()

            self.map.move_map()
            self.try_reach_destination()

            plot_map(self.map)

            cv2.waitKey(cfg.WAIT_MS)
            ticks += 1

            if not len(self.destinations):
                break
        end_time = time.time()
        time_taken = end_time - start_time
        # print('Distance: ', self.main_vehicle.distance)
        # print('Time: ', time_taken)
        self.end_simulation()
        return {
            'distance': self.main_vehicle.distance,
            'time': time_taken,
            'ticks': ticks
        }

    def stop(self):
        self.simulation_running = False

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
        self.main_vehicle.on_simulation_end()
        print('Simulation ended')

    def on_simulation_start(self):
        for v in self.map.vehicles:
            v.on_simulation_start()

    def set_init_api_values(self):
        crossroads = self.map.crossroads
        API.crossroads_pos_list = [(cr.x, cr.y) for cr in crossroads]
        API.possible_directions = [cr.get_connection_directions() for cr in crossroads]
        API.roads_length_per_crossroad = [{dir: cr.get_road_length(dir) for dir in API.possible_directions[i]} for i, cr
                                          in enumerate(crossroads)]

    def set_final_dest_api_value(self):
        final_destination = self.map.last_destination
        API.final_destination_pos = final_destination.x, final_destination.y

    def update_rest_api_values(self):
        API.main_vehicle_pos = self.map.main_vehicle.get_position()
        API.main_vehicle_direction = self.map.main_vehicle.current_direction
        API.target_crossroad_pos = self.map.main_vehicle.target_crossroad.get_position()
        API.target_crossroad_possible_directions = self.map.main_vehicle.target_crossroad.get_connection_directions()
        API.destinations_pos_list = [des.get_position() for des in self.destinations]
        crossroads = self.map.crossroads
        API.cars_on_road = [{dir: len(cr.vehicle_queue[dir].queue) for dir in API.possible_directions[i]} for i, cr in
                            enumerate(crossroads)]
