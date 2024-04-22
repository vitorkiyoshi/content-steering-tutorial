import docker
import threading
import collections


ContainerReport = collections.UserList([ "cpu", "mem", "tx", "rx", "net_out" , "net_in"])


# CLASSES
###############################################################################
class Monitoring(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.interval = 2
        self.servers = {}
        self.client = docker.from_env()

    def measureServers(self):
        for container in self.client.containers.list():
            stats = container.stats(stream=False)

            name = stats['name']
            if 'video-streaming' not in name:
                continue

            cpu             = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
            mem_usage_limit = stats['memory_stats']['usage'] / stats['memory_stats']['limit']
            mem_percentage  = stats['memory_stats']['usage'] / stats['memory_stats']['limit'] * 100
            net_input       = stats['networks']['eth0']['rx_bytes']
            net_output      = stats['networks']['eth0']['tx_bytes']

            rx_rate, tx_rate = self.computeRate(name, net_input, net_output)

            instance = [
                cpu,                # cpu
                mem_percentage,     # mem
                tx_rate,            # tx
                rx_rate,            # rx
                net_output,         # net_out
                net_input           # net_in
            ]
        
            self.servers[name].addItem(instance)
        return None
    
    def computeRate(self, name, net_input, net_output):
        prev_tx = self.servers[name].getLastTx()
        prev_rx = self.servers[name].getLastRx()
        cur_tx  = net_output
        cur_rx  = net_input
        
        tx_rate = (cur_tx - prev_tx) / self.interval
        rx_rate = (cur_rx - prev_rx) / self.interval
        
        return rx_rate, tx_rate


    def addList(self, name):
        self.servers[name] = ContainerReport()


    def run(self):
        for container in self.client.containers.list():
            stats = container.stats(stream=False)

            name = stats['name']
            if 'video-streaming' not in name:
                continue

            self.addList(name)

        while True:
            stats = self.measureServers()


class EdgeNode():
    def __init__(self, name, cpu, mem, net_input, net_output):
        self.name = name
        self.cpu = cpu
        self.mem = mem
        self.net_input = net_input
        self.net_output = net_output

        self.prev_net_input = 0
        self.prev_net_output = 0


class ContainerReport():
    def __init__(self, max_size=10):
        self.max_size = max_size
        self.list = []

    def getLastTx(self):
        return self.list[-1][4] if self.list else 0

    def getLastRx(self):
        return self.list[-1][5] if self.list else 0

    def addItem(self, item):
        if len(self.list) >= self.max_size:
            self.list.pop()
        self.list.append(item)

        print(self.list)
    
    def __str__(self):
        return str(self.list)

# END CLASS.



# MAIN
#################################################
if __name__ == '__main__':

    main = Monitoring()
    main.run()
# EOF