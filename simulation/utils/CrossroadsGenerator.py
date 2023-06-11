from .Crossroad import Crossroad
from .Direction import Direction

import numpy as np
from itertools import product

class CrossroadsGenerator:
    def __init__(self, width, height, road_padding, map_filling, rng):
        self.width = width
        self.height = height
        self.road_padding = road_padding
        self.map_filling = map_filling
        self.rng = rng

    def generate_crossroads(self):
        crossroads_coords = self.__get_crossroads_coords()
        return [Crossroad(i, x, y) for i, (x, y) in enumerate(crossroads_coords)]

    def connect_crossroads(self, crossroads):
        self.crossroads = crossroads
        for crossroad in crossroads:
            neighbors = self.__get_neighbors(crossroad, crossroads)
            for direction, neighbor in neighbors.items():
                if crossroad.connections_dirs[direction] != -1:
                    continue
                if self.__has_colliding_connection(crossroad, neighbor, direction):
                    continue
                crossroad.connect(neighbor, direction)
                neighbor.connect(crossroad, Direction.get_reverse(direction))

    def __get_crossroads_coords(self):
        points_x = np.arange(self.road_padding, self.width - self.road_padding, self.road_padding)
        points_y = np.arange(self.road_padding, self.height - self.road_padding, self.road_padding)
        points = [(x, y) for x, y in product(points_x, points_y)]
        self.rng.shuffle(points)
        num_crossroads = int(len(points) * self.map_filling)
        return points[:num_crossroads]

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

    def __get_neighbors(self, crossroad, crossroads):
        neighbors = {}
        west_neighbors = filter(lambda c: c.x < crossroad.x and c.y == crossroad.y, crossroads)
        east_neighbors = filter(lambda c: c.x > crossroad.x and c.y == crossroad.y, crossroads)
        south_neighbors = filter(lambda c: c.x == crossroad.x and c.y > crossroad.y, crossroads)
        north_neighbors = filter(lambda c: c.x == crossroad.x and c.y < crossroad.y, crossroads)

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