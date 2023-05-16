# manager for all drivers and the visualization
from simulation.Map import Map
from simulation.MapRenderer import MapRenderer


class Simulation:
    def __init__(self, argv):
        self.map = Map().default()
        self.map_renderer = MapRenderer()

    def run(self):
        print('Welcome in the Simulation!')
