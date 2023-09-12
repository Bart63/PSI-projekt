# example implementation of driver
from simulation.api import API
from .Driver import Driver
import random
from simulation.utils.Direction import Direction
import time


class GreedyDriver(Driver):
    def __init__(self):
        super().__init__()
        self.previous_decision = 0

    def on_road_start(self):
        ##print("\n nowa droga \n")
        pass

    def on_road_end(self):
        a = 0.7
        b = 1

        road_to_dest_costs = []
        for i in API.target_crossroad_possible_directions:
            if Direction(i) == Direction.UP:
                road_to_dest_costs.append([(abs(API.destinations_pos_list[0][0] - API.target_crossroad_pos[0]) + abs(API.destinations_pos_list[0][1] - (API.target_crossroad_pos[1] - 40)))/400, Direction.UP])
            if Direction(i) == Direction.RIGHT:
                road_to_dest_costs.append([(abs(API.destinations_pos_list[0][0] - (API.target_crossroad_pos[0] + 40)) + abs(API.destinations_pos_list[0][1] - API.target_crossroad_pos[1]))/400, Direction.RIGHT])
            if Direction(i) == Direction.DOWN:
                road_to_dest_costs.append([(abs(API.destinations_pos_list[0][0] - (API.target_crossroad_pos[0])) + abs(API.destinations_pos_list[0][1] - (API.target_crossroad_pos[1] + 40)))/400, Direction.DOWN])
            if Direction(i) == Direction.LEFT:
                road_to_dest_costs.append([(abs(API.destinations_pos_list[0][0] - (API.target_crossroad_pos[0] - 40)) + abs(API.destinations_pos_list[0][1] - (API.target_crossroad_pos[1])))/400, Direction.LEFT])

        road_occupancy_cost_list = [occupancy/ 10 for occupancy in API.cars_on_road[API.crossroads_pos_list.index(API.target_crossroad_pos)].values()]
        
        cost = [[a * road_to_dest_cost[0] + b * road_occupancy_cost, road_to_dest_cost[1]] for road_to_dest_cost, road_occupancy_cost in zip(road_to_dest_costs, road_occupancy_cost_list)]
        cost = sorted(cost, key=lambda x: x[0])

        self.direction_decisions = [x[1] for x in cost]
    
        if self.previous_decision !=0 and self.direction_decisions[0].get_reverse() == self.previous_decision:
            self.direction_decisions.pop(0)

        # if all_equal(cost):
        #     random.shuffle(self.direction_decisions)

        self.previous_decision = self.direction_decisions[0]

# def all_equal(iterator):
#     iterator = iter(iterator)
#     try:
#         first = next(iterator)
#     except StopIteration:
#         return True
#     return all(first == x for x in iterator)