import json
import pytz
from datetime import datetime, timedelta
import dateutil.parser
import os

TEMP_CONF_FILE = 'conf/conf.json'
TEMP_SERVICES_FILE = 'conf/services.json'
TEMP_INDEX = "tubvdc-*"


def format_time_window(t0, t1):
    start_time = t0.strftime('%Y-%m-%dT%H:%M:%S')
    end_time = t1.strftime('%Y-%m-%dT%H:%M:%S')
    return end_time, f'[{start_time} TO {end_time}]'


# Compute time window of interest for the query
def get_timestamp_timewindow(minutes):
    t0 = datetime.now(pytz.utc)
    t1 = t0 - timedelta(minutes=minutes)
    return format_time_window(t0, t1)


def read_services_from_file(filepath):
    with open(filepath) as services_file:
        services = json.load(services_file)
    return services['services']


def get_services():
    return read_services_from_file(TEMP_SERVICES_FILE)


def parse_timestamp(datestring):
    return dateutil.parser.parse(datestring)