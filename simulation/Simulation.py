# manager for all drivers and the visualization
from time import sleep
from .Map import Map
from .MapRenderer import MapRenderer


class Simulation:
    def __init__(self, argv):
        self.map = Map(size=(512, 512), seed=0)
        self.map_renderer = MapRenderer(self.map)

    def run(self):
        print('Welcome in the Simulation!')

        while True:
            self.map.move_map()
            sleep(0.2)
        
            
