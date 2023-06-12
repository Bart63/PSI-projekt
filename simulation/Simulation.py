# manager for all drivers and the visualization
from time import sleep
from .Map import Map
from .MapRenderer import MapRenderer
from .debug import plot_map
import cv2


class Simulation:
    def __init__(self, argv):
        self.map = Map(size=(512, 512), seed=0, vehicles_number=5)
        self.map_renderer = MapRenderer(self.map)

    def run(self):
        print('Welcome in the Simulation!')

        ticks = 0
        while True:
            if ticks % 20 == 5:
                self.map.switch_traffic_lights(1)
            self.map.move_map()
            plot_map(self.map)
            cv2.waitKey(200)
            ticks += 1
        
            
