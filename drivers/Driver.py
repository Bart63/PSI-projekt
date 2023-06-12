# base class for the drivers inherit it to do own driver
from typing import List
from simulation.utils.Direction import Direction


class Driver:
    def __init__(self):
        '''direction_decisions: stores direction decisions of type simulation.utils.Direction

        When a vehicle is ending road (entering crossroad) it will decide
        to turn left, right, back or keep straight. If a list is empty or
        the direction does not exist, it will be chosen random. While choosing
        it will also pop the first element of a list.'''
        self.direction_decisions:List[Direction] = []
    
    def on_road_start(self):
        '''First tick after switching to a new road'''
        pass

    def on_tick():
        '''Runs on every change of map'''
        pass

    def on_road_end(self):
        '''Last tick before choosing the next road'''
        pass

    def get_direction_decisions(self) -> Direction:
        return self.direction_decisions and self.direction_decisions.pop(0)
