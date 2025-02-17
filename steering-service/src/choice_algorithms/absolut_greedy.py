import math

NODE_NAME = 0

class AbsolutGreedy():
    def __init__(self, counts, values):
        self.counts = counts # Count represent counts of pulls for each arm. For multiple arms, this will be a map with key=arm_name and value=count of pulls
        self.values = values # Value represent average reward for specific arm. For multiple arms, this will be a map with key=arm_name and value=average reward
        return

    # Initialise arms with given names
    def initialize(self, arms_names : list):
        self.counts = dict.fromkeys(arms_names, 0)
        self.values = dict.fromkeys(arms_names, 0.0)
        return
    
    # UCB arm sorting based on max of UCB reward of each arm
    def select_arm(self, nodes):
        for node in nodes:
            if self.counts[node[NODE_NAME]] == 0:
                # Sort the list of servers based on times that they have been picked up
                return sorted(nodes, key=lambda node: self.counts[node[NODE_NAME]])
        
        print("[LOG]")
        print("[LOG]")
        print("[LOG]")
        print(sorted(nodes, key=lambda node: self.values[node[NODE_NAME]]))
        return sorted(nodes, key=lambda node: self.values[node[NODE_NAME]])
    
    # Choose to update chosen arm and reward
    def update(self, chosen_arm_name, latency):
        print("aloo")
        if self.counts[chosen_arm_name] == 0:
            self.values[chosen_arm_name] = latency
        self.counts[chosen_arm_name] = self.counts[chosen_arm_name] +1
        print(self.counts)
        print(self.values)
        return