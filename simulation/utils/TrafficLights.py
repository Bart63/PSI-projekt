from .Direction import Direction


class TrafficLights:
    def __init__(self):
        self.connections_dirs = {
            Direction.UP: None,
            Direction.DOWN: None,
            Direction.RIGHT: None,
            Direction.LEFT: None,
        }
        self.horizontal_traffic = True
        self.vertical_traffic = False

    def add_dir(self, direction):
        self.connections_dirs[direction] = True

    def remove_dir(self, direction):
        self.connections_dirs[direction] = False

    def switch_state(self):
        if self.horizontal_traffic is not None:
            self.horizontal_traffic = not self.horizontal_traffic
        if self.vertical_traffic is not None:
            self.vertical_traffic = not self.vertical_traffic

    def get_state(self):
        return self.horizontal_traffic, self.vertical_traffic
