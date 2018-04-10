# -*- coding:utf8 -*-

import ConfigParser
import os
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent
)
from pymysqlreplication.event import RotateEvent
import time

from update_es import data_to_es

CONFIG_FILE = "setting.cfg"
if os.path.exists( os.path.join( os.getcwd(),CONFIG_FILE)):
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)
else:
    CONFIG_FILE = ".dev.setting.cfg"
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)

run_log_file = config.get('run_log','run_log_file')

def pull_bin_log(log_file, time_stamp):

    mysql_settings = {
        'host': config.get('mysql', 'host'), 
        'port': int(config.get('mysql', 'port')),
        'user': config.get('mysql', 'user'),
        'passwd': config.get('mysql', 'passwd')
    }

    stream = BinLogStreamReader(connection_settings = mysql_settings, server_id=10, 
        resume_stream=True,
        only_events=[DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent, RotateEvent],
        log_file=log_file,
        log_pos=4,
        # only_tables=table_filters['db1'],
        skip_to_timestamp= time_stamp+0.1
        )
    next_binlog = log_file
    next_time_stamp = time_stamp

    while True:
        time.sleep(1)
        for binlogevent in stream:
            if isinstance(binlogevent, RotateEvent):
                next_binlog = binlogevent.next_binlog
            else:
                print binlogevent.timestamp, binlogevent
                # for i in  binlogevent.rows:
                #     print i
            # if isinstance(binlogevent, WriteRowsEvent):
            #     new_data = {}
            #     new_data['table_name'] = binlogevent.table
            #     new_data['data'] = binlogevent.rows[0]['values']
            #     update_es_data = data_to_es(new_data)
            #     update_es_data.update_es()

            # if isinstance(binlogevent, UpdateRowsEvent):
            #     update_data = {}
            #     update_data['table_name'] = binlogevent.table
            #     data_list = []
            #     for i in binlogevent.rows:
            #         data_list.append('after_values')
            #     update_data['data'] = data_list
            #     index_es_data = data_to_es(update_data)
            #     index_es_data.index_new_data()
            next_time_stamp = binlogevent.timestamp
        # stream.close()
        run_log = '{bin_log_name},{time_log}'.format(bin_log_name = next_binlog, time_log=int(next_time_stamp))
        write_file(run_log_file, run_log)
        print 'done'

def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.readline()

def write_file(file_name, content):
    with open(file_name, 'w+') as f:
        f.write(content)

def run():
    start_binlog, start_time_stamp = read_file(run_log_file).split(',')
    pull_bin_log(start_binlog, int(start_time_stamp))

run()
