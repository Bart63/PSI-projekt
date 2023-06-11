from simulation import Map
from .utils import Direction

import matplotlib.pyplot as plt

def plot_map(map: Map, connect_lvl=2):
    connect_lvl = connect_lvl / 2
    crossroads = map.crossroads
    road_padding = map.road_padding
    for crossroad in crossroads:
        x = crossroad.x
        y = -crossroad.y    # Make (0,0) in upper left corner

        # Plotting lines for each direction
        for direction, connection in crossroad.connections_dirs.items():
            if connection != -1:
                if direction == Direction.UP:
                    plt.plot([x, x], [y, y + int(road_padding * connect_lvl)], 'k-')  # Upward line
                elif direction == Direction.DOWN:
                    plt.plot([x, x], [y, y - int(road_padding * connect_lvl)], 'k-')  # Downward line
                elif direction == Direction.RIGHT:
                    plt.plot([x, x + int(road_padding * connect_lvl)], [y, y], 'k-')  # Rightward line
                elif direction == Direction.LEFT:
                    plt.plot([x, x - int(road_padding * connect_lvl)], [y, y], 'k-')  # Leftward line
                    
    for crossroad in crossroads:
        x = crossroad.x
        y = -crossroad.y    # Make (0,0) in upper left corner
        plt.plot(x, y, 'ro')  # Plotting a red dot for each crossroad

    plt.show()