import json
from abc import ABC, abstractmethod
import requests
import os
import lockfile


OUTPUT_PATH = 'aggregated_metrics.json'
BP_ABSTRACT_PROPERTIES = 'ABSTRACT_PROPERTIES'
BP_METHOD_ID = 'method_id'

CONF_CONNECTION = 'connection'
CONF_CONN_HOST = 'host'
CONF_CONN_PORT = 'port'
CONF_BLUEPRINT = 'blueprints_path'

RESULTS = 'computation_results'

class Metric(ABC):
    def __init__(self, conf_path):
        with open(conf_path) as conf_file:
            conf_data = json.load(conf_file)
        host = conf_data[CONF_CONNECTION][CONF_CONN_HOST]
        port = conf_data[CONF_CONNECTION][CONF_CONN_PORT]
        self.base = 'http://' + host + ':' + str(port) + '/meter/'
        self.conf_data = conf_data
        self.bp_path = conf_data[CONF_BLUEPRINT]
        if not os.path.exists(OUTPUT_PATH):
            body = {
                RESULTS: []
            }
            file = open(OUTPUT_PATH, 'w+')
            file.write(json.dumps(body))
            file.close()


    def format_time_window(self, t0, t1):
        start_time = t0.strftime('%Y-%m-%dT%H:%M:%S')
        end_time = t1.strftime('%Y-%m-%dT%H:%M:%S')
        return end_time, f'@timestamp:[{start_time} TO {end_time}]'

    @abstractmethod
    def compute_metric(self, update_interval):
        pass

    @abstractmethod
    def launch_sync_update(self):
        pass

    def search(self, vdc, op_id, metric, start_time, end_time):
        vdc = vdc.split('.')[0]
        path = self.base + vdc
        params = {
            'vdcId': vdc,
            'operationID': op_id,
            'name': metric,
            'startTime': start_time,
            'endTime': end_time
        }
        return requests.get(path, params).json()

    def write(self, vdc_inst, operation_id, value, name, unit, hit_timestamp, computation_timestamp):
        vdc_inst = vdc_inst.split('.')[0]
        body = {
            'meter': {
                'vdc': vdc_inst,
                'operationId': operation_id,
                'value': value,
                'name': name,
                'unit': unit,
                'hit-timestamp': hit_timestamp,
                'computation-timestamp': computation_timestamp
            }
        }

        with lockfile.LockFile(OUTPUT_PATH):
            file = open(OUTPUT_PATH, 'r+')
            data = json.load(file)
            data[RESULTS].append(body)
            file.seek(0)
            file.write(json.dumps(data, indent=4))
            file.close()

    def read_vdcs_from_file(self):
        return os.listdir(self.bp_path)

    def read_methods(self, vdc):
        print('Detected methods for ' + vdc + ':')
        with open(os.path.join(self.bp_path, vdc)) as file:
            blueprint = json.load(file)
        methods = []
        for method in blueprint[BP_ABSTRACT_PROPERTIES]:
            methods.append(method[BP_METHOD_ID])
        print(methods)
        return methods