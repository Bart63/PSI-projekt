from enum import Enum
from drivers.Driver import Driver


class Crossroad:
    def __init__(self, _id: int, x: float, y: float):
        self._id = _id
        self.x = x
        self.y = y


class VehicleOrientation(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4


class Vehicle:
    def __init__(self, _id: int, spawn_x: float, spawn_y: float, orientation: VehicleOrientation, driver: Driver):
        self._id = _id
        self.x = spawn_x
        self.y = spawn_y
        self.orientation = orientation
        self.driver = driver
