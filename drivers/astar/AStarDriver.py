from simulation.api import API
from drivers.Driver import Driver
from simulation.utils.Direction import Direction
from .Solution import Solution
from .utils import get_direction_from_crossroads, calculate_crossroad_id, \
                   find_next_crossroad, point_is_on_the_road
import heapq
from copy import deepcopy

HEAVY_TRAFFIC_THRESHOLD = 3


class AStarDriver(Driver):
    def __init__(self):
        super().__init__()

    def calculate_next_solution(self, last_stage: Solution,
                                direction: Direction):
        start_crossroad_id = last_stage.visited_crossroads_ids[-1]
        start_crossroad = API.crossroads_pos_list[start_crossroad_id]
        next_crossroad = find_next_crossroad(start_crossroad_id, direction)
        next_crossroad_id = calculate_crossroad_id(next_crossroad)

        new_solution = deepcopy(last_stage)

        for point_to_visit in new_solution.points_to_visit:
            if point_is_on_the_road(point_to_visit,
                                    start_crossroad, next_crossroad):
                new_solution.points_to_visit.remove(point_to_visit)
                new_solution.visited_points_no += 1

        new_solution.add_crossroad(next_crossroad_id, direction)
        new_solution.calculate_heuristic_cost()

        return new_solution

    def calculate_best_solution(self):
        solutions: list[Solution] = [Solution(API.main_vehicle_direction)]
        while True:
            if not solutions:
                return None

            last_stage = heapq.heappop(solutions)

            if last_stage.visited_all_not_returned():
                last_stage.points_to_visit.append(API.final_destination_pos)
                last_stage.go_to_final_destination = True
            if last_stage.visited_all_and_returned():
                last_stage.directions.pop(0)
                return last_stage

            for possible_direction in API.possible_directions[
                    last_stage.visited_crossroads_ids[-1]]:
                new_solution = self.calculate_next_solution(last_stage,
                                                            possible_direction)
                heapq.heappush(solutions, new_solution)

    def calculate_directions(self):
        solution = self.calculate_best_solution()

        if solution:
            self.direction_decisions = solution.directions
        else:
            print('Failed to calculate road')

    def on_simulation_start(self):
        super().on_simulation_start()
        self.calculate_directions()

    def on_road_start(self):
        super().on_road_start()

    def on_road_end(self):
        super().on_road_end()
        cars = API.cars_on_road[API.crossroads_pos_list.index(
            API.target_crossroad_pos)][self.direction_decisions[0]]
        if cars > HEAVY_TRAFFIC_THRESHOLD:
            self.calculate_directions()
