import sys
from simulation.api import API
from .Driver import Driver
from simulation.utils.Direction import Direction


class AStarDriver(Driver):
    def __init__(self):
        super().__init__()


    def deep_copy(self, list):
        list_copy = []
        for element in list:
            list_copy.append((element[0], element[1]))
        return list_copy


    def simple_copy(self, list):
        list_copy = []
        for element in list:
            list_copy.append(element)
        return list_copy


    def calculate_manhattan_distance(self, source, destination):
        return abs(source[0] - destination[0]) + abs(source[1] - destination[1])


    def avg(self, new_crossroad, destinations):
        distance = 0
        routes = 1
        for i in range(len(destinations)):
            distance += self.calculate_manhattan_distance(destinations[i], API.crossroads_pos_list[new_crossroad])
            routes += 1
            distance += self.calculate_manhattan_distance(destinations[i], API.final_destination_pos)
            routes += 1
            for j in range(len(destinations)):
                if i != j:
                    distance += self.calculate_manhattan_distance(destinations[i], destinations[j])
                    routes += 1
        if routes > 1:
            routes -= 1
        return distance / routes


    def calculate_crossroad(self, pos):
        for i in range(len(API.crossroads_pos_list)):
            crossroad = API.crossroads_pos_list[i]
            if abs(crossroad[0] - pos[0]) < 0.1 and abs(crossroad[1] - pos[1]) < 0.1:
                return i
        return None


    def calculate_next_crossroad(self, start_crossroad, direction, points_to_visit):
        check_points_to_visit = self.deep_copy(points_to_visit)
        road = API.roads_length_per_crossroad[start_crossroad][direction]
        if direction == Direction.LEFT:
            for i in range(len(check_points_to_visit)):
                point_to_visit = check_points_to_visit[i]
                if API.crossroads_pos_list[start_crossroad][1] == point_to_visit[1] and API.crossroads_pos_list[start_crossroad][0] - road <= point_to_visit[0] <= API.crossroads_pos_list[start_crossroad][0]:
                    points_to_visit.pop(i)
            return self.calculate_crossroad((API.crossroads_pos_list[start_crossroad][0] - road, API.crossroads_pos_list[start_crossroad][1]))
        elif direction == Direction.RIGHT:
            for i in range(len(check_points_to_visit)):
                point_to_visit = check_points_to_visit[i]
                if API.crossroads_pos_list[start_crossroad][1] == point_to_visit[1] and API.crossroads_pos_list[start_crossroad][0] + road >= point_to_visit[0] >= API.crossroads_pos_list[start_crossroad][0]:
                    points_to_visit.pop(i)
            return self.calculate_crossroad((API.crossroads_pos_list[start_crossroad][0] + road, API.crossroads_pos_list[start_crossroad][1]))
        elif direction == Direction.UP:
            for i in range(len(check_points_to_visit)):
                point_to_visit = check_points_to_visit[i]
                if API.crossroads_pos_list[start_crossroad][0] == point_to_visit[0] and API.crossroads_pos_list[start_crossroad][1] - road <= point_to_visit[1] <= API.crossroads_pos_list[start_crossroad][1]:
                    points_to_visit.pop(i)
            return self.calculate_crossroad((API.crossroads_pos_list[start_crossroad][0], API.crossroads_pos_list[start_crossroad][1] - road))
        else:
            for i in range(len(check_points_to_visit)):
                point_to_visit = check_points_to_visit[i]
                if API.crossroads_pos_list[start_crossroad][0] == point_to_visit[0] and API.crossroads_pos_list[start_crossroad][1] + road >= point_to_visit[1] >= API.crossroads_pos_list[start_crossroad][1]:
                    points_to_visit.pop(i)
            return self.calculate_crossroad((API.crossroads_pos_list[start_crossroad][0], API.crossroads_pos_list[start_crossroad][1] + road))


    def calculate_directions(self, points_to_visit):
        solutions = [[[self.calculate_crossroad(API.target_crossroad_pos)], 0, points_to_visit, False, []]]
        # solutions = [[[len(test_crossroads_pos_list) - 1], 0, points_to_visit, False, []]]
        while True:
            if len(solutions) == 0:
                success = False
                break
            lowest_cost_index = 0
            lowest_cost = sys.maxsize
            for solution_index in range(len(solutions)):
                if solutions[solution_index][1] < lowest_cost:
                    lowest_cost_index = solution_index
                    lowest_cost = solutions[solution_index][1]
            last_stage = solutions.pop(lowest_cost_index)
            crossroads = last_stage[0]
            points_to_visit = last_stage[2]
            go_to_final_destination = last_stage[3]
            directions = last_stage[4]
            if len(points_to_visit) == 0 and not go_to_final_destination:
                points_to_visit.append(API.final_destination_pos)
                go_to_final_destination = True
            elif len(points_to_visit) == 0:
                success = True
                solutions.insert(lowest_cost_index, last_stage)
                break
            possible_directions = API.possible_directions[crossroads[len(crossroads)-1]]
            for possible_direction in possible_directions:
                new_points_to_visit = self.deep_copy(points_to_visit)
                new_directions = self.simple_copy(directions)
                new_directions.append(possible_direction)
                new_crossroads = self.simple_copy(crossroads)
                new_crossroad = self.calculate_next_crossroad(crossroads[len(crossroads)-1], possible_direction, new_points_to_visit)
                if new_crossroad is None:
                    continue
                new_crossroads.append(new_crossroad)
                cost = 0
                for i in range(1, len(new_crossroads)):
                    previous_crossroad = new_crossroads[i - 1]
                    crossroad = new_crossroads[i]
                    cost += self.calculate_manhattan_distance(API.crossroads_pos_list[previous_crossroad], API.crossroads_pos_list[crossroad])
                cost += self.avg(new_crossroad, new_points_to_visit) * len(new_points_to_visit)
                solutions.append([new_crossroads, cost, new_points_to_visit, go_to_final_destination, new_directions])
        directions = []
        cost = sys.maxsize
        if success:
            for state in solutions:
                if cost > state[1] and len(state[2]) == 0:
                    directions = state[4]
                    cost = state[1]
        else:
            print('Failed to calculate road')
        return directions


    def on_simulation_start(self):
        super().on_simulation_start()
        destinations_pos_list = self.deep_copy(API.destinations_pos_list)
        if API.final_destination_pos in destinations_pos_list:
            destinations_pos_list.remove(API.final_destination_pos)
        self.direction_decisions = self.calculate_directions(API.destinations_pos_list)