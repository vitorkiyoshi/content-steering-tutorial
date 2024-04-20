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
from kubernetes import client
from flask_cors import CORS, cross_origin

from builder import Builder



# DEFINES
########################################################################
STEERING_ADDR = 'steering-service'
STEERING_PORT = int(os.environ.get('STEERING_PORT'))
CONTENT_TYPE_LATEST = os.environ.get('CONTENT_TYPE_LATEST')

_builder = Builder()

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


        self.client = docker.from_env()

        base_uri = f'http://{STEERING_ADDR}:{STEERING_PORT}'


        @self.app.route('/steering/<name>')
        def do_remote_steering(name):

            data = _builder.build(
                nodes = None, 
                uri   = f'{base_uri}{request.path}'
            )
            
            return jsonify(data)


    def run(self):
        self.app.run(host=STEERING_ADDR, port=STEERING_PORT, debug=True)

# END CLASS.


# MAIN
#################################################
if __name__ == '__main__':

    main = Main()
    main.run()
# EOF
