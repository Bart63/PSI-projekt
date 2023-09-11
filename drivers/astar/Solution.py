from simulation.api import API
from simulation.utils.Direction import Direction
from .utils import calculate_manhattan_distance, opposite_directions


class Solution():
    def __init__(self, prev_direction: Direction) -> None:
        self.visited_crossroads_ids = \
            [API.crossroads_pos_list.index(API.target_crossroad_pos)]
        self.cost = 0.0
        self.heuristic_cost = 0.0
        self.visited_points_no = 0

        self.points_to_visit = list(API.destinations_pos_list)
        if API.final_destination_pos in self.points_to_visit:
            self.points_to_visit.remove(API.final_destination_pos)

        self.go_to_final_destination = False
        self.directions: list[Direction] = [prev_direction]

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
        if not self.points_to_visit:
            self.heuristic_cost = 0.0
            return

        sum = routes = 0
        smallest_distance = float('inf')
        last_crossroad_id = self.visited_crossroads_ids[-1]
        for destination in self.points_to_visit:
            distance = calculate_manhattan_distance(destination,
                       API.crossroads_pos_list[last_crossroad_id])
            if distance < smallest_distance:
                smallest_distance = distance
            sum += distance
            distance = calculate_manhattan_distance(destination,
                                                    API.final_destination_pos)
            if distance < smallest_distance:
                smallest_distance = distance
            sum += distance
            routes += 2
            for destination_2 in self.points_to_visit:
                distance = calculate_manhattan_distance(destination,
                                                        destination_2)
                if distance < smallest_distance:
                    smallest_distance = distance
            routes += len(self.points_to_visit) - 1
        cars = API.cars_on_road[self.
                                visited_crossroads_ids[0]][self.directions[1]]
        self.heuristic_cost = ((sum / routes) + smallest_distance)/2 * \
            (1 + cars*0.1) * \
            (len(self.points_to_visit) + int(not self.go_to_final_destination))

    def add_crossroad(self, new_crossroad_id: int, new_direction: Direction):
        prev_cross = API.crossroads_pos_list[self.visited_crossroads_ids[-1]]
        next_cross = API.crossroads_pos_list[new_crossroad_id]
        new_cost = calculate_manhattan_distance(prev_cross, next_cross)
        prev_direction = self.directions[-1]
        self.visited_crossroads_ids.append(new_crossroad_id)
        self.directions.append(new_direction)

        if opposite_directions(prev_direction, new_direction):
            self.cost += 2*new_cost
        else:
            self.cost += new_cost
