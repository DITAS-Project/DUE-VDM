import json
import uuid
from abc import ABC, abstractmethod
import requests
import os


OUTPUT_PATH = 'aggregated_metrics.json'
BP_ABSTRACT_PROPERTIES = 'ABSTRACT_PROPERTIES'
BP_METHOD_ID = 'method_id'

CONF_CONNECTION = 'connection'
CONF_CONN_HOST = 'host'
CONF_CONN_PORT = 'port'
CONF_BLUEPRINT = 'blueprints_path'

class Metric(ABC):
    def __init__(self, conf_path):
        with open(conf_path) as conf_file:
            conf_data = json.load(conf_file)
        host = conf_data[CONF_CONNECTION][CONF_CONN_HOST]
        port = conf_data[CONF_CONNECTION][CONF_CONN_PORT]
        self.base = 'http://' + host + ':' + str(port) + '/data-analytics/meter/'
        self.conf_data = conf_data
        self.bp_path = conf_data[CONF_BLUEPRINT]

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

    def search(self, infra_id, op_id, metric, start_time, end_time):
        path = self.base + infra_id
        params = {
            'operationID': op_id,
            'name': metric,
            'startTime': start_time,
            'endTime': end_time
        }
        return requests.get(path, params)

    def __format_key(self, bp_id, vdc_inst, request_id, operation_id):
        return bp_id + '-' + vdc_inst + '-' + request_id + '-' + operation_id

    def write(self, bp_id, vdc_inst, request_id, operation_id, value, name, unit, hit_timestamp, computation_timestamp):
        body = {
            'meter': {
                'key': self.__format_key(bp_id, vdc_inst, request_id, operation_id),
                'value': value,
                'name': name,
                'unit': unit,
                'hit-timestamp': hit_timestamp,
                'computation-timestamp': computation_timestamp
            }
        }
        #TODO cambiare la modalità di salvataggio da W in Append
        # Se viene appeso il file json non sarà più valido quindi bisogna aprire il file se esiste e aggiungere una nuova entry
        with open(OUTPUT_PATH, 'w') as outfile:
            json.dump(body, outfile, indent=4)

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