from simulation.utils import Vehicle, Crossroad
from simulation.utils.Direction import Direction
from simulation.utils.VehicleOrientation import VehicleOrientation
from drivers.DummyDriver import DummyDriver
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt


# assume that (0, 0) is ihe left up corner
def check_crossroads(crossroads):
    for crossroad in crossroads:
        if crossroad.get_num_connections() < 1:
            return False
    return True


class Map:

    def __init__(self, size: tuple[int, int], seed: int, road_padding=50, map_filling=1, vehicles_number=10, driver=DummyDriver):
        self.vehicles: list[Vehicle] = []
        self.crossroads: list[Crossroad] = []
        self.width = size[0]
        self.height = size[1]
        self.rng = np.random.default_rng(seed)
        self.road_padding = road_padding
        self.driver = driver
        self.__generate_crossroads(map_filling)
        self.__add_vehicles(vehicles_number)

    def start(self):
        for crossroad in self.crossroads:
            crossroad.start()
        for vehicle in self.vehicles:
            vehicle.start()

    def __get_potential_crossroads_coords(self):
        points_x = np.arange(self.road_padding, self.width - self.road_padding, self.road_padding)
        points_y = np.arange(self.road_padding, self.height - self.road_padding, self.road_padding)
        points = [[(x, y) for x in points_x] for y in points_y]
        return points

    def __generate_crossroads(self, map_filling: float):
        points = self.__get_potential_crossroads_coords()
        potential_crossroads: list[Crossroad] = []
        for i, row in enumerate(points):
            for j, (x_coord, y_coord) in enumerate(row):
                crossroad = Crossroad(len(potential_crossroads), x_coord, y_coord)
                potential_crossroads.append(crossroad)

        if map_filling >= 1.0:
            self.crossroads = potential_crossroads
            return
        self.__remove_crossroads(points, 1 - map_filling)

    def __remove_crossroads(self, points, part):
        for i, row in enumerate(points):
            for j, _ in enumerate(row):
                up = self.crossroads[(i - 1) * len(row) + j] if i > 0 else None
                down = self.crossroads[(i + 1) * len(row) + j] if i < len(points) - 1 else None
                left = self.crossroads[i * len(row) + j - 1] if j > 0 else None
                right = self.crossroads[i * len(row) + j + 1] if j < len(row) - 1 else None

                self.crossroads[i * len(row) + j].connect(up.id_, Direction.UP) if up else None
                self.crossroads[i * len(row) + j].connect(down.id_, Direction.DOWN) if down else None
                self.crossroads[i * len(row) + j].connect(left.id_, Direction.LEFT) if left else None
                self.crossroads[i * len(row) + j].connect(right.id_, Direction.RIGHT) if right else None

        for crossroad in self.crossroads:
            print(crossroad)
        to_delete_num = int(part * len(self.crossroads))
        crossroad_to_delete = self.rng.choice(len(self.crossroads), to_delete_num, replace=False)
        print(crossroad_to_delete)
        potential_crossroads_dict = {crossroad.id_: crossroad for crossroad in self.crossroads}
        temp_crossroads: dict[int, Crossroad] = deepcopy(potential_crossroads_dict)
        for index in crossroad_to_delete:
            print(index)
            crossroad: Crossroad = temp_crossroads[index]

            left_id = crossroad.connections_dirs[Direction.LEFT]
            right_id = crossroad.connections_dirs[Direction.RIGHT]
            up_id = crossroad.connections_dirs[Direction.UP]
            down_id = crossroad.connections_dirs[Direction.DOWN]

            print(left_id, right_id, up_id, down_id)

            temp_crossroads[left_id].disconnect(Direction.RIGHT) if left_id != -1 else None
            temp_crossroads[right_id].disconnect(Direction.LEFT) if right_id != -1 else None
            temp_crossroads[up_id].disconnect(Direction.DOWN) if up_id != -1 else None
            temp_crossroads[down_id].disconnect(Direction.UP) if down_id != -1 else None

            if left_id != -1 and right_id != -1:
                temp_crossroads[left_id].connect(right_id, Direction.RIGHT)
                temp_crossroads[right_id].connect(left_id, Direction.LEFT)

            elif down_id != -1 and up_id != -1:
                temp_crossroads[down_id].connect(up_id, Direction.UP)
                temp_crossroads[up_id].connect(down_id, Direction.DOWN)

            temp_crossroads.pop(index)

            # check if everything is ok
            if not check_crossroads(temp_crossroads.values()):
                continue

            crossroad: Crossroad = potential_crossroads_dict[index]

            left_id = crossroad.connections_dirs[Direction.LEFT]
            right_id = crossroad.connections_dirs[Direction.RIGHT]
            up_id = crossroad.connections_dirs[Direction.UP]
            down_id = crossroad.connections_dirs[Direction.DOWN]

            potential_crossroads_dict[left_id].disconnect(Direction.RIGHT) if left_id != -1 else None
            potential_crossroads_dict[right_id].disconnect(Direction.LEFT) if right_id != -1 else None
            potential_crossroads_dict[up_id].disconnect(Direction.DOWN) if up_id != -1 else None
            potential_crossroads_dict[down_id].disconnect(Direction.UP) if down_id != -1 else None

            if left_id != -1 and right_id != -1:
                potential_crossroads_dict[left_id].connect(right_id, Direction.RIGHT)
                potential_crossroads_dict[right_id].connect(left_id, Direction.LEFT)

            elif down_id != -1 and up_id != -1:
                potential_crossroads_dict[down_id].connect(up_id, Direction.UP)
                potential_crossroads_dict[up_id].connect(down_id, Direction.DOWN)

            potential_crossroads_dict.pop(index)
        x_p = []
        y_p = []
        y_l = []
        for xd in list(potential_crossroads_dict.values()):
            x_p.append(xd.x)
            y_p.append(xd.y)
            y_l.append(xd.get_num_connections())
            print(xd)
        print(y_l)
        plt.scatter(x_p, y_p, c=y_l)
        plt.show()

    def __add_vehicles(self, vehicles_number):
        for id_ in range(vehicles_number):
            # TODO spawn points need to be counted and orientation according to the roads
            vehicle = Vehicle(id_, spawn_x=0, spawn_y=0, orientation=VehicleOrientation.RIGHT, driver=self.driver)
            self.vehicles.append(vehicle)
