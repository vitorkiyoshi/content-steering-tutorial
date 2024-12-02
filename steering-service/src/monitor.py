import docker
import threading
import math
from choice_algorithms.epsilon_greedy import EpsilonGreedy
from choice_algorithms.ucb1 import UCB1
import latency.latency_estimator as lat_estimator

# CLASS
class ContainerMonitor:
    def __init__(self):
        self.client = docker.from_env()
        self.container_stats = {}
        self.nodes = []
        self.interval = 2
        self.choice_algorithm = None
        self.last_selected_node = None
        self.latency_average = []


    def start_collecting(self):
        self.collect_stats()

        # Schedule the next collection
        threading.Timer(self.interval, self.start_collecting).start()


    def collect_stats(self):
        for container in self.client.containers.list(all=True):
            if container.status != 'running':
                if container.name in self.container_stats:
                    del self.container_stats[container.name]
                continue
            try:
                stats = container.stats(stream=False)
                networks = container.attrs['NetworkSettings']['Networks']
                ip_address = networks.get('video-streaming_default', {}).get('IPAddress', 'N/A')
                
                latitude = None
                longitude = None 
                for env_var in container.attrs['Config']['Env']:
                    if env_var.startswith("LATITUDE="):
                        latitude = float(env_var.split("=", 1)[1])
                    elif env_var.startswith("LONGITUDE="):
                        longitude = float(env_var.split("=", 1)[1])
                
                prev_stats = self.container_stats.get(container.name, [{}])[-1]

                container_stats = {
                    'cpu_usage': stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100,
                    'mem_usage': stats['memory_stats']['usage'] / stats['memory_stats']['limit'] * 100,
                    'rx_bytes': stats['networks']['eth0']['rx_bytes'],
                    'tx_bytes': stats['networks']['eth0']['tx_bytes'],
                    'rate_rx_bytes': (stats['networks']['eth0']['rx_bytes'] - prev_stats.get('rx_bytes', 0)),
                    'rate_tx_bytes': (stats['networks']['eth0']['tx_bytes'] - prev_stats.get('tx_bytes', 0)),
                    'ip_address': ip_address,  # IP address of the container
                    'latitude': latitude,
                    'longitude': longitude
                }

                if container.name not in self.container_stats:
                    self.container_stats[container.name] = []
    
                self.container_stats[container.name].append(container_stats)
    
                # Keep only the last 10 metrics for each container
                self.container_stats[container.name] = self.container_stats[container.name][-10:]
                
            except Exception as e:
                print(f"Failed to get stats for container {container.name}: {str(e)}")

            # self.print_stats()


    def getNodes(self):
        if not self.nodes:
            return [(name, stat[-1]['ip_address']) for name, stat in self.container_stats.items()]
        
        return self.nodes

    def print_stats(self):
        for name, stats_list in self.container_stats.items():
            print(f"Stats for {name}:")
            if stats_list:
                stats = stats_list[-1]
                print(f"  CPU Usage: {stats['cpu_usage']}")
                print(f"  Memory Usage: {stats['mem_usage']}")
                print(f"  Network Input: {stats['rx_bytes']}")
                print(f"  Network Output: {stats['tx_bytes']}")
                print(f"  Rate Network Input: {stats['rate_rx_bytes']}")
                print(f"  Rate Network Output: {stats['rate_tx_bytes']}")
                print(f"  Metrics size: {len(stats_list)}")
                print(f"  IP address: {stats['ip_address']}")
    
    def estimate_latency(self, lat, lon, selected_node):
            selected_node_lat = self.container_stats[selected_node][-1]['latitude']
            selected_node_lon = self.container_stats[selected_node][-1]['longitude']
            # Estimante lat_distance
            response = lat_estimator.estimate_latency(lat, lon, selected_node_lat, selected_node_lon)
            return response

    def algorith_boot(self, algorithm):
        # Algorithm boot
        if not self.nodes:
            self.nodes = self.getNodes()

        if self.choice_algorithm is None:
            if algorithm.lower() == 'greedy':
                print("Setting up Greedy algorithm")
                self.choice_algorithm = EpsilonGreedy(0.3, None, None)
                self.choice_algorithm.initialize([name for (name, _) in self.nodes])
            elif algorithm.lower() == 'ucb1':
                print("Setting up UCB1 algorithm")
                self.choice_algorithm = UCB1(None, None)
                self.choice_algorithm.initialize([name for (name, _) in self.nodes])
            else:
                print("Not valid algorithm provided, setting up to random choice")
                self.choice_algorithm = EpsilonGreedy(0.3, None, None)
                self.choice_algorithm.initialize([name for (name, _) in self.nodes])

    def sort_nodes(self):
            
        # Choose a server
        self.nodes = self.choice_algorithm.select_arm(self.nodes)
        selected_node = self.nodes[0]
        return selected_node[0]
    
    def update(self, selected_node, rt):

        self.choice_algorithm.update(selected_node, rt)
        print(f"[LOG] Counts: {self.choice_algorithm.counts}")
        print(f"[LOG] Values: {self.choice_algorithm.values}")


# END CLASS.


# MAIN
if __name__ == '__main__':

    main = ContainerMonitor()
    main.start_collecting()
# EOF