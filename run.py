from metrics.throughput import Throughput
from metrics.response_time import ResponseTime
from metrics.availability import Availability

if __name__ == "__main__":
    es = Throughput()
    es.launch_sync_update()
    es = ResponseTime()
    es.launch_sync_update()
    es = Availability()
    es.launch_sync_update()