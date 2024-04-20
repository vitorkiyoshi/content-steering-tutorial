import os
import subprocess
import sqlite3
from utilities import get_hostname
import logging
from subprocess import check_output



class Sqlite3Service(object):
    def __init__(self, **kwargs):
        self.table = kwargs.get('table', 'table')

        self.database = kwargs.get('database', 'database')
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

        print("Database {} - table {}".format(self.database, self.table))


    def execute_edit_cmd(self, cmd):
        #logging.debug(cmd)
        self.cursor.execute(cmd)
        self.conn.commit()


    def execute_read_cmd(self, cmd):
        #logging.debug(cmd)
        self.cursor.execute(cmd)
        data = self.cursor.fetchall()
        return data


    def create_table(self, columns):
        cmd = "CREATE TABLE {} ({})".format(self.table, columns)
        self.execute_edit_cmd(cmd)


    def insert_data(self, values):
        cmd = "INSERT INTO {} VALUES ({})".format(self.table, values)
        self.execute_edit_cmd(cmd)


class Sqlite3NetworkMonitor(Sqlite3Service):
    def __init__(self, **kwargs):
        table = 'networkMonitor'

        database = kwargs.get('database', '{}network.db'.format(get_hostname()))
        super(Sqlite3NetworkMonitor, self).__init__(database=database, table=table)

    def create(self):
        if os.path.isfile(self.database):
            check_output(['savelog', '-ntl', self.database])
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        columns = 'timestamp text, source_dest text, latency real, bandwidth real'
        self.create_table(columns)

    def insert_net_metrics(self, ts, source_ip, dest_ip, latency, bandwidth):
        write_sql = "'{0}', '{1}_{2}', {3}, {4}".format(ts, source_ip, dest_ip,
            latency, bandwidth)
        self.insert_data(write_sql)



class Sqlite3ContainerMonitor(Sqlite3Service):
    def __init__(self, **kwargs):
        table = 'containerMonitor'

        database = kwargs.get('database', '{}-container.db'.format(get_hostname()))
        super(Sqlite3ContainerMonitor, self).__init__(database=database, table=table)

    def create(self):
        if os.path.isfile(self.database):
            subprocess.check_output(['savelog', 'ntl', self.database])
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        columns = ', '.join(['timestamp text',
                             'container_name',
                             'status',
                             'cpu',
                             'memory',
                             'size'])
        self.create_table(columns)

    def insert_container_metrics(self, ts, name, status, cpu, memory, size):
        write_sql = "'{0}', '{1}', '{2}', {3}, {4}, {5}".format(ts, name,
                                                                status, cpu,
                                                                memory, size)
        self.insert_data(write_sql)

class Sqlite3UserMonitor(Sqlite3Service):
    def __init__(self, **kwargs):
        table = 'usersMonitor'

        database = kwargs.get('database', '{}-users.db'.format(get_hostname()))
        super(Sqlite3UserMonitor, self).__init__(database=database, table=table)

    def create(self):
        if os.path.isfile(self.database):
            subprocess.check_output(['savelog', 'ntl', self.database])
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()
        columns = ', '.join(['timestamp text',
                             'user',
                             'throughput',
                             'btrid',
                             'btrmax',
                             'qoe'])
        self.create_table(columns)

    def insert_container_metrics(self, ts, name, throughput, btrid, btrmax, qoe):
        write_sql = "'{0}', '{1}', '{2}', {3}, {4}, {5}".format(ts, name,
                                                                throughput, btrid,
                                                                btrmax, qoe)
        self.insert_data(write_sql)


class Sqlite3ServerMonitor(Sqlite3Service):
    def __init__(self, **kwargs):
        table = 'serverMonitor'

        database = kwargs.get('database', '{}server.db'.format(get_hostname()))
        super(Sqlite3ServerMonitor, self).__init__(database=database, table=table)