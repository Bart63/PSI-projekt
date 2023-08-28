# example implementation of driver
from simulation.api import API
from .Driver import Driver


class GreedyDriver(Driver):
    def __init__(self):
        super().__init__()
        self.previous_decision = 0

    def on_road_start(self):
        print("\n nowa droga \n")

    def on_road_end(self):
        
        a = 1
        b = 1
        print(API.target_crossroad_pos)
        print(API.crossroads_pos_list.index(API.target_crossroad_pos))
        print(API.roads_length_per_crossroad[4].values())
        road_lenght_cost_list = [cost/ 400 for cost in API.roads_length_per_crossroad[API.crossroads_pos_list.index(API.target_crossroad_pos)].values()]
        road_occupancy_cost_list = [occupancy/ 10 for occupancy in API.cars_on_road[API.crossroads_pos_list.index(API.target_crossroad_pos)].values()]
        print(road_lenght_cost_list)
        print(road_occupancy_cost_list)

        cost = [a * road_lenght_cost + b * road_occupancy_cost for road_lenght_cost, road_occupancy_cost in zip(road_lenght_cost_list, road_occupancy_cost_list)]
        print(cost)

        self.direction_decisions = API.target_crossroad_possible_directions
        sorted_labels = sorted(self.direction_decisions, key=lambda label: cost[self.direction_decisions.index(label)])
        cost = sorted(cost)
        self.direction_decisions = list(self.direction_decisions)
        if self.previous_decision !=0 and self.direction_decisions[0].get_reverse() == self.previous_decision:
            self.direction_decisions.pop(0)
        print(self.direction_decisions)
        print(cost)
        self.previous_decision = self.direction_decisions[0]

