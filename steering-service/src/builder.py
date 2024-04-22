class Builder:
    def __init__(self):
        self.build_obj = None


    def build(self, nodes, uri, request):
        message = {}
        message['VERSION'] = 1
        message['TTL'] = 10
        message['RELOAD-URI'] = f'{uri}{request.path}'

        if nodes:
            message['PATHWAY-CLONES'] = self.pathway_clones(nodes)
        
        message["PATHWAY-PRIORITY"] = ['cdn']

        return message


    def pathway_clones(self, nodes):
        
        clones = []
        
        for node in nodes:
            clone = {
                'BASE-ID': 'edge1',
                'ID': 'edge1-clone',
                'URI-REPLACEMENT': {
                    'HOST': 'http://127.0.0.1:30001',
                    'PARAMS': {
                        'ap1': '3.71',
                        'ap2': '5'
                    }
                }
            }
            
            clones.append(clone)
            
        return clones
