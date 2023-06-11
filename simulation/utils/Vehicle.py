from drivers import Driver


class Vehicle:
    def __init__(self, _id: int, spawn_x: float, spawn_y: float, driver: Driver):
        self._id = _id
        self.x = spawn_x
        self.y = spawn_y
        self.driver = driver
        self.current_crossroad = None 
