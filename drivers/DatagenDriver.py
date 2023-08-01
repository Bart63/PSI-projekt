
import config
from simulation.api import API
from drivers.Driver import Driver
from math import floor, ceil
import numpy as np
import config as cfg
import keyboard
from simulation.utils.Direction import Direction
from typing import List
import datetime


def get_arrow_input():
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'up':
                return Direction.UP
            elif event.name == 'down':
                return Direction.DOWN
            elif event.name == 'left':
                return Direction.LEFT
            elif event.name == 'right':
                return Direction.RIGHT

import time
np.set_printoptions(threshold=np.inf)
class DatagenDriver(Driver):
    def __init__(self):
        super().__init__()
        self.tick = 0
        self.direction_decisions: List[Direction] = []
        self.map_tensors = []
        self.decisions = []
        self.at_tick = []




    def on_simulation_start(self):
        self.road_padding = cfg.ROAD_PADDING
        self.map_state_tensor = self.generate_map_state_tensor()
        print(self.map_state_tensor)

    def on_simulation_end(self):
        last_tick = self.tick
        self.at_tick = [0] + self.at_tick
        ticks_to_finish = []
        ticks_from_last_xroad = []
        for index, val in enumerate(self.at_tick[1:]):
            to_finish = last_tick - val
            from_last_road = val - self.at_tick[index]
            ticks_to_finish.append(to_finish)
            ticks_from_last_xroad.append(from_last_road)
        ticks_to_finish = np.array(ticks_to_finish)
        ticks_from_last_xroad = np.array(ticks_from_last_xroad)
        map_tensors = np.array(self.map_tensors)
        decisions = np.array(self.decisions)
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d_%H-%M-%S.%f")
        np.savez(f"human_datasets/run_{now}.npz", ticks_to_finish=ticks_to_finish,
                 ticks_from_last_xroad=ticks_from_last_xroad, map_tensors=map_tensors, decisions=decisions)




    def on_tick(self):
        self.tick += 1

    def on_road_end(self):
        self.update_map_tensor()
        direction = get_arrow_input()
        self.direction_decisions.append(direction)
        self.map_tensors.append(self.map_state_tensor)
        self.decisions.append(direction)
        self.at_tick.append(self.tick)
        print(self.map_state_tensor)
        print(self.at_tick)
    def on_road_start(self):
        pass

    def generate_map_state_tensor(self):
        map_height = cfg.HEIGHT
        map_width = cfg.WIDTH
        road_padding = self.road_padding
        grid_width = floor(map_width / road_padding-1)
        grid_height = floor(map_height / road_padding-1)
        xroads_positions = list(API.crossroads_pos_list)
        xroads_positions = [(int(tup[0] / road_padding)-1, int(tup[1] / road_padding)-1) for tup in xroads_positions]

        map_state_tensor = np.zeros((29, grid_height, grid_width))

        #CHANNEL 0 - XROADS
        for pos in xroads_positions:
            map_state_tensor[0][pos[1]][pos[0]] = 1

        #CHANNELS 1-4 - DIRECTIONS FROM CROSSROADS
        possible_directions = API.possible_directions
        for i in range(len(xroads_positions)):
            xroad_directions = possible_directions[i]
            xroad_position = xroads_positions[i]
            for direction in xroad_directions:
                map_state_tensor[direction.value][xroad_position[1]][xroad_position[0]] = 1

        #CHANNELS 5-8 - CARS ON DIRECTION FROM CROSSRADS
        cars_on_road = API.cars_on_road
        for i in range(len(xroads_positions)):
            cars_on_current_xroad = cars_on_road[i]
            xroad_position = xroads_positions[i]
            for direction in cars_on_current_xroad.items():
                map_state_tensor[4+direction[0].value][xroad_position[1]][xroad_position[0]] = direction[1]

        #CHAANNELS 9-12 - ROADS LENGTH PER CROSSROAD
        roads_length_per_crossroad = API.roads_length_per_crossroad
        for i in range(len(xroads_positions)):
            lenghts_from_currend_xroad = roads_length_per_crossroad[i]
            xroad_position = xroads_positions[i]
            for direction in lenghts_from_currend_xroad.items():
                map_state_tensor[8+direction[0].value][xroad_position[1]][xroad_position[0]] = direction[1]/road_padding

        # CHANNELS 13-16 - DESTINTION POSITIONS
        destination_pos_list = API.destinations_pos_list[:-1]
        destination_pos_list= [(tup[0] / road_padding - 1, tup[1] / road_padding - 1) for tup in destination_pos_list]
        for pos in destination_pos_list:
            print(pos)
            if pos[0] % 1 == 0:
                map_state_tensor[13][ceil(pos[1])][int(pos[0])] = 1
                map_state_tensor[15][floor(pos[1])][int(pos[0])] = 1
            if pos[1] % 1 == 0:
                map_state_tensor[14][int(pos[1])][floor(pos[0])] = 1
                map_state_tensor[16][int(pos[1])][ceil(pos[0])] = 1



        # CHANNEL 17 - FINAL POSITION
        pos = API.final_destination_pos
        pos = (pos[0] / road_padding - 1, pos[1] / road_padding - 1)
        map_state_tensor[17][int(pos[1])][int(pos[0])] = 1

        #map_state_tensor[[13, 14, 15, 16]][int(pos[1])][int(pos[0])] = 0

        # CHANNEL 18 - 22 - VEHICLE POS
        pos = API.main_vehicle_pos
        pos = (pos[0] / road_padding - 1, pos[1] / road_padding - 1)
        map_state_tensor[18][int(pos[1])][int(pos[0])] = 1


        direction = API.main_vehicle_direction.value
        map_state_tensor[18+direction][int(pos[1])][int(pos[0])] = 1


        # CHANNELS 23-24  CONFIG DATA

        map_state_tensor[23, :, :] = config.WIDTH / 1000
        map_state_tensor[24, :, :] = config.HEIGHT / 1000
        map_state_tensor[25, :, :] = config.VEHICLE_PROGRESS_STEP
        map_state_tensor[26, :, :] = config.QUEUE_PADDING / road_padding
        map_state_tensor[27, :, :] = config.TRAFFIC_LIGHTS_CHANGE_TICKS / 100
        map_state_tensor[28, :, :] = config.TRAFFIC_LIGHTS_CHANGE_PERC / 100

        return map_state_tensor



    def update_map_tensor(self):
        self.map_state_tensor[[5, 6, 7, 8, 13, 14, 15, 16, 18, 19, 20, 21, 22]] = np.zeros(self.map_state_tensor.shape[1:])
        xroads_positions = list(API.crossroads_pos_list)
        xroads_positions = [(int(tup[0] / self.road_padding)-1, int(tup[1] / self.road_padding)-1) for tup in xroads_positions]
        cars_on_road = API.cars_on_road
        for i in range(len(xroads_positions)):
            cars_on_current_xroad = cars_on_road[i]
            xroad_position = xroads_positions[i]
            for direction in cars_on_current_xroad.items():
                self.map_state_tensor[4+direction[0].value][xroad_position[1]][xroad_position[0]] = direction[1]


        destination_pos_list = API.destinations_pos_list[:-1]
        destination_pos_list= [(tup[0] / self.road_padding - 1, tup[1] / self.road_padding - 1) for tup in destination_pos_list]
        for pos in destination_pos_list:
            if pos[0] % 1 == 0:
                self.map_state_tensor[13][ceil(pos[1])][int(pos[0])] = 1
                self.map_state_tensor[15][floor(pos[1])][int(pos[0])] = 1
            if pos[1] % 1 == 0:
                self.map_state_tensor[14][int(pos[1])][floor(pos[0])] = 1
                self.map_state_tensor[16][int(pos[1])][ceil(pos[0])] = 1

        pos = API.main_vehicle_pos
        pos = (pos[0] / self.road_padding - 1, pos[1] / self.road_padding - 1)
        self.map_state_tensor[18][int(pos[1])][int(pos[0])] = 1

        direction = API.main_vehicle_direction.value
        self.map_state_tensor[18 + direction][int(pos[1])][int(pos[0])] = 1

    def get_direction_decisions(self) -> Direction:
        return self.direction_decisions and self.direction_decisions.pop(0)



