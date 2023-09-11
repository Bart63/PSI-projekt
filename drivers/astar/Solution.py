from simulation.api import API
from simulation.utils.Direction import Direction
from .utils import calculate_manhattan_distance, opposite_directions, \
    point_is_on_the_road
from .config import TURN_BACK_COST_MULTIPLIER, PER_CAR_ON_ROAD_MULTIPLIER


class Solution():
    def __init__(self, next_crossroad_id: int, next_direction: Direction,
                 points_to_visit: list[tuple[float, float]],
                 parent_solution=None) -> None:
        if parent_solution:
            self.add_crossroad(parent_solution, next_crossroad_id,
                               next_direction)
            self.go_to_final_destination = parent_solution.\
                go_to_final_destination
            self.calculate_heuristic_cost()
        else:
            if points_to_visit is None:
                points_to_visit = API.destinations_pos_list
            self.init_solution(next_crossroad_id, next_direction,
                               points_to_visit)

    def add_crossroad(self, parent_solution,
                      new_crossroad_id: int, new_direction: Direction):
        prev_direction = parent_solution.directions[-1]
        prev_cross_id = parent_solution.visited_crossroads_ids[-1]
        prev_cross = API.crossroads_pos_list[prev_cross_id]
        next_cross = API.crossroads_pos_list[new_crossroad_id]

        new_cost = calculate_manhattan_distance(prev_cross, next_cross)
        total_cost = new_cost
        if opposite_directions(prev_direction, new_direction):
            total_cost += TURN_BACK_COST_MULTIPLIER*new_cost
        cars_on_road = API.cars_on_road[prev_cross_id][new_direction]
        total_cost += cars_on_road*PER_CAR_ON_ROAD_MULTIPLIER*new_cost
        self.costs = parent_solution.costs + (total_cost,)
        self.cost = parent_solution.cost + total_cost

        self.visited_crossroads_ids = parent_solution.visited_crossroads_ids \
            + (new_crossroad_id,)
        self.directions = parent_solution.directions + (new_direction,)

        self.points_to_visit = []
        self.visited_points = list(parent_solution.visited_points)
        for point_to_visit in parent_solution.points_to_visit:
            if point_is_on_the_road(point_to_visit, prev_cross, next_cross):
                self.visited_points.append(point_to_visit)
            else:
                self.points_to_visit.append(point_to_visit)

    def init_solution(self, next_crossroad_id: int,
                      next_direction: Direction,
                      points_to_visit: list[tuple[float, float]]) -> None:
        self.visited_crossroads_ids = (next_crossroad_id,)
        self.costs = (0,)
        self.cost = 0.0
        self.heuristic_cost = 0.0
        self.visited_points = []

        self.points_to_visit = list(points_to_visit)
        if API.final_destination_pos in self.points_to_visit:
            self.points_to_visit.remove(API.final_destination_pos)

        self.go_to_final_destination = False
        self.directions = (next_direction,)

    def __lt__(self, other):
        return self.cost + self.heuristic_cost < other.cost + \
            other.heuristic_cost

    def visited_all_not_returned(self):
        return not self.points_to_visit and not self.go_to_final_destination

    def visited_all_and_returned(self):
        return (not self.points_to_visit and self.go_to_final_destination)

    def get_last_visited_crossroad(self) -> tuple[float, float]:
        return API.crossroads_pos_list[self.visited_crossroads_ids[-1]]

    def calculate_heuristic_cost(self):
        sum = 0
        routes = len(self.visited_crossroads_ids) - 1
        smallest_cost = float('inf')
        for road_cost in self.costs:
            sum += road_cost
            if road_cost < smallest_cost:
                smallest_cost = road_cost
        min_adv_distance = ((sum / routes) + smallest_cost)/2
        crossroads_left = (len(self.points_to_visit) + int(
            not self.go_to_final_destination) + 1) * \
            len(self.visited_crossroads_ids) / (len(self.visited_points) + 1)
        self.heuristic_cost = min_adv_distance / crossroads_left
