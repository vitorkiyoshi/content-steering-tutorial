import yaml

from selector import Selector
from edge_server import EdgeCluster, EdgeServer



# CLASSES
###############################################################################
class Planner:

    """
    """

    def __init__(self, selector, conf="scenario_config.yml"):
        
        self.selector = selector
    
        self.selector.add_cluster('k8s-configs/single-node')
        
        # Add edge servers with specific capacities
        self.selector.add_server_to_cluster(0, 50, 'http://10.0.1.1:30001')
        self.selector.add_server_to_cluster(0, 50, 'http://10.0.1.2:30001')
        self.selector.add_server_to_cluster(0, 50, 'http://10.0.1.3:30001')

        self.obj = {}
        with open(conf, 'r') as f:
            self.obj = yaml.safe_load(f)

        self.aps = self.obj.get('aps', [])
        self.servers = self.obj.get('servers', [])
        self.centre = self.obj.get('centre', [])

        for server in self.servers:
            print(server)
        

    def add_cluster(self, kubeconfig):
        cluster = EdgeCluster(kubeconfig)
        self.clusters.append(cluster)
        

    def add_server_to_cluster(self, cluster_index, capacity, uri, weight=1):
        if cluster_index < len(self.clusters):
            self.clusters[cluster_index].add_server("", capacity, uri, weight)


    def add_server(self, name, capacity, uri, weight=1):
        server = EdgeServer(name, capacity, uri)
        server.weight = weight
        self.servers.append(server)


    """Load AP list from a yaml file.
    Example::

        centre:
        aps:
          - name: "docker1-bts"
            - bssid: '51:3e:aa:49:98:cb'
            - server: "docker1"
          - name: "docker2-bts"
            - bssid: '52:3e:aa:49:98:cb'
            - server: "docker2"
        servers:
          - name: "docker1"
            ip: 10.0.99.10
          - name: "docker2"
            ip: 10.0.99.11
            ...
        end_users:
    """
    def discovery(self, conf):
        self.obj = {}
        with open(conf, 'r') as f:
            self.obj = yaml.safe_load(f)

        self.aps = self.obj.get('aps', [])
        self.servers = self.obj.get('servers', [])
        self.centre = self.obj.get('centre', [])

    def reschedule(self, container, SLO):
        for server in self.servers:
            pass

    def main_planner(self):
        while True:
            pass            

# END CLASS.

