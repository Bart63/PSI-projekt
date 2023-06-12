from .Direction import Direction

class Vehicle:
    from drivers import Driver
    def __init__(self, _id: int, driver: Driver):
        self._id = _id
        self.x = None
        self.y = None
        self.driver = driver
        self.current_crossroad = None 
    
    def get_direction_decision(self) -> Direction:
        return self.driver.get_direction_decisions()
