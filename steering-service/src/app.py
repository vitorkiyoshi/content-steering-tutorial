from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin

import argparse

from dash_parser import DashParser
from monitor import ContainerMonitor


# DEFINES
STEERING_ADDR = 'steering-service'
STEERING_PORT = 30500
BASE_URI      = f'https://{STEERING_ADDR}:{STEERING_PORT}'


# Create instances of the parsers and the container monitor
dash_parser  = DashParser()
monitor = ContainerMonitor()


class Main:
    def __init__(self):
        """
        """
        self.app = Flask(__name__)
        CORS(self.app)

        @self.app.route('/<name>', methods=['GET'])
        @cross_origin()
        def do_remote_steering(name):
            tar = request.args.get('_DASH_pathway', default='', type=str)
            thr = request.args.get('_DASH_throughput', default=0.0, type=float)

            nodes = monitor.getNodes()

            data = dash_parser.build(
                target  = tar,
                nodes   = nodes,
                uri     = BASE_URI,
                request = request
            )
            
            # print(data)
            return jsonify(data), 200
        
        @self.app.route('/estimate-latency', methods=['POST'])
        def estimate_latency():
            """
            Endpoint para calcular a estimativa de latência.
            """
            try:
                # Obtém os dados da requisição
                data = request.get_json()
                longitude = data['longitude']
                latitude = data['latitude']
                selected_node = data['selected_node']

                # Calcula a latência estimada
                latency = monitor.estimate_latency(latitude, longitude, selected_node)

                # Retorna a estimativa como resposta JSON
                return jsonify({
                    'estimated_latency_ms': latency
                }), 200

            except Exception as e:
                return jsonify({'error': str(e)}), 400
        

        @self.app.route('/sort_nodes', methods=['POST'])
        def sort_nodes():
            m = {}
            m["status"] = "ok"
            m["selected"] = monitor.sort_nodes()
            return jsonify(m), 200
        
        @self.app.route('/update', methods=['POST'])
        def update():
            data = request.get_json()
            selected_node = data['selected_node']
            rt = data['rt']
            monitor.update(selected_node, rt)
            return jsonify(), 200

    def run(self):
        ssl_context = ('steering-service/certs/steering-service.pem', 'steering-service/certs/steering-service-key.pem')
        self.app.run(host=STEERING_ADDR, port=STEERING_PORT, debug=True, ssl_context=ssl_context)

# END CLASS.


# MAIN
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Configuração do servidor Flask")
    parser.add_argument('algorithm', type=str, help="Algoritmo de escolha a ser aplicado")
    args = parser.parse_args()

    # Configurar o Flask com base no argumento
    monitor.start_collecting()
    monitor.algorith_boot(args.algorithm)

    main = Main()
    main.run()
# EOF
