def deep_copy(list):
        list_copy = []
        for element in list:
            list_copy.append((element[0], element[1]))
        return list_copy

def simple_copy(list):
        list_copy = []
        for element in list:
            list_copy.append(element)
        return list_copy


def calculate_manhattan_distance(source, destination):
        return abs(source[0] - destination[0]) + abs(source[1] - destination[1])