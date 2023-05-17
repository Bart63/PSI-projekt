from drivers.Driver import Driver
from .VehicleOrientation import VehicleOrientation

class Vehicle:
    def __init__(self, _id: int, spawn_x: float, spawn_y: float, orientation: VehicleOrientation, driver: Driver):
        self._id = _id
        self.x = spawn_x
        self.y = spawn_y
        self.orientation = orientation
        self.driver = driver
