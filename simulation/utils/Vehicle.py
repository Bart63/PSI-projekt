class Vehicle:
    from drivers import Driver
    def __init__(self, _id: int, driver: Driver):
        self._id = _id
        self.x = None
        self.y = None
        self.driver = driver
        self.current_crossroad = None 
