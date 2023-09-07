# example implementation of driver
from simulation.api import API
from .Driver import Driver
from simulation.utils.Direction import Direction


class AStarDriver(Driver):
    def __init__(self):
        super().__init__()

    def on_simulation_start(self):
        super().on_simulation_start()
        self.direction_decisions = [Direction.DOWN, Direction.RIGHT,  Direction.DOWN,  Direction.LEFT, Direction.DOWN, Direction.LEFT, Direction.LEFT, Direction.UP, Direction.UP, Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.RIGHT]