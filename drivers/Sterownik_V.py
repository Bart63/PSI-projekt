from .Driver import Driver
from simulation.utils.Direction import Direction
from simulation.api import API
from collections import deque
import math
import random

class Sterownik_V(Driver):
    def __init__(self):
        super().__init__()
        self.current_direction = None
        self.last_directions = deque(maxlen=7)
    
    def on_simulation_start(self):
        self.main_vehicle_pos = API.main_vehicle_pos
        self.main_vehicle_direction = API.main_vehicle_direction
        self.target_crossroad_pos = API.target_crossroad_pos
        self.final_destination_pos = API.final_destination_pos
        all_points = API.destinations_pos_list 

        self.path_order = self.sort_points_with_centroid_bfs(all_points, self.final_destination_pos)    
        self.current_direction = self.decide_direction(self.main_vehicle_pos, self.path_order[0], self.main_vehicle_direction)


    def create_adjacency_matrix(self, points):
        num_points = len(points)
        matrix = [[math.nan for _ in range(num_points)] for _ in range(num_points)]
        for i in range(num_points):
            for j in range(num_points):
                if i != j:
                    matrix[i][j] = self.manhattan_distance(points[i], points[j])
        return matrix


    def manhattan_distance(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    

    def find_shortest_path_bfs(self, points, start):
        adj_matrix = self.create_adjacency_matrix(points)
        num_points = len(points)
        shortest_path_indices = None
        shortest_length = math.inf
        queue = deque([(start, 0, [start], [])]) 
        while queue:
            city, length, path, path_distances = queue.popleft()
            if len(path) == num_points and not math.isnan(adj_matrix[city][start]):
                total_distance = length + adj_matrix[city][start]
                if total_distance < shortest_length:
                    shortest_path_indices = path
                    shortest_length = total_distance
            for next_city in range(num_points):
                if next_city not in path and not math.isnan(adj_matrix[city][next_city]):
                    new_distance = adj_matrix[city][next_city]
                    queue.append((next_city, length + new_distance, path + [next_city], path_distances + [new_distance]))
        shortest_path_coordinates = [points[i] for i in shortest_path_indices] if shortest_path_indices else []
        return shortest_path_coordinates
    

    def compute_centroid(self, points): # oblicza centroid / wyznacza reprezentanta
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        centroid = (sum(x_coords) / len(points), sum(y_coords) / len(points))
        return centroid


    def closest_points(self, coordinates):  # grupuje punkty na podstawie ich wzajemnej odległości
        clusters = []
        ungrouped = coordinates.copy()
        while ungrouped:
            current_city = ungrouped.pop(0) # punkt główny nowego klastra
            distances = [(city, self.manhattan_distance(current_city, city)) for city in ungrouped] # obliczenie odległości od punktu głównego
            distances.sort(key=lambda x: x[1])  # sortowanie punktów według odległości od punktu głównego
            cluster = [current_city]
            for i in range(min(7, len(distances))): 
                cluster.append(distances[i][0]) # dodawanie do klastra max 7 najbliższych punktów
                ungrouped.remove(distances[i][0])   # usunięcie z listy do zakwalfikowania
            clusters.append(cluster)
        return clusters
    

    def sort_clusters_by_bfs(self, clusters, centroids, start_centroid):
        start_index = centroids.index(start_centroid)
        sorted_centroids = self.find_shortest_path_bfs(centroids, start_index)  # najkrótsza ścieżka między centroidami
        sorted_clusters = [clusters[centroids.index(centroid)] for centroid in sorted_centroids]    # sortowanie klastrów według kolejności centroidów
        return sorted_clusters
    

    def sort_points_with_centroid_bfs(self, points, start_centroid):
        clusters = self.closest_points(points)
        centroids = [self.compute_centroid(cluster) for cluster in clusters]
        
       
        if len(clusters) == 1: # zwróć jeśli jeden klaster
            start_index = clusters[0].index(min(clusters[0], key=lambda x: x[0]))
            return self.find_shortest_path_bfs(clusters[0], start_index)
        
        
        if start_centroid not in centroids:
            start_centroid = min(centroids, key=lambda x: x[0])
        sorted_clusters = self.sort_clusters_by_bfs(clusters, centroids, start_centroid)
        sorted_city_list = []
        for cluster in sorted_clusters:
            start_index = cluster.index(min(cluster, key=lambda x: x[0]))
            sorted_cluster = self.find_shortest_path_bfs(cluster, start_index)
            sorted_city_list.extend(sorted_cluster)
        return sorted_city_list
  

    def decide_direction(self, vehicle_pos, target_pos, current_direction):
        dx = target_pos[0] - vehicle_pos[0]
        dy = target_pos[1] - vehicle_pos[1]

        direction_weights = {
            Direction.RIGHT: dx**2 if dx > 0 else 0,
            Direction.LEFT: (-dx)**2 if dx < 0 else 0,
            Direction.DOWN: dy**2 if dy > 0 else 0,
            Direction.UP: (-dy)**2 if dy < 0 else 0
        }

        if len(self.last_directions) >= random.randint(3,4):
            last_three = list(self.last_directions)[-3:]
            
            if last_three in [[Direction.UP, Direction.DOWN, Direction.UP], 
                            [Direction.DOWN, Direction.UP, Direction.DOWN]]:
                
                direction_weights[Direction.UP] /= 10
                direction_weights[Direction.DOWN] /= 10
                        
            elif last_three in [[Direction.LEFT, Direction.RIGHT, Direction.LEFT], 
                            [Direction.RIGHT, Direction.LEFT, Direction.RIGHT]]:
                
                direction_weights[Direction.LEFT] /= 10
                direction_weights[Direction.RIGHT] /= 10

        directions = list(direction_weights.keys())
        weights = list(direction_weights.values())

        if sum(weights) > 0:
            next_direction = random.choices(directions, weights=weights, k=1)[0]
        else:
            next_direction = current_direction  

        self.last_directions.append(next_direction)
        return next_direction


    def on_tick(self):
        self.main_vehicle_pos = API.main_vehicle_pos # Główna pozycja pojazdu na mapie
        self.main_vehicle_direction = API.main_vehicle_direction # Aktualny kierunek głównego pojazdu
        self.target_crossroad_pos = API.target_crossroad_pos # Położenie docelowego skrzyżowania
        
        for dest in self.path_order:
            if abs(self.main_vehicle_pos[0] - dest[0]) < 0.1 and abs(self.main_vehicle_pos[1] - dest[1]) < 0.1: # warunek usuwający z listy osiągnięty punkt
                self.path_order.remove(dest)
                break  # Przerywamy pętlę po usunięciu punktu
        if not self.path_order:
            self.path_order.append(self.final_destination_pos)
         

    def on_road_start(self): 
        pass
        

    def on_road_end(self):       
        self.current_direction = self.decide_direction(self.main_vehicle_pos, self.path_order[0], self.main_vehicle_direction)


    def get_direction_decisions(self) -> Direction:
        return self.current_direction


    def remove_direction_decision(self) -> None:
        self.current_direction = None
   