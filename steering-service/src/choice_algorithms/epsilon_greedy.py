import random

NODE_NAME = 0

class EpsilonGreedy():
    def __init__(self, epsilon, counts, values):
        self.epsilon = epsilon
        self.counts = counts # Count represent counts of pulls for each arm. For multiple arms, this will be a map with key=arm_name and value=count of pulls
        self.values = values # Value represent average reward for specific arm. For multiple arms, this will be a map with key=arm_name and value=average reward
        return
    
    # Initialise arms with given names
    def initialize(self, arms_names : list):
        self.counts = dict.fromkeys(arms_names, 0)
        self.values = dict.fromkeys(arms_names, 0.0)
        return
    
    # Epsilon greedy arm selection
    # nodes is the list of nodes actives
    def select_arm(self, nodes):
        # If prob is not in epsilon, do exploitation of best arm so far
        if random.random() > self.epsilon:
            # Sort the list of servers based on values (less, better)
            return sorted(nodes, key=lambda node: self.values[node[NODE_NAME]])
        # If prob falls in epsilon range, do exploration
        else:
            # Do a shuffle and return list of nodes
            random.shuffle(nodes)
            return nodes
    
    # Choose to update chosen arm and punishment
    def update(self, chosen_arm_name, punishment):
        # update counts pulled for chosen arm
        self.counts[chosen_arm_name] = self.counts[chosen_arm_name] + 1
        n = self.counts[chosen_arm_name]
        
        # Update average/mean value/punishment for chosen arm
        value = self.values[chosen_arm_name]
        new_value = ((n-1)/float(n)) * value + (1 / float(n)) * punishment
        self.values[chosen_arm_name] = new_value
        return