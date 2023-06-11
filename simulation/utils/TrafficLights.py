from .Direction import Direction


class TrafficLights:
    def __init__(self):
        self.connections_dirs = {
            Direction.UP: False,
            Direction.DOWN: False,
            Direction.RIGHT: False,
            Direction.LEFT: False,
        }
        self.horizontal_traffic = None
        self.vertical_traffic = None

    def add_dir(self, direction):
        self.connections_dirs[direction] = True

    def remove_dir(self, direction):
        self.connections_dirs[direction] = False

    def start(self):
        connection_values = list(self.connections_dirs.values())
        connections = sum(connection_values)
        if connections >= 3:
            self.horizontal_traffic = True
            self.vertical_traffic = False

    def switch_state(self):
        if self.horizontal_traffic is not None:
            self.horizontal_traffic = not self.horizontal_traffic
        if self.vertical_traffic is not None:
            self.vertical_traffic = not self.vertical_traffic

    def get_state(self):
        return self.horizontal_traffic, self.vertical_traffic
