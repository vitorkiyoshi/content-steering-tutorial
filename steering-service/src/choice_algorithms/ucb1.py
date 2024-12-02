import math

NODE_NAME = 0

class UCB1():
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
    
        ucb_values = dict.fromkeys(list(map(lambda node: node[NODE_NAME], nodes)), 0.0)
        total_counts = sum(self.counts.values())
        
        for node in nodes:
            bonus = math.sqrt((2 * math.log(total_counts)) / float(self.counts[node[NODE_NAME]]))
            ucb_values[node[NODE_NAME]] = self.values[node[NODE_NAME]] + bonus
        return sorted(nodes, key=lambda node: ucb_values[node[NODE_NAME]], reverse=True)
    
    # Choose to update chosen arm and reward
    def update(self, chosen_arm_name, latency):
        # Converts latency in reward
        reward = 1000 / latency
        self.counts[chosen_arm_name] = self.counts[chosen_arm_name] + 1
        n = self.counts[chosen_arm_name]
        
        # Update average/mean value/reward for chosen arm
        value = self.values[chosen_arm_name]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm_name] = new_value
        return