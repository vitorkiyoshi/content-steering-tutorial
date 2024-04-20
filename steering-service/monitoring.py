import os
import json
import time
import queue
import logging
import datetime
import subprocess
import collections
import docker
import Constants

from sql_service import Sqlite3ContainerMonitor, Sqlite3UserMonitor

from flask import request


ContainerReport = collections.namedtuple('ContainerReport', ['container',
                                                             'status', 'cpu',
                                                             'mem', 'size',
                                                             'delta_memory',
                                                             'pre_checkpoint',
                                                             'time_checkpoint',
                                                             'time_xdelta'])



class ContainerMonitor(object):

    UNITS = {'MiB': 1024**2/1000**2,
             'GiB': 1024**3/1000**2,
             'MB': 1,
             'GB':1000}


    def __init__(self, servers, delay=5*60, **kwargs):
        self.client = docker.from_env()
        self.delay = delay

        self.containers = servers

        self.dbContainer = Sqlite3ContainerMonitor()
        self.dbContainer.create()

        self.dbUser = Sqlite3UserMonitor()
        self.dbUser.create()


        self.users = []
        self.containers = []
        self.servers = []


    def measure_container_basic_stat(self, name):
        cmd_prefix = \
            'docker stats --no-stream --format "{{.CPUPerc}}    {{.MemUsage}}" '
        out = subprocess.check_output(cmd_prefix + name, shell=True).decode()
        logging.debug('command {} return {}'.format(cmd_prefix+name, out))
        stats = out.split("\n")[0].split("    ")
        cpu = float(stats[0].rstrip('%'))
        mem_str = stats[1].split(' / ')[0]
        mem_unit = mem_str[-3:]
        mem = float(mem_str[:-3])*ContainerMonitor.UNITS[mem_unit]

        return (cpu,mem)


    def measure_container_size(self, name, image):
        query_size = 'docker images ' + image + ' --format "{{.Size}}"'
        out = subprocess.check_output(query_size, shell=True).replace(' ', '').rstrip("\n")
        logging.debug('command {} return {}'.format(query_size, out))
        val = float(out[:-2])
        unit = out[-2:]
        return val*ContainerMonitor.UNITS[unit]

    def get_container_size(self, container_id):
        cmd_prefix = 'docker inspect -s ' + container_id + ' --format "{{.SizeRw}}" ' 
        total_size = subprocess.check_output(cmd_prefix, shell=True).decode()

        return int(total_size)


    def container_status(self, name):
        containers = self.client.containers.list(filters={'name':name})
        if len(containers) != 0:
            return containers[0].status
        else:
            logging.warn("Canot find container")
            return None


    def measureContainers(self):
        for service in self.containers:
            container = service['name']
            status = self.container_status(container)

            if status is None:
                return
            try:
                cpu, mem = self.measure_container_basic_stat(container)
                size = self.get_container_size(container)

                print(size)
            except ValueError:
                logging.warn("Cannot check container stats")
                return
            except subprocess.CalledProcessError:
                logging.warn("Cannot check container stats")
                return

            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            self.database.insert_container_metrics(ts, container, status, cpu, mem, size);

            report = ContainerReport(container, status, cpu, mem, size,
                                        0, # s.delta_memory,
                                        0, # s.pre_checkpoint,
                                        0, # s.time_checkpoint,
                                        0) # s.time_xdelta)

            self.container_report(report)


    def measureUsersQoE(self):
        total_qoe = 0

        for user in self.users:
            total_qoe += user

            params = {
                'uid'    : request.args.get('userName', default='', type=str),
                'video'  : request.args.get('video', default='', type=str),
                'QoE'    : request.args.get('QoE', default=0.0, type=float),
                'thr'    : request.args.get('throughput', default=0.0, type=float),
                'segid'  : request.args.get('segid', default=0, type=int),
                'btrid'  : request.args.get('btrid', default=0, type=int),
                'btrmx'  : request.args.get('btrmax', default=0, type=int),
            }
            
            user  = params['uid']
            video = params['video']
            qoe   = params['QoE']
            thr   = params['thr']
            segid = params['segid']
            btrid = params['btrid']
            btrmx = params['btrmx']
            bt    = params['bt']
            rssi  = params['rssi']
            
            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            self.database.insert_container_metrics(ts, user, video, qoe, thr, segid, btrid, btrmx, bt, rssi)

            report = ContainerReport(user, video, qoe, thr, segid, btrid, btrmx,
                                        0, # s.delta_memory,
                                        0, # s.pre_checkpoint,
                                        0, # s.time_checkpoint,
                                        0) # s.time_xdelta)

            self.container_report(report)

        return total_qoe
    

    def measureServers(self):
        for service in self.servers:
            container = service['name']
            status = self.container_status(container)

            if status is None:
                return
            try:
                cpu, mem = self.measure_container_basic_stat(container)
                size = self.get_container_size(container)

                print(size)
            except ValueError:
                logging.warn("Cannot check container stats")
                return
            except subprocess.CalledProcessError:
                logging.warn("Cannot check container stats")
                return

            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            self.database.insert_container_metrics(ts, container, status, cpu, mem, size);

            report = ContainerReport(container, status, cpu, mem, size,
                                        0, # s.delta_memory,
                                        0, # s.pre_checkpoint,
                                        0, # s.time_checkpoint,
                                        0) # s.time_xdelta)

            self.container_report(report)

    def measureNetwork(self):
        raise NotImplemented

    def report_namedtuple(self, report, topic_prefix):
        topic = '{}/{}'.format(topic_prefix,
                               'cacheserver')
        payload = json.dumps(report)
        logging.info('Publish to topic {}: {}'.format(topic, payload))
        # self.publish(topic, payload)


    def network_report(self, report):
        self.report_namedtuple(report, Constants.MONITOR_EDGE)


    def server_report(self, report):
        self.report_namedtuple(report, Constants.MONITOR_SERVER)


    def container_report(self, report):
        self.report_namedtuple(report, Constants.MONITOR_CONTAINER)


    def user_report(self):
        qoe_ = 0


    def main_monitor(self):
        self.last_list = []

        while True:
            self.user_report()
            
            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            containers, servers, qoes = {}, {}, {}

            self.database.insert_metrics(ts, containers, servers, qoes)

            time.sleep(2)
