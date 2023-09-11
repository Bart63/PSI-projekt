from simulation.api import API
from simulation.utils.Direction import Direction


def calculate_manhattan_distance(source: tuple[float, float],
                                 destination: tuple[float, float]):
    return abs(source[0] - destination[0]) + abs(source[1] - destination[1])


def calculate_crossroad_id(crossroad_pos: tuple[float, float]):
    return API.crossroads_pos_list.index(crossroad_pos)


def find_next_crossroad(crossroad_id: int,
                        direction: Direction) -> tuple[float, float]:
    crossroad = API.crossroads_pos_list[crossroad_id]
    road_len = API.roads_length_per_crossroad[crossroad_id][direction]

    if direction == Direction.LEFT:
        return (crossroad[0]-road_len, crossroad[1])
    elif direction == Direction.RIGHT:
        return (crossroad[0]+road_len, crossroad[1])
    elif direction == Direction.UP:
        return (crossroad[0], crossroad[1]-road_len)
    elif direction == Direction.DOWN:
        return (crossroad[0], crossroad[1]+road_len)
    else:
        raise TypeError


def point_is_on_the_road(point: tuple[float, float],
                         crossroad_start: tuple[float, float],
                         crossroad_end: tuple[float, float]):
    if crossroad_start[0] == crossroad_end[0] == point[0]:
        return crossroad_start[1] <= point[1] <= crossroad_end[1] or \
               crossroad_end[1] <= point[1] <= crossroad_start[1]
    elif crossroad_start[1] == crossroad_end[1] == point[1]:
        return crossroad_start[0] <= point[0] <= crossroad_end[0] or \
               crossroad_end[0] <= point[0] <= crossroad_start[0]


def opposite_directions(direction_1: Direction, direction_2: Direction):
    return direction_1.get_reverse() == direction_2


def get_direction_from_crossroads(crossroad_start: tuple[float, float],
                                  crossroad_end: tuple[float, float]):
    if crossroad_start[0] < crossroad_end[0]:
        return Direction(Direction.RIGHT)
    elif crossroad_start[0] > crossroad_end[0]:
        return Direction(Direction.LEFT)
    elif crossroad_start[1] < crossroad_end[1]:
        return Direction(Direction.DOWN)
    elif crossroad_start[1] > crossroad_end[1]:
        return Direction(Direction.UP)
    else:
        raise ValueError
