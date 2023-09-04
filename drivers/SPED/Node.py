from drivers.SPED.utils import *
import numpy as np
class Node:
    def __init__(self, map_tensor, parent, prior, previous_dir, predictor, state_id=0):
        self.state_id = state_id
        self.map_tensor = map_tensor
        self.parent = parent
        self.prior = prior
        self.num_visits = 1
        self.initial_destinations_left = np.sum(self.map_tensor[[13, 14, 15, 16]] == 1)
        pi, self.ticks_to_finish, self.ticks_from_last_xroad = predictor.predict(map_tensor)
        legal_directions = get_available_directions(self.map_tensor)
        policy = []
        for direction in legal_directions:
            policy.append((direction, pi[direction-1]))
        sum_of_priors = sum(x[1] for x in policy)
        policy = [(x[0], x[1] / sum_of_priors) for x in policy]
        self.pi = sorted(policy, key=lambda x: x[1])
        self.total_reward = self.ticks_to_finish
        self.is_fully_expanded = False
        self.add_node_picked = True
        self.last_added_node = None
        self.is_terminal = self.is_terminal()
        self.children = {}
        self.destinations_left = np.sum(self.map_tensor[[13, 14, 15, 16]] == 1)
        if self.is_terminal:
            self.destinations_left = -1
            self.initial_destinations_left = -1

    def is_terminal(self):
        if np.all(self.map_tensor[[13, 14, 15, 16]] == 0) and np.any((self.map_tensor[17] == 1) & (self.map_tensor[18] == 1)):
            self.ticks_to_finish = 0
            return True
        else:
            return False

    def get_distribution(self):
        distribution = [0]*4
        for direction, child in self.children.items():
            distribution[direction-1] = child.num_visits
        distribution = [x+1 for x in distribution]
        distribution = [x/sum(distribution) for x in distribution]
        return distribution





