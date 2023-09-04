import config
from simulation.api import API
from drivers.Driver import Driver
from math import floor, ceil
from simulation.utils.Direction import Direction
from typing import List
from drivers.SPED.MCTS import Mcts
from drivers.SPED.inference import *
import config as cfg


class SPED(Driver):
    def __init__(self):
        super().__init__()
        self.tick = 0
        self.direction_decisions: List[Direction] = []
        self.map_tensors = []
        self.decisions = []
        self.at_tick = []
        self.last_direction = 10
        self.visits = []

    def on_tick(self):
        self.tick += 1

    def on_simulation_start(self):
        self.road_padding = cfg.ROAD_PADDING
        self.map_state_tensor = self.generate_map_state_tensor()
        self.predictor = predictor(floor(cfg.HEIGHT / cfg.ROAD_PADDING), floor(cfg.WIDTH / cfg.ROAD_PADDING))
        self.mcts = Mcts(self.map_state_tensor, self.last_direction, self.predictor)

    def search(self):
        left = self.mcts.root.initial_destinations_left
        while True:
            self.mcts.execute_round()
            if self.mcts.root.num_visits > 0 and self.mcts.root.destinations_left < left:
                break

    def on_road_end(self):
        self.update_map_tensor()
        if len(self.direction_decisions) == 0 and not self.mcts.root.is_terminal:
            self.mcts = Mcts(self.map_state_tensor, self.last_direction, self.predictor)
            self.search()
            directions, _, _ = self.mcts.get_directions_list()
            directions = [self.get_direction_from_idx(direction) for direction in directions]
            self.direction_decisions += directions
            self.mcts.print_info()

    def generate_map_state_tensor(self):
        map_height = cfg.HEIGHT
        map_width = cfg.WIDTH
        road_padding = self.road_padding
        grid_width = floor(map_width / road_padding)
        grid_height = floor(map_height / road_padding)
        xroads_positions = list(API.crossroads_pos_list)
        xroads_positions = [(round(tup[0] / road_padding), round(tup[1] / road_padding)) for tup in xroads_positions]
        size = max((grid_width, grid_height))
        map_state_tensor = np.zeros((29, size, size))

        # CHANNEL 0 - XROADS
        for pos in xroads_positions:
            map_state_tensor[0][pos[1]][pos[0]] = 1

        # CHANNELS 1-4 - DIRECTIONS FROM CROSSROADS
        possible_directions = API.possible_directions
        for i in range(len(xroads_positions)):
            xroad_directions = possible_directions[i]
            xroad_position = xroads_positions[i]
            for direction in xroad_directions:
                map_state_tensor[direction.value][xroad_position[1]][xroad_position[0]] = 1

        '''#CHANNELS 5-8 - CARS ON DIRECTION FROM CROSSRADS
        cars_on_road = API.cars_on_road
        for i in range(len(xroads_positions)):
            cars_on_current_xroad = cars_on_road[i]
            xroad_position = xroads_positions[i]
            for direction in cars_on_current_xroad.items():
                map_state_tensor[4+direction[0].value][xroad_position[1]][xroad_position[0]] = direction[1]'''

        # CHAANNELS 9-12 - ROADS LENGTH PER CROSSROAD
        roads_length_per_crossroad = API.roads_length_per_crossroad
        for i in range(len(xroads_positions)):
            lenghts_from_currend_xroad = roads_length_per_crossroad[i]
            xroad_position = xroads_positions[i]
            for direction in lenghts_from_currend_xroad.items():
                map_state_tensor[8 + direction[0].value][xroad_position[1]][xroad_position[0]] = direction[
                                                                                                     1] / road_padding

        # CHANNELS 13-16 - DESTINTION POSITIONS
        destination_pos_list = API.destinations_pos_list[:-1]
        destination_pos_list = [(tup[0] / road_padding, tup[1] / road_padding) for tup in destination_pos_list]
        for pos in destination_pos_list:
            if pos[0] % 1 == 0:
                map_state_tensor[13][ceil(pos[1])][round(pos[0])] = 1
                map_state_tensor[15][floor(pos[1])][round(pos[0])] = 1
            if pos[1] % 1 == 0:
                map_state_tensor[14][round(pos[1])][floor(pos[0])] = 1
                map_state_tensor[16][round(pos[1])][ceil(pos[0])] = 1

        # CHANNEL 17 - FINAL POSITION
        pos = API.final_destination_pos
        pos = (pos[0] / road_padding, pos[1] / road_padding)
        map_state_tensor[17][round(pos[1])][round(pos[0])] = 1


        # CHANNEL 18 - 22 - VEHICLE POS
        pos = API.main_vehicle_pos
        pos = (pos[0] / road_padding, pos[1] / road_padding)
        map_state_tensor[18][round(pos[1])][round(pos[0])] = 1

        direction = API.main_vehicle_direction.value
        map_state_tensor[18 + direction][round(pos[1])][round(pos[0])] = 1

        # CHANNELS 23-24  CONFIG DATA

        map_state_tensor[23, :, :] = config.WIDTH / 500
        map_state_tensor[24, :, :] = config.HEIGHT / 500
        # map_state_tensor[25, :, :] = road_padding / 100
        map_state_tensor[25, :, :] = config.MAP_FILLING
        coords = np.linspace(-1, 1, size)
        map_state_tensor[26], map_state_tensor[27] = np.meshgrid(coords, coords) #positional encoding
        # map_state_tensor[26, :, :] = config.QUEUE_PADDING / road_padding
        # map_state_tensor[27, :, :] = config.TRAFFIC_LIGHTS_CHANGE_TICKS / 100
        # map_state_tensor[28, :, :] = config.TRAFFIC_LIGHTS_CHANGE_PERC / 100

        return map_state_tensor

    def update_map_tensor(self):
        self.map_state_tensor[[5, 6, 7, 8, 13, 14, 15, 16, 18, 19, 20, 21, 22]] = np.zeros(
            self.map_state_tensor.shape[1:])
        destination_pos_list = API.destinations_pos_list[:-1]
        destination_pos_list = [(tup[0] / self.road_padding, tup[1] / self.road_padding) for tup in
                                destination_pos_list]
        for pos in destination_pos_list:
            if pos[0] % 1 == 0:
                self.map_state_tensor[13][ceil(pos[1])][round(pos[0])] = 1
                self.map_state_tensor[15][floor(pos[1])][round(pos[0])] = 1
            if pos[1] % 1 == 0:
                self.map_state_tensor[14][round(pos[1])][floor(pos[0])] = 1
                self.map_state_tensor[16][round(pos[1])][ceil(pos[0])] = 1

        pos = API.main_vehicle_pos
        pos = (round(pos[0] / self.road_padding), round(pos[1] / self.road_padding))
        self.map_state_tensor[18][int(pos[1])][int(pos[0])] = 1

        direction = API.main_vehicle_direction.value
        self.map_state_tensor[18 + direction][int(pos[1])][int(pos[0])] = 1

    def get_direction_decisions(self) -> Direction:
        return self.direction_decisions and self.direction_decisions.pop(0)

    def get_direction_from_idx(self, idx):
        if idx == 1:
            return Direction.UP
        elif idx == 2:
            return Direction.RIGHT
        elif idx == 3:
            return Direction.DOWN
        elif idx == 4:
            return Direction.LEFT
