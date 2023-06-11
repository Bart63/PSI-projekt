from enum import Enum


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def get_reverse(self):
        if self == Direction.UP:
            return Direction.DOWN
        elif self == Direction.DOWN:
            return Direction.UP
        elif self == Direction.RIGHT:
            return Direction.LEFT
        elif self == Direction.LEFT:
            return Direction.RIGHT
