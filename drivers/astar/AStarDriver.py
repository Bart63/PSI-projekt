from simulation.api import API
from drivers.Driver import Driver
from simulation.utils.Direction import Direction
from .Solution import Solution
from .utils import calculate_crossroad_id, find_next_crossroad
import heapq
from .config import FAST_ASTAR_DEST_NO


class AStarDriver(Driver):
    def __init__(self):
        super().__init__()

    def calculate_next_solution(self, last_stage: Solution,
                                direction: Direction):
        start_crossroad_id = last_stage.visited_crossroads_ids[-1]
        next_crossroad = find_next_crossroad(start_crossroad_id, direction)
        next_crossroad_id = calculate_crossroad_id(next_crossroad)

        return Solution(next_crossroad_id, direction, [], last_stage)

    def calculate_best_solution(self):
        target_crossroad_id = calculate_crossroad_id(API.target_crossroad_pos)
        solutions: list[Solution] = [Solution(target_crossroad_id,
                                              API.main_vehicle_direction,
                                              API.destinations_pos_list)]
        while True:
            if not solutions:
                return None

            last_stage = heapq.heappop(solutions)

            if last_stage.visited_all_not_returned():
                last_stage.points_to_visit.append(API.final_destination_pos)
                last_stage.go_to_final_destination = True
            if last_stage.visited_all_and_returned():
                return last_stage

            for possible_direction in API.possible_directions[
                    last_stage.visited_crossroads_ids[-1]]:
                new_solution = self.calculate_next_solution(last_stage,
                                                            possible_direction)
                heapq.heappush(solutions, new_solution)

    def calculate_part_solution(self, how_many_destinations: int):
        target_crossroad_id = calculate_crossroad_id(API.target_crossroad_pos)
        points_to_visit = [self.destinations_order[i]
                           for i in range(min(how_many_destinations,
                                              len(self.destinations_order)))]
        solutions: list[Solution] = [Solution(target_crossroad_id,
                                              API.main_vehicle_direction,
                                              points_to_visit)]
        while True:
            if not solutions:
                return None

            last_stage = heapq.heappop(solutions)

            if last_stage.visited_all_not_returned() and \
               len(last_stage.visited_points) < how_many_destinations:
                last_stage.points_to_visit.append(API.final_destination_pos)
                last_stage.go_to_final_destination = True
            elif last_stage.visited_all_not_returned() or \
                    last_stage.visited_all_and_returned():
                return last_stage

            for possible_direction in API.possible_directions[
                    last_stage.visited_crossroads_ids[-1]]:
                new_solution = self.calculate_next_solution(last_stage,
                                                            possible_direction)
                heapq.heappush(solutions, new_solution)

    def calculate_destinations(self):
        solution = self.calculate_best_solution()

        if solution:
            self.destinations_order = solution.visited_points
            self.direction_decisions = [solution.directions[i] for i in
                                        range(1, len(solution.directions))]
        else:
            print('Failed to calculate road')

    def calculate_directions(self):
        solution = self.calculate_part_solution(FAST_ASTAR_DEST_NO)

        if solution:
            self.direction_decisions = [solution.directions[i] for i in
                                        range(1, len(solution.directions))]
        else:
            print('Failed to calculate road')

    def on_simulation_start(self):
        super().on_simulation_start()
        self.calculate_destinations()

    def on_road_end(self):
        super().on_road_end()
        for point in self.destinations_order:
            if point not in API.destinations_pos_list:
                self.destinations_order.remove(point)
        self.calculate_directions()
