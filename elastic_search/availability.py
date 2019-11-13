import time
import threading
from elastic_search.metric import Metric
from datetime import datetime

METRIC_NAME = 'Availability'

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
                self.read_methods(vdc)


            '''

                #TODO no hardcode
                response = super().search("cloudsigma-deployment","getAllValuesForBloodTestComponent", METRIC_NAME,
                                          timestamp, time_window)

                #TODO ciclare sul numero di risposte x calcolare media valore
                #for hit in hits:


                #self.write(hit['BluePrint-ID'], hit['VDC-Instance-ID'], hit['Request-ID'], hit['Operation-ID'],hit['value'], hit['metric'], hit['unit'], hit['hit-timestamp'], hit['@timestamp'])
                print()'''

    def launch_sync_update(self):
        queries = self.conf_data['availability']['queries']
        for query in queries:
            update_interval = query['update_interval']
            threading.Thread(target=self.compute_metric, args=[update_interval]).start()
            break  # TODO: delete this line