from .Direction import Direction
from .TrafficLights import TrafficLights


class Crossroad:
    def __init__(self, id: int, x: float, y: float):
        self.id = id
        self.x = x
        self.y = y

        self.connections_dirs = {
            Direction.UP: -1,
            Direction.DOWN: -1,
            Direction.RIGHT: -1,
            Direction.LEFT: -1,
        }
        self.traffic_lights = TrafficLights()

    def connect(self, crossroad_id: int, direction: Direction):
        self.connections_dirs[direction] = crossroad_id
        self.traffic_lights.add_dir(direction)

    def disconnect(self, direction: Direction):
        self.connections_dirs[direction] = -1
        self.traffic_lights.remove_dir(direction)

    def get_num_connections(self):
        return len([1 for value in list(self.connections_dirs.values()) if value != -1])

    def __str__(self):
        return f'{self.id} - ({self.x}, {self.y}) {len(self.connections_dirs)}'
