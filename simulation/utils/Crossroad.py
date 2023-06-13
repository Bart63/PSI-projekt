from typing import Dict
from .Vehicle import Vehicle
from .VehicleQueue import VehicleQueue
from .Direction import Direction
from .TrafficLights import TrafficLights
from math import sqrt

class Crossroad:
    def __init__(self, id: int, x: float, y: float, rng):
        self.id = id
        self.x = x
        self.y = y
        self.rng = rng

        self.connections_dirs = {
            Direction.UP: -1,
            Direction.DOWN: -1,
            Direction.RIGHT: -1,
            Direction.LEFT: -1,
        }

        self.vehicle_queue:Dict[Direction, VehicleQueue] = {
            Direction.UP: -1,
            Direction.DOWN: -1,
            Direction.RIGHT: -1,
            Direction.LEFT: -1,
        }

        self.traffic_lights = TrafficLights()

    def get_position(self):
        return self.x, self.y

    def connect(self, crossroad:'Crossroad', direction: Direction):
        self.connections_dirs[direction] = crossroad
        is_green_callbac = lambda: crossroad.traffic_lights.horizontal_traffic if direction in [Direction.LEFT, Direction.RIGHT] else crossroad.traffic_lights.vertical_traffic
        self.vehicle_queue[direction] = VehicleQueue(self.get_distance_between(crossroad), (self.x, self.y), (crossroad.x, crossroad.y), is_green_callbac)
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

    def switch_traffic_lights(self):
        self.traffic_lights.switch_state()
    
    def get_connections(self):
        return list(filter(lambda conn: conn != -1, self.connections_dirs.values()))
    
    def enqueue_vehicle(self, vehicle: Vehicle, direction: Direction):
        vehicle.current_crossroad = self
        vehicle.current_direction = direction
        vehicle.target_crossroad = self.connections_dirs[direction]
        vehicle.x, vehicle.y = self.x, self.y
        self.vehicle_queue[direction].enqueue(vehicle)
    
    def move_vehicles(self):
        for direction, queue in self.vehicle_queue.items():
            if queue == -1:
                continue
            finished_vehicles = queue.move_closer()
            for v in finished_vehicles:
                self.__choose_road(v, direction)

    def __choose_road(self, vehicle:Vehicle, direction: Direction):
        next_crossroad = self.connections_dirs[direction]
        possible_directions = [direction for direction, crossroad in next_crossroad.connections_dirs.items() if crossroad != -1]
        chosen_direction = vehicle.get_direction_decision()
        if chosen_direction not in possible_directions:
            chosen_direction = self.rng.choice(possible_directions)
        next_crossroad.enqueue_vehicle(vehicle, chosen_direction)

    def get_connection_directions(self):
        return [di for di, conn in self.connections_dirs.items() if conn != -1]
    
    def get_road_length(self, direction:Direction):
        if self.vehicle_queue[direction] == -1:
            raise Exception('No road in this direction')
        return self.vehicle_queue[direction].road_length

    def get_num_connections(self):
        return len([1 for value in list(self.connections_dirs.values()) if value != -1])

    def __str__(self):
        return f'{self.id} - ({self.x}, {self.y}) {len(self.connections_dirs)}'
