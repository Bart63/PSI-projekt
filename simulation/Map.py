from .utils import Direction, Vehicle, Crossroad
from drivers import DummyDriver
from itertools import product
from typing import List

import numpy as np


class Map:

    def __init__(self, size: tuple[int, int], seed: int, road_padding=50, map_filling=.7, vehicles_number=10, driver=DummyDriver):
        self.vehicles: List[Vehicle] = []
        self.crossroads: List[Crossroad] = []
        self.width, self.height = size
        self.rng = np.random.default_rng(seed)
        self.road_padding = road_padding
        self.__generate_crossroads(map_filling)
        self.__add_vehicles(vehicles_number)

        from .debug import plot_map
        plot_map(self)

    def __get_crossroads_coords(self, map_filling:float):
        points_x = np.arange(self.road_padding, self.width - self.road_padding, self.road_padding)
        points_y = np.arange(self.road_padding, self.height - self.road_padding, self.road_padding)
        points = [(x, y) for x, y in product(points_x, points_y)]
        self.rng.shuffle(points)
        num_crossroads = int(len(points) * map_filling)
        return points[:num_crossroads]

    def __generate_crossroads(self, map_filling: float):
        points = self.__get_crossroads_coords(map_filling)
        self.crossroads = [Crossroad(i, x, y) for i, (x, y) in enumerate(points)]
        self.__connect_crossroads()

    def __connect_crossroads(self):
        for crossroad in self.crossroads:
            neighbors = self.__get_neighbors(crossroad)
            for direction, neighbor in neighbors.items():
                if crossroad.connections_dirs[direction] != -1:
                    continue
                if self.__has_colliding_connection(crossroad, neighbor, direction):
                    continue
                crossroad.connect(neighbor.id, direction)
                neighbor.connect(crossroad.id, Direction.get_reverse(direction))

        
    def __has_colliding_connection(self, crossroad, neighbor, direction):
        is_vertical = direction in (Direction.UP, Direction.DOWN)
        start, end = sorted([crossroad.y, neighbor.y] if is_vertical else [crossroad.x, neighbor.x])
        fixed_coord = crossroad.x if is_vertical else crossroad.y
        step = self.road_padding
        return any(
            self.__is_crossroad_present(coord, fixed_coord, is_vertical)
            for coord in range(start + step, end, step)
        )

    def __is_crossroad_present(self, coord, fixed_coord, is_vertical=True):
        crossroads = [c for c in self.crossroads if c.y == coord] if is_vertical else [c for c in self.crossroads if c.x == coord]
        if not crossroads:
            return False
        if is_vertical:
            left_crossroad = max((c for c in crossroads if c.x < fixed_coord), key=lambda c: c.x, default=None)
            right_crossroad = min((c for c in crossroads if c.x > fixed_coord), key=lambda c: c.x, default=None)
            return (
                left_crossroad and left_crossroad.connections_dirs[Direction.RIGHT] != -1
            ) or (
                right_crossroad and right_crossroad.connections_dirs[Direction.LEFT] != -1
            )
        else:
            up_crossroad = max((c for c in crossroads if c.y < fixed_coord), key=lambda c: c.y, default=None)
            down_crossroad = min((c for c in crossroads if c.y > fixed_coord), key=lambda c: c.y, default=None)
            return (
                up_crossroad and up_crossroad.connections_dirs[Direction.DOWN] != -1
            ) or (
                down_crossroad and down_crossroad.connections_dirs[Direction.UP] != -1
            )

    def __get_neighbors(self, crossroad):
        neighbors = {}
        west_neighbors = filter(lambda c: c.x < crossroad.x and c.y == crossroad.y, self.crossroads)
        east_neighbors = filter(lambda c: c.x > crossroad.x and c.y == crossroad.y, self.crossroads)
        south_neighbors = filter(lambda c: c.x == crossroad.x and c.y > crossroad.y, self.crossroads)
        north_neighbors = filter(lambda c: c.x == crossroad.x and c.y < crossroad.y, self.crossroads)

        left_neighbor = min(west_neighbors, key=lambda c: crossroad.x - c.x, default=None)
        right_neighbor = min(east_neighbors, key=lambda c: c.x - crossroad.x, default=None)
        down_neighbor = min(south_neighbors, key=lambda c: c.y - crossroad.y, default=None)
        up_neighbor = min(north_neighbors, key=lambda c: crossroad.y - c.y, default=None)

        if left_neighbor:
            neighbors[Direction.LEFT] = left_neighbor
        if right_neighbor:
            neighbors[Direction.RIGHT] = right_neighbor
        if down_neighbor:
            neighbors[Direction.DOWN] = down_neighbor
        if up_neighbor:
            neighbors[Direction.UP] = up_neighbor

        return neighbors

    def __add_vehicles(self, vehicles_number):
        for id_ in range(vehicles_number):
            # TODO spawn points need to be counted and orientation according to the roads
            vehicle = Vehicle(id_, spawn_x=0, spawn_y=0, driver=DummyDriver())
            self.vehicles.append(vehicle)
