from .utils import calculate_manhattan_distance
import heapq

class PathNode:
    all_destinations_number = 0

    def __init__(self, destination: tuple[float, float], parentNode=None) -> None:
        if parentNode is None:
            self.distance_from_start = 0
            self.visited_destinations = (destination,)
            self.visited_distances = [0]
        else:
            self.update_manhattan_distance(destination)
            self.visited_destinations = parentNode.visited_destinations + (destination,)
        self.approximate_distance_to_end()
    
    def update_manhattan_distance(self, next_destination: tuple(float, float)):
        last_destination = self.visited_destinations[-1]
        last_next_distance = calculate_manhattan_distance(last_destination, next_destination)
        self.visited_distances.append(last_next_distance)
        self.distance_from_start += last_next_distance

    def __lt__(self, other):
        selfDist = self.distance_from_start + self.distance_to_end
        otherDist = other.distance_from_start + other.distance_to_end
        return selfDist < otherDist

    def __contains__(self, item: tuple(float, float)):
        for destination in self.visited_destinations:
            if destination[0] != item[0] or destination[1] != item[1]:
                return False
        return True
    
    def path_length(self) -> float:
        return self.distance_from_start

    def heuristic_path_length(self) -> float:
        return self.distance_from_start + self.distance_to_end

    def approximate_distance_to_end(self):
        distance_sum = 0
        min_distance = float('inf')
        for visited_distance in self.visited_distances:
            distance_sum += visited_distance
            if visited_distance < min_distance:
                min_distance = visited_distance
        avg_distance = distance_sum / len(self.visited_distances)

        med_distance = (avg_distance + min_distance) / 2

        destinations_left_to_visit = self.all_destinations_number + 1 - len(self.visited_destinations)
        self.distance_to_end = destinations_left_to_visit * med_distance

    def should_skip_destination(self, child_destination: str) -> bool:
        """Skip node if child destination is already visited and
           it doesn't close the graph

        Args:
            childdestination (str): childdestination that would be added to the path

        Returns:
            bool: True if the destination is already in the Path,
                  False if it can be added to the Path
        """
        if (child_destination in self.visited_destinations) and not \
           (self.visited_all_cities() and child_destination == self.start_destination()):
            return True
        return False

    def discoverBestChildren(self, left_to_visit: list[tuple[float, float]], startdestination: tuple[float, float],
                             childrenList: list,
                             heuristicDistance: float | None = None) -> None:
        for child_destination in left_to_visit:
            if (self.should_skip_destination(child_destination)):
                continue
            child_node = PathNode(child_destination, self)
            heapq.heappush(childrenList, child_node)

    def start_destination(self) -> tuple[float, float]:
        return self.visited_destinations[0]

    def last_destination(self) -> tuple[float, float]:
        return self.visited_destinations[-1]

    def get_visited_destinations(self) -> tuple[tuple[float, float]]:
        return self.visited_destinations

    def last_node(self) -> tuple[tuple[float, float], tuple[float, float]] | None:
        if len(self.visited_destinations) < 2:
            return None
        return (self.visited_destinations[-2], self.visited_destinations[-1])  # type: ignore

    def full_path(self):
        return len(self.visited_destinations) == self.all_destinations_number + 1

    def visited_all_cities(self) -> bool:
        return len(self.visited_destinations) == self.all_destinations_number
