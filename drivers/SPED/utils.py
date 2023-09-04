import numpy as np
import copy
def get_next_possible_xroad_coords(map_tensor, direction, vehicle_pos):
    pos_row = vehicle_pos[0]
    pos_column = vehicle_pos[1]
    if direction == 1:
        while True:
            map_tensor[13][pos_row][pos_column] = 0
            map_tensor[15][pos_row-1][pos_column] = 0
            pos_row -= 1
            if map_tensor[0][pos_row][pos_column] == 1:
                return pos_row, pos_column, map_tensor
    elif direction == 2:
        while True:
            map_tensor[14][pos_row][pos_column] = 0
            map_tensor[16][pos_row][pos_column+1] = 0
            pos_column += 1
            if map_tensor[0][pos_row][pos_column] == 1:
                return pos_row, pos_column, map_tensor
    elif direction == 3:
        while True:
            map_tensor[15][pos_row][pos_column] = 0
            map_tensor[13][pos_row+1][pos_column] = 0
            pos_row += 1
            if map_tensor[0][pos_row][pos_column] == 1:
                return pos_row, pos_column, map_tensor
    elif direction == 4:
        while True:
            map_tensor[16][pos_row][pos_column] = 0
            map_tensor[14][pos_row][pos_column-1] = 0
            pos_column -= 1
            if map_tensor[0][pos_row][pos_column] == 1:
                return pos_row, pos_column, map_tensor


def take_action(map_tensor, direction):
    shape = map_tensor.shape[1:]
    new_map_tensor = copy.copy(map_tensor)
    previous_vehicle_position = np.argwhere(new_map_tensor[18] == 1)[0]
    new_pos_row, new_pos_column, new_map_tensor = get_next_possible_xroad_coords(new_map_tensor, direction, previous_vehicle_position)
    new_map_tensor[18] = np.zeros(shape)
    new_map_tensor[18][new_pos_row][new_pos_column] = 1
    new_map_tensor[18 + direction] = np.zeros(shape)
    new_map_tensor[18 + direction][new_pos_row][new_pos_column] = 1
    return new_map_tensor

def get_available_directions(map_tensor):
    vehicle_position = np.argwhere(map_tensor[18] == 1)[0]
    vehicle_row = vehicle_position[0]
    vehicle_column = vehicle_position[1]
    directions = []
    for direction in range(1,5):
        if map_tensor[direction][vehicle_row][vehicle_column]:
            directions.append(direction)
    return directions
















