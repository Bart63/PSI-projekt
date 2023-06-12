from .Vehicle import Vehicle
from .VehicleQueue import VehicleQueue
from .Direction import Direction
from .TrafficLights import TrafficLights
from math import sqrt

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

        self.vehicle_queue = {
            Direction.UP: -1,
            Direction.DOWN: -1,
            Direction.RIGHT: -1,
            Direction.LEFT: -1,
        }

        self.traffic_lights = TrafficLights()

    def connect(self, crossroad, direction: Direction):
        self.connections_dirs[direction] = crossroad
        self.vehicle_queue[direction] = VehicleQueue(self.get_distance_between(crossroad), (self.x, self.y), (crossroad.x, crossroad.y))
        self.traffic_lights.add_dir(direction)
    
    def get_distance_between(self, cr_other):
        x1, x2 = self.x, cr_other.x
        y1, y2 = self.y, cr_other.y
        dist = sqrt(abs(x1-x2)**2 + abs(y1-y2)**2)
        return dist

    def disconnect(self, direction: Direction):
        self.connections_dirs[direction] = -1
        self.vehicle_queue[direction] = -1
        self.traffic_lights.remove_dir(direction)
    
    def get_connections(self):
        return list(filter(lambda conn: conn != -1, self.connections_dirs.values()))
    
    def enqueue_vehicle(self, vehicle: Vehicle, direction: Direction):
        vehicle.current_crossroad = self
        self.vehicle_queue[direction].enqueue(vehicle)
    
    def move_vehicles(self):
        for direction, queue in self.vehicle_queue.items():
            if queue == -1:
                continue
            finished_vehicles = queue.move_closer()
            for v in finished_vehicles:
                self.enqueue_vehicle(v, direction) # Wrong

    def get_connection_directions(self):
        return [di for di, conn in self.connections_dirs.items() if conn != -1]

    def get_num_connections(self):
        return len([1 for value in list(self.connections_dirs.values()) if value != -1])

    def __str__(self):
        return f'{self.id} - ({self.x}, {self.y}) {len(self.connections_dirs)}'
