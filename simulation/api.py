'''API for drivers about map and main vehicle

Let's assume there is only one main vehicle. 
The API class can then a static class with fields accessible
without the need to create an object of that class.'''

from typing import Dict, List, Tuple
from .utils.Direction import Direction

import inspect


class MetaAPI(type):
    _main_vehicle_pos: Tuple[float, float] = None
    '''Main vehicle position on a map'''

    _main_vehicle_direction: Direction = None
    '''Current direction of main vehicle'''

    _target_crossroad_pos: Tuple[float, float] = None
    '''Position of the target crossroad'''

    _target_crossroad_possible_directions: List[Direction] = None
    '''Possible directions for the target crossroad'''

    _crossroads_pos_list: List[Tuple[float, float]] = None
    '''Crossroads list of positions'''

    _possible_directions: List[List[Direction]] = None
    '''Possible directions for every crossroad'''

    _roads_length_per_crossroad: List[Dict[Direction, float]] = None
    '''Length of every road from every crossroad'''

    _cars_on_road: List[Dict[Direction, int]] = None
    '''Number of cars on every road from every crossroad'''

    _destinations_pos_list: List[Tuple[float, float]] = None
    '''Destinations list of positions except the last destination'''

    _final_destination_pos: Tuple[float, float] = None
    '''Destinations list of positions except the last destination'''


    @staticmethod
    def _check_access():
        frame = inspect.currentframe().f_back
        while frame is not None:
            module_name = inspect.getmodule(frame).__name__
            if module_name.startswith('drivers'):
                raise PermissionError(f"Access denied from {module_name}")
            frame = frame.f_back

    @classmethod
    def _get_property(cls, prop_name):
        return getattr(cls, prop_name)

    @classmethod
    def _set_property(cls, prop_name, value):
        cls._check_access()
        setattr(cls, prop_name, value)

    @property
    def main_vehicle_pos(self):
        return self._get_property('_main_vehicle_pos')

    @main_vehicle_pos.setter
    def main_vehicle_pos(self, value):
        self._set_property('_main_vehicle_pos', value)

    @property
    def main_vehicle_direction(self):
        return self._get_property('_main_vehicle_direction')

    @main_vehicle_direction.setter
    def main_vehicle_direction(self, value):
        self._set_property('_main_vehicle_direction', value)

    @property
    def target_crossroad_pos(self):
        return self._get_property('_target_crossroad_pos')

    @target_crossroad_pos.setter
    def target_crossroad_pos(self, value):
        self._set_property('_target_crossroad_pos', value)

    @property
    def target_crossroad_possible_directions(self):
        return self._get_property('_target_crossroad_possible_directions')

    @target_crossroad_possible_directions.setter
    def target_crossroad_possible_directions(self, value):
        self._set_property('_target_crossroad_possible_directions', value)

    @property
    def crossroads_pos_list(self):
        return self._get_property('_crossroads_pos_list')

    @crossroads_pos_list.setter
    def crossroads_pos_list(self, value):
        self._set_property('_crossroads_pos_list', value)

    @property
    def possible_directions(self):
        return self._get_property('_possible_directions')

    @possible_directions.setter
    def possible_directions(self, value):
        self._set_property('_possible_directions', value)

    @property
    def roads_length_per_crossroad(self):
        return self._get_property('_roads_length_per_crossroad')

    @roads_length_per_crossroad.setter
    def roads_length_per_crossroad(self, value):
        self._set_property('_roads_length_per_crossroad', value)

    @property
    def cars_on_road(self):
        return self._get_property('_cars_on_road')

    @cars_on_road.setter
    def cars_on_road(self, value):
        self._set_property('_cars_on_road', value)

    @property
    def destinations_pos_list(self):
        return self._get_property('_destinations_pos_list')

    @destinations_pos_list.setter
    def destinations_pos_list(self, value):
        self._set_property('_destinations_pos_list', value)

    @property
    def final_destination_pos(self):
        return self._get_property('_final_destination_pos')

    @final_destination_pos.setter
    def final_destination_pos(self, value):
        self._set_property('_final_destination_pos', value)


class API(metaclass=MetaAPI):
    pass
