from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

from dash_parser import DashParser
from monitor import ContainerMonitor


# DEFINES
STEERING_ADDR = '0.0.0.0'
STEERING_PORT = 30500
BASE_URI      = f'http://{STEERING_ADDR}:{STEERING_PORT}'


# Create instances of the parsers and the container monitor
dash_parser  = DashParser()
monitor = ContainerMonitor()


class Main:

    def __init__(self):
        """
        """
        self.app = Flask(__name__)
        CORS(self.app)

        @self.app.route('/')
        def do_remote_steering(name):
            trg = request.args.get('_DASH_pathway', default='', type=str)
            thr = request.args.get('_DASH_throughput', default=0.0, type=float)
            
            nodes = monitor.getNodes()

            data = dash_parser.build(
                target  = trg,
                nodes   = nodes,
                uri     = BASE_URI,
                request = request
            )
            
            return jsonify(data)


    def run(self):
        self.app.run(host=STEERING_ADDR, port=STEERING_PORT, debug=True)

# END CLASS.


# MAIN
if __name__ == '__main__':

    monitor.start_collecting()

    main = Main()
    main.run()
# EOF
