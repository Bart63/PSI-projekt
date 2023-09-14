import numpy as np
from simulation.utils.Direction import Direction


DIRECTIONS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


class Node:
    def __init__(self, x, y, parent):
        self.x = x
        self.y = y
        self.parent = parent


def back_propagate(history: Node):
    """
    Back propagate through all moves and returns first one.
    :param history: Last position of car.
    :return: First position of car after first move, and steps to goal.
    """
    steps, goal = 0, history

    while history.parent != [-1, -1]:
        steps += 1
        goal = history
        history = history.parent

    return goal, steps


def navigate_car(car_pos, car_direction):  # TODO check if this is working - directions are interpreted correctly.
    """
    Base on initial car position and first move to get to goal returns move that should be done.
    :param car_pos: Initial car position.
    :param car_direction: Car first move direction.
    :return: Correct move.
    """
    change_x = car_pos[0] - car_direction[0]
    change_y = car_pos[1] - car_direction[1]

    if change_x == 1:
        return Direction.LEFT
    if change_x == -1:
        return Direction.RIGHT

    if change_y == 1:
        return Direction.UP
    if change_y == -1:
        return Direction.DOWN

    return None


def run_BFS(map: np.ndarray, car_pos: [float, float]):
    """
    Run BFS search and base of found move steer the car.
    :param map: 2d array with positions of cars, and goal's.
    :param car_pos: position of player car, as [x, y].
    """
    # map = ...(map)  # TODO modify map such that it has info about other cars and goals.
    visited_node = 1
    other_cars = 2  # TODO set it in map.
    goal = 3  # TODO value of goal in map, set it in map.

    stack = []
    car_pos_x, car_pos_y = car_pos
    stack.append(Node(car_pos_x, car_pos_y, [-1, -1]))  # Pushing initial car pos into stack.

    map_width, map_height = map.shape  # TODO check if this works. If not set it different way.

    while len(stack) != 0:  # break if stack is empty.
        position = stack.pop(0)
        for move in DIRECTIONS:  # iterate over all moves.
            new_x, new_y = position.x + move[0], position.y + move[1]

            # Check if new node outside maze boundary.
            if new_y < 0 or new_x < 0 or new_x >= map_width or new_y >= map_height:
                continue

            # Check if new node was visited or is blue car.
            if map[new_x, new_y] == other_cars or map[new_x, new_y] == visited_node:
                continue

            # Check if new move is target.
            if map[new_x, new_y] == goal:
                # TODO This should work, but if code is not working error might be below
                direction_to_go, steps = back_propagate(position)
                if steps == 0:
                    turn = navigate_car([car_pos.x, car_pos.y], [new_x, new_y])
                else:
                    turn = navigate_car([car_pos.x, car_pos.y], [direction_to_go.x, direction_to_go.y])

                if turn is not None:
                    pass  # TODO Call turn here with "turn"
                else:
                    print(f"TURN {turn}")  # Something went wrong.
                break

            # If new node wasn't visited before, and it is not another car, append it to stack and mark as visited.
            stack.append(Node(x=new_x, y=new_y, parent=position))
            map[new_x, new_y] = visited_node
