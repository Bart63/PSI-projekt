import numpy as np
import numpy.random

from drivers.Driver import Driver
from simulation.api import API
from simulation.utils.Direction import Direction


def euclidean_dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def manhattan(a, b):
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


class NaiveDriver(Driver):
    def __init__(self):
        super().__init__()

    def on_simulation_start(self):
        print("Naive Driver started!")

    def on_road_start(self):
        '''First tick after switching to a new road'''
        pass

    def on_tick(self):
        pass

    def on_road_end(self):
        up_move = (0, 40)
        down_move = (0, -40)
        left_move = (40, 0)
        right_move = (-40, 0)
        API.destinations_pos_list.pop(-1)
        dest_pos = API.destinations_pos_list

        distances_to_goals = [euclidean_dist(API.main_vehicle_pos, dest) for dest in dest_pos]

        goal_point = API.final_destination_pos
        if len(distances_to_goals) > 0:
            goal_point = API.destinations_pos_list[distances_to_goals.index(min(distances_to_goals))]

        # print('goal_point', goal_point)
        crossroads_dists = {
            Direction.UP: 9999999999,
            Direction.LEFT: 9999999999,
            Direction.DOWN: 9999999999,
            Direction.RIGHT: 9999999999,
        }
        for direction in API.target_crossroad_possible_directions:
            if direction == Direction.UP:
                future_pos = (API.target_crossroad_pos[0] - up_move[0], API.target_crossroad_pos[1] - up_move[1])
                if future_pos not in API.crossroads_pos_list:
                    while future_pos in API.crossroads_pos_list:
                        future_pos = (future_pos[0] - up_move[0], future_pos[1] - up_move[1])
                crossroads_dists[direction] = manhattan(goal_point, future_pos)
            elif direction == Direction.DOWN:
                future_pos = (API.target_crossroad_pos[0] - down_move[0], API.target_crossroad_pos[1] - down_move[1])
                if future_pos not in API.crossroads_pos_list:
                    while future_pos in API.crossroads_pos_list:
                        future_pos = (future_pos[0] - up_move[0], future_pos[1] - up_move[1])
                crossroads_dists[direction] = manhattan(goal_point, future_pos)
            elif direction == Direction.RIGHT:
                future_pos = (API.target_crossroad_pos[0] - right_move[0], API.target_crossroad_pos[1] - right_move[1])
                if future_pos not in API.crossroads_pos_list:
                    while future_pos in API.crossroads_pos_list:
                        future_pos = (future_pos[0] - up_move[0], future_pos[1] - up_move[1])
                crossroads_dists[direction] = manhattan(goal_point, future_pos)
            elif direction == Direction.LEFT:
                future_pos = (API.target_crossroad_pos[0] - left_move[0], API.target_crossroad_pos[1] - left_move[1])
                if future_pos not in API.crossroads_pos_list:
                    while future_pos in API.crossroads_pos_list:
                        future_pos = (future_pos[0] - up_move[0], future_pos[1] - up_move[1])
                crossroads_dists[direction] = manhattan(goal_point, future_pos)

        # print(crossroads_dists)
        # print(sorted(crossroads_dists.items(), key=lambda x: x[1]))
        sorted_dict = sorted(crossroads_dists.items(), key=lambda x: x[1])

        decisions = [a for a, b in sorted_dict]
        if sorted_dict[0][1] == sorted_dict[1][1]:
            if numpy.random.random() > 0.5:
                temp = decisions[0]
                decisions[0] = decisions[1]
                decisions[1] = temp

        self.direction_decisions = decisions

    def get_direction_decisions(self) -> Direction:
        return self.direction_decisions and self.direction_decisions.pop(0)
