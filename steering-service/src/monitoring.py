import yaml
import docker


# CLASSES
###############################################################################
class Monitoring:

    def __init__(self):
        self.client = docker.from_env()

    def collect_container_metrics(self):
        for container in self.client.containers.list():
            stats = container.stats(stream=False)

            # Extracting required fields
            container_id    = stats['id']
            name            = stats['name']
            cpu_percentage  = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
            mem_usage_limit = stats['memory_stats']['usage'] / stats['memory_stats']['limit']
            mem_percentage  = stats['memory_stats']['usage'] / stats['memory_stats']['limit'] * 100
            net_input       = stats['networks']['eth0']['rx_bytes']
            net_output      = stats['networks']['eth0']['tx_bytes']
            block_input     = stats['blkio_stats']['io_service_bytes_recursive'][0]['value']
            block_output    = stats['blkio_stats']['io_service_bytes_recursive'][1]['value']
            pids            = stats['pids_stats']['current']
            
            print(['NAME', 'CPU %', 'MEM USAGE / LIMIT', 'MEM %', 'NET I/O', 'BLOCK I/O', 'PIDS'])
            print([name, cpu_percentage, mem_usage_limit, mem_percentage, net_input, net_output, block_input, block_output, pids])

        return None

    def main_monitoring(self):
        while True:
            stats = self.collect_container_metrics()            

# END CLASS.

# MAIN
#################################################
if __name__ == '__main__':

    main = Monitoring()
    main.main_monitoring()
# EOF