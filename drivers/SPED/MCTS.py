from drivers.SPED.Node import Node
from drivers.SPED.utils import *
from drivers.SPED.SPED_mcts_config import CPUCT
class Mcts:
    def __init__(self, starting_map_tensor, last_direction, predictor):
        self.root = Node(starting_map_tensor, None, 0, last_direction, predictor)
        self.min_left = float('inf')
        self.predictor = predictor
        pass

    def print_info(self):
        childs = []
        for move, child in self.root.children.items():
            if self.root.ticks_to_finish == 0:
                t = 1
            else:
                t = self.root.ticks_to_finish
            v = ((child.total_reward / child.num_visits) + child.ticks_from_last_xroad) / t
            childs.append((move, v, child.num_visits, child.prior))
        childs = sorted(childs, key=lambda x: x[2], reverse=True)
        #print(childs)
        print(f'Selecting path which starts with direction {childs[0][0]} visited {childs[0][2]} out of total {self.root.num_visits-1} iterations of MCTS, with prior probability of {childs[0][3]}')

    def execute_round(self):
        node = self.select_node(self.root)
        self.backpropagate(node)


    def select_node(self, node):
        while not (node.is_terminal or node.num_visits == 1):
            if node.is_fully_expanded:
                node = self.get_best_child(node)
            else:
                if node.add_node_picked:
                    newNode = self.expand(node)
                    node = self.get_best_child(node)
                    if newNode == node:
                        node.parent.add_node_picked = True
                        return newNode
                    else:
                        node.parent.add_node_picked = False
                        node.parent.last_added_node = newNode
                else:
                    node = self.get_best_child(node)
                    if node == node.parent.last_added_node:
                        node.parent.add_node_picked = True
                        return node
        return node

    def get_best_child(self, node):
        best_value = float('inf')
        for child in node.children.values():
            if node.ticks_to_finish == 0:
                t = 1
            else:
                t = node.ticks_to_finish
            v = ((child.total_reward / child.num_visits) + child.ticks_from_last_xroad) / t
            h = child.prior
            child_value = v - h * CPUCT * ((node.num_visits ** (1 / 2)) / child.num_visits)
            if child_value < best_value:
                best_value = child_value
                best_node = child
        return best_node

    def expand(self, node):
        direction = node.pi[0][0]
        prior = node.pi[0][1]
        node.pi.pop(0)
        map_tensor = take_action(node.map_tensor, direction)
        new_node = Node(map_tensor=map_tensor, parent=node, prior=prior, previous_dir=direction,
                        predictor=self.predictor, state_id=node.state_id)
        node.children[direction] = new_node
        if not bool(node.pi):
            node.is_fully_expanded = True
        return new_node

    def backpropagate(self, node):
        reward = node.total_reward / node.num_visits
        left = node.destinations_left
        while node is not None:
            if left < node.destinations_left:
                node.destinations_left = left
            node.total_reward += reward
            reward += node.ticks_from_last_xroad
            node.num_visits += 1
            node = node.parent

    def get_best_visit_direction(self, node):
        for direction, child in node.children.items():
            if child.num_visits>best_visits:
                best_visits = child.num_visits
                best_direction = direction
        return best_direction

    def set_next_root(self, to_direction):
        for direction, child in self.root.children.items():
            if direction == to_direction:
                self.root = child
                self.root.parent = None
                return

    def get_directions_list(self):
        node = self.root
        initial_left = self.root.initial_destinations_left
        directions = []
        decisions = []
        visits = []
        while True:
            best_visits = 0
            for direction, child in node.children.items():
                if child.num_visits > best_visits and child.destinations_left < initial_left:
                    best_visits = child.num_visits
                    best_direction = direction
                    best_node = child
            best_decision = [0]*4
            best_decision[direction - 1] = 1
            decisions.append(best_decision)
            node = best_node
            directions.append(best_direction)
            visits.append(best_node.num_visits)
            if node.initial_destinations_left < initial_left:
                return directions, decisions, visits







