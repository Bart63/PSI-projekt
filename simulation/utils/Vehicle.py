from .Direction import Direction
import drivers

class Vehicle:
    from drivers import Driver
    def __init__(self, _id: int, driver: drivers.Driver):
        self._id = _id
        self.x = None
        self.y = None
        self.driver = driver
        self.current_crossroad = None 
    
    def get_direction_decision(self) -> Direction:
        return self.driver.get_direction_decisions()

    def on_road_start(self):
        self.driver.on_road_start()

    def on_tick(self):
        self.driver.on_tick()

    def on_road_end(self):
        self.driver.on_road_end()
