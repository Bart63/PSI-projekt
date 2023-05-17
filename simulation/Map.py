from simulation.utils import Vehicle, Crossroad
from typing import List

class Map:
    def __init__(self):
        self.vehicles:List[Vehicle] = []
        self.crossroads:List[Crossroad] = []

    # builder methods e.g.
    def with_crossroads(self, number: int):
        # generate crossroads with given number matching builder pattern
        return self

    def default(self):
        # default map generation
        return self.with_crossroads(10)

