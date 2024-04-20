#!/usr/bin/python3
# -*- coding: utf-8 -*-


########################################################################
# IMPORTS                                                             ##
########################################################################
import randomname
import logging
import json
import os

from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from kubernetes import client
from flask_cors import CORS, cross_origin
from prometheus_client import generate_latest
from timeit import default_timer as timer

from builder import Builder



# DEFINES
########################################################################
STEERING_ADDR = 'localhost'
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

        base_uri = f'http://{STEERING_ADDR}:{STEERING_PORT}'


        @self.app.route('/steering/<name>')
        def do_remote_steering(name):                       
            vid = request.args.get('video', default='', type=str)

            print(request.data)
            
            uri = f'{base_uri}{request.path}?video={vid}'


            data = _builder.build(None, uri)
            
            return jsonify(data)


        @self.app.route('/collect/qoe', methods=['GET', 'OPTIONS'])
        def do_qoe_info():
            params = {
                'uid'    : request.args.get('userName', default='*', type=str),
                'video'  : request.args.get('video', default='*', type=str),
                'QoE'    : request.args.get('QoE', default=0.0, type=float),
                'thr'    : request.args.get('throughput', default=0.0, type=float),
                'segid'  : request.args.get('segid', default=0, type=int),
                'btrid'  : request.args.get('btrid', default=0, type=int),
                'btrmx' : request.args.get('btrmax', default=30000, type=int),
            }
            
            user  = params['uid']
            video = params['video']
            qoe   = params['QoE']
            thr   = params['thr']
            segid = params['segid']
            btrid = params['btrid']
            btrmx = params['btrmx']

            print(user, video, segid, thr, qoe, btrid, btrmx)
            
            return Response(
                "ok", 
                status=200,
                headers={
                    'Access-Control-Allow-Origin': '*',
                }
            )

    def run(self):
        self.app.run(host=STEERING_ADDR, port=STEERING_PORT, debug=True)

# END CLASS.


# MAIN
#################################################
if __name__ == '__main__':

    main = Main()
    main.run()
# EOF
