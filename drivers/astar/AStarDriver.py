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

        return Solution(next_crossroad_id, direction,
                        parent_solution=last_stage)

    def explore_children_solutions(self, last_stage: Solution,
                                   solutions_heap: list[Solution]):
        possible_directions = API.possible_directions[
            last_stage.visited_crossroads_ids[-1]]
        for possible_direction in possible_directions:
            new_solution = self.calculate_next_solution(last_stage,
                                                        possible_direction)
            heapq.heappush(solutions_heap, new_solution)

    def find_visited_all_solution(self, solutions: list[Solution]):
        while solutions:
            last_stage = heapq.heappop(solutions)
            if last_stage.visited_all():
                return last_stage
            self.explore_children_solutions(last_stage, solutions)
        return None

    def calculate_best_solution(self):
        target_crossroad_id = calculate_crossroad_id(API.target_crossroad_pos)
        points_to_visit: list[tuple[float, float]] = API.destinations_pos_list
        solutions: list[Solution] = [Solution(target_crossroad_id,
                                              API.main_vehicle_direction,
                                              points_to_visit,
                                              len(points_to_visit))]
        solution = self.find_visited_all_solution(solutions)

        if solution:
            self.destinations_order = solution.visited_points
            self.directions_decisions = [solution.directions[i] for i in
                                         range(1, len(solution.directions))]

    def calculate_part_solution(self):
        target_crossroad_id = calculate_crossroad_id(API.target_crossroad_pos)
        points_to_visit = [self.destinations_order[i]
                           for i in range(min(FAST_ASTAR_DEST_NO,
                                              len(self.destinations_order)))]
        solutions: list[Solution] = [Solution(target_crossroad_id,
                                              API.main_vehicle_direction,
                                              points_to_visit,
                                              FAST_ASTAR_DEST_NO)]
        solution = self.find_visited_all_solution(solutions)

        if solution:
            self.direction_decisions = [solution.directions[i] for i in
                                        range(1, len(solution.directions))]

    def on_simulation_start(self):
        super().on_simulation_start()
        self.calculate_best_solution()

    def on_road_end(self):
        super().on_road_end()
        for point in self.destinations_order:
            if point not in API.destinations_pos_list:
                self.destinations_order.remove(point)
        self.calculate_part_solution()
