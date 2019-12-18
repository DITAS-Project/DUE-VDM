import time
import threading
from metrics.metric import Metric
from datetime import datetime
import numpy as np

METRIC_NAME = 'Response_Time'

VALUE_FIELD = 'value'
UNIT_FIELD = 'unit'


class ResponseTime(Metric):
    def __init__(self, conf_path='conf/conf.json'):
        super().__init__(conf_path)

    def compute_metric(self, update_interval):
        while True:
            # Compute time window of interest for the query
            t0 = datetime.now()
            time.sleep(update_interval)
            t1 = datetime.now()
            #TODO modificare metodo per la time window che non è conforme alle richeste
            timestamp, time_window = self.format_time_window(t0, t1)
            timestamp, time_window = '2016-06-20T22:28:46', '[2018-06-20T22:28:46 TO 2020-06-20T22:36:41]'  # TODO: delete this line
            vdcs = self.read_vdcs_from_file()
            for vdc in vdcs:
                methods = self.read_methods(vdc)
                for method in methods:
                    response = super().search(vdc, method, METRIC_NAME, timestamp, time_window)
                    responses = []
                    for element in response:
                        responses.append(element[VALUE_FIELD])
                    mean = np.mean(responses)
                    self.write(vdc, methods, mean, METRIC_NAME, response[0][UNIT_FIELD], timestamp, time_window)
            print()

    def launch_sync_update(self):
        queries = self.conf_data['response_time']['queries']
        for query in queries:
            update_interval = query['update_interval']
            threading.Thread(target=self.compute_metric, args=[update_interval]).start()