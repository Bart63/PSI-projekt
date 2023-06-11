from typing import List
from simulation import Map
from .utils import Direction, TrafficLights, Destination

import matplotlib.pyplot as plt

def plot_map(map: Map, connect_lvl=2):
    connect_lvl = connect_lvl / 2
    crossroads = map.crossroads
    road_padding = map.road_padding

    plot_destinations(map.destinations)

    for crossroad in crossroads:
        x = crossroad.x
        y = -crossroad.y
        plot_traffic_lights(crossroad.traffic_lights, x, y)

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

    plt.show()


def plot_traffic_lights(traffic_lights: TrafficLights, x, y, width=10):
    connections_dirs = traffic_lights.connections_dirs
    horizontal_traffic = traffic_lights.horizontal_traffic
    vertical_traffic = traffic_lights.vertical_traffic

    half_width = width / 2

    center = (x, y)
    vertices = [
        (x - half_width, y - half_width),
        (x + half_width, y - half_width),
        (x + half_width, y + half_width),
        (x - half_width, y + half_width)
    ]

    triangles = [
        (vertices[0], vertices[1], center, Direction.DOWN),
        (vertices[1], vertices[2], center, Direction.RIGHT),
        (vertices[2], vertices[3], center, Direction.UP),
        (vertices[3], vertices[0], center, Direction.LEFT)
    ]

    for *triangle_vertices, direction in triangles:
        connection = connections_dirs[direction]
        if connection == None:
            continue
        traffic_state = horizontal_traffic if direction.is_horizontal() else vertical_traffic
        triangle_color = 'green' if traffic_state else 'red'
        plt.fill(*zip(*triangle_vertices), color=triangle_color, zorder=10)


def plot_destinations(destinations: List[Destination], radius=10):
    for dest in destinations:
        circle = plt.Circle((dest.x, -dest.y), radius, color='yellow', alpha=0.9)
        plt.gca().add_patch(circle)
