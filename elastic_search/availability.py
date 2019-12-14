import time
import threading
from elastic_search.metric import Metric
from datetime import datetime
import numpy as np

METRIC_NAME = 'Availability'

VALUE_FIELD = 'value'
UNIT_FIELD = 'unit'

class Availability(Metric):
    def __init__(self, conf_path='conf/conf.json'):
        super().__init__(conf_path)

    def compute_metric(self, update_interval):
        while True:
            # Compute time window of interest for the query
            t0 = datetime.now()
            time.sleep(update_interval)
            t1 = datetime.now()
            timestamp, time_window = self.format_time_window(t0, t1)
            timestamp, time_window = '2016-06-20T22:28:46', '[2018-06-20T22:28:46 TO 2020-06-20T22:36:41]'  # TODO: delete this line
            # TODO anzichè ciclare su servizi -> ciclare su infraID e metodi che si trovano nel file conf (momentaneo?)
            vdcs = self.read_vdcs_from_file()
            for vdc in vdcs:
                methods = self.read_methods(vdc)
                for method in methods:
                    response = super().search(vdc, method, METRIC_NAME, timestamp, time_window)
                    availabilities = []
                    for element in response:
                        availabilities.append(element[VALUE_FIELD])
                    mean = np.mean(availabilities)
                    self.write(vdc, methods, mean, METRIC_NAME, response[0][UNIT_FIELD], timestamp, time_window)
            print()

    def launch_sync_update(self):
        queries = self.conf_data['availability']['queries']
        for query in queries:
            update_interval = query['update_interval']
            threading.Thread(target=self.compute_metric, args=[update_interval]).start()
            break  # TODO: delete this line