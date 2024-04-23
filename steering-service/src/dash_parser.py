class DashParser:
    def __init__(self):
        pass

    def build(self, nodes, uri, request):
        message = {}
        message['VERSION'] = 1
        message['TTL'] = 10
        message['RELOAD-URI'] = f'{uri}{request.path}'

        if nodes:
            message['PATHWAY-CLONES'] = self.pathway_clones(nodes)
        
        message["PATHWAY-PRIORITY"] = [f'edge-{node.id}' for node in nodes] + ['cdn']

        return message


    def pathway_clones(self, nodes):
        
        clones = []
        
        for node in nodes:
            clone = {
                'BASE-ID': 'cloud',
                'ID': f'edge-{node.id}',
                'URI-REPLACEMENT': {
                    'HOST': node.host,
                    'PARAMS': {}
                }
            }
            
            clones.append(clone)
            
        return clones
