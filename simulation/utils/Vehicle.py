from .Direction import Direction
import drivers

class Vehicle:
    from drivers import Driver
    def __init__(self, _id: int, driver: drivers.Driver, main_vehicle=False):
        self._id = _id
        self.x = None
        self.y = None
        self.driver = driver
        self.current_crossroad = None
        self.main_vehicle = main_vehicle
    
    def get_direction_decision(self) -> Direction:
        return self.driver.get_direction_decisions()
    
    def get_position(self):
        return self.x, self.y

    def on_road_start(self):
        self.driver.on_road_start()

    def on_tick(self):
        self.driver.on_tick()

    def on_road_end(self):
        self.driver.on_road_end()
