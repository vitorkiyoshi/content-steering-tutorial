#!/usr/bin/python3
# -*- coding: utf-8 -*-


########################################################################
# IMPORTS                                                             ##
########################################################################
import logging
import docker
import os

from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin

from builder import Builder
from monitoring import Monitoring


# DEFINES
########################################################################
STEERING_ADDR = '0.0.0.0'
STEERING_PORT = 30500
BASE_URI      = f'http://{STEERING_ADDR}:{STEERING_PORT}'

_builder    = Builder()
_monitoring = Monitoring()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# CLASSES.
class Main:

    def __init__(self):
        """
        """
        self.app = Flask(__name__)
        CORS(self.app)


    
        @self.app.route('/steering/<name>')
        def do_remote_steering(name):
            print("entroi")
            data = _builder.build(
                nodes   = None,
                uri     = BASE_URI,
                request = request
            )
            
            return jsonify(data)


    def run(self):
        self.app.run(host=STEERING_ADDR, port=STEERING_PORT, debug=True)

# END CLASS.


# MAIN
#################################################
if __name__ == '__main__':

    print("entrou1")

    _monitoring.start()

    print("entrou2")

    main = Main()
    main.run()
# EOF
