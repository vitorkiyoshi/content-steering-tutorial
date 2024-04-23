import docker
import threading


# CLASS
class ContainerMonitor:
    def __init__(self):
        self.client = docker.from_env()
        self.container_stats = {}
        self.interval = 2  # collect stats every 2 seconds


    def start_collecting(self):
        self.collect_stats()

        # Schedule the next collection
        threading.Timer(self.interval, self.start_collecting).start()


    def collect_stats(self):
        for container in self.client.containers.list():
            try:
                stats = container.stats(stream=False)
                prev_stats = self.container_stats.get(container.name, [{}])[-1]

                container_stats = {
                    'cpu_usage': stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100,
                    'mem_usage': stats['memory_stats']['usage'] / stats['memory_stats']['limit'] * 100,
                    'rx_bytes': stats['networks']['eth0']['rx_bytes'] - prev_stats.get('rx_bytes', 0),
                    'tx_bytes': stats['networks']['eth0']['tx_bytes'] - prev_stats.get('tx_bytes', 0),
                }

                if container.name not in self.container_stats:
                    self.container_stats[container.name] = []
    
                self.container_stats[container.name].append(container_stats)
    
                # Keep only the last 10 metrics for each container
                self.container_stats[container.name] = self.container_stats[container.name][-10:]
                
            except Exception as e:
                print(f"Failed to get stats for container {container.name}: {str(e)}")

            self.print_stats()


    def getNodes(self, metric='cpu_usage'):
        return [(name, stats[metric]) for name, stats_list in self.container_stats.items() for stats in stats_list]


    def print_stats(self):
        for name, stats_list in self.container_stats.items():
            print(f"Stats for {name}:")
            if stats_list:
                stats = stats_list[-1]
                print(f"  CPU Usage: {stats['cpu_usage']}")
                print(f"  Memory Usage: {stats['mem_usage']}")
                print(f"  Network Input: {stats['rx_bytes']}")
                print(f"  Network Output: {stats['tx_bytes']}")
                print(f"  Metrics size: {len(stats_list)}")

# END CLASS.


# MAIN
if __name__ == '__main__':

    main = ContainerMonitor()
    main.start_collecting()
# EOF