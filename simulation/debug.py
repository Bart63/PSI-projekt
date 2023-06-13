from typing import List
import cv2
from simulation import Map
from .utils import Direction, TrafficLights, Destination, Vehicle
import numpy as np

def plot_map(map: Map, connect_lvl=2):
    connect_lvl = connect_lvl / 2
    crossroads = map.crossroads
    road_padding = map.road_padding
    canvas_size = (map.width, map.height)
    canvas = 255 * np.ones((canvas_size[0], canvas_size[1], 3), dtype=np.uint8)

    plot_vehicles(map.vehicles, canvas)
    plot_destinations(map.destinations, canvas)

    for crossroad in crossroads:
        x = crossroad.x
        y = crossroad.y
        plot_traffic_lights(crossroad.traffic_lights, canvas, x, y)

    for crossroad in crossroads:
        x = crossroad.x
        y = crossroad.y

        # Plotting lines for each direction
        for direction, connection in crossroad.connections_dirs.items():
            if connection != -1:
                if direction == Direction.UP:
                    cv2.line(canvas, (x, y), (x, y - int(road_padding * connect_lvl)), (0, 0, 0), 1)  # Upward line
                elif direction == Direction.DOWN:
                    cv2.line(canvas, (x, y), (x, y + int(road_padding * connect_lvl)), (0, 0, 0), 1)  # Downward line
                elif direction == Direction.RIGHT:
                    cv2.line(canvas, (x, y), (x + int(road_padding * connect_lvl), y), (0, 0, 0), 1)  # Rightward line
                elif direction == Direction.LEFT:
                    cv2.line(canvas, (x, y), (x - int(road_padding * connect_lvl), y), (0, 0, 0), 1)  # Leftward line

    cv2.namedWindow('Map', cv2.WINDOW_NORMAL)
    cv2.imshow("Map", canvas)

def plot_traffic_lights(traffic_lights: TrafficLights, canvas, x, y, width=10):
    connections_dirs = traffic_lights.connections_dirs
    horizontal_traffic = traffic_lights.horizontal_traffic
    vertical_traffic = traffic_lights.vertical_traffic

    half_width = width // 2

    center = (x, y)
    vertices = [
        (x - half_width, y - half_width),
        (x + half_width, y - half_width),
        (x + half_width, y + half_width),
        (x - half_width, y + half_width)
    ]

    triangles = [
        (vertices[0], vertices[1], center, Direction.UP),
        (vertices[1], vertices[2], center, Direction.RIGHT),
        (vertices[2], vertices[3], center, Direction.DOWN),
        (vertices[3], vertices[0], center, Direction.LEFT)
    ]

    for *triangle_vertices, direction in triangles:
        connection = connections_dirs[direction]
        if connection is None:
            continue
        traffic_state = horizontal_traffic if direction.is_horizontal() else vertical_traffic
        triangle_color = (0, 255, 0) if traffic_state else (0, 0, 255)
        cv2.fillPoly(canvas, [np.array(triangle_vertices, np.int32)], triangle_color)


def plot_destinations(destinations: List[Destination], canvas, radius=10):
    for dest in destinations:
        center = (dest.x, dest.y)
        color = (255, 255, 0) if dest.is_last else (0, 255, 255)
        cv2.circle(canvas, center, radius, color, -1)


def plot_vehicles(vehicles: List[Vehicle], canvas, radius=10):
    for vhc in vehicles:
        center = (int(vhc.x), int(vhc.y))
        color = (0, 0, 255) if vhc.main_vehicle else (255, 0, 0)
        cv2.circle(canvas, center, radius, color, -1)
