# manager for all drivers and the visualization
from .Map import Map
from .MapRenderer import MapRenderer


class Simulation:
    def __init__(self, argv):
        self.map = Map(size=(512, 512), seed=0)
        self.map_renderer = MapRenderer(self.map)

    def run(self):
        print('Welcome in the Simulation!')
