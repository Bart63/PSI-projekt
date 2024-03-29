from .Direction import Direction
import drivers
import math

class Vehicle:
    def __init__(self, _id: int, driver: drivers.Driver, main_vehicle=False):
        self._id = _id
        self.x = None
        self.y = None
        self.distance = 0
        self.driver = driver
        self.current_crossroad:'Crossroad' = None
        self.current_direction = None
        self.target_crossroad:'Crossroad' = None
        self.main_vehicle = main_vehicle
    
    def drive(self, x, y):
        distance = math.dist((x,y), (self.x, self.y))
        self.__add_distance(distance)
        self.x, self.y = x, y
    
    def __add_distance(self, distance: float):
        self.distance += distance
    
    def get_direction_decision(self) -> Direction:
        return self.driver.get_direction_decisions()

    def remove_direction_decision(self) -> None:
        self.driver.remove_direction_decision()
  
    def get_position(self):
        return self.x, self.y

    def on_simulation_start(self):
        self.driver.on_simulation_start()

    def on_road_start(self):
        self.driver.on_road_start()

    def on_tick(self):
        self.driver.on_tick()

    def on_road_end(self):
        self.driver.on_road_end()
