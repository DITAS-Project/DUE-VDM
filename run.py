#TODO questa classe è solo una prova

import requests

response = requests.get('http://0.0.0.0:8080/data-analytics/meter/cloudsigma-deployment/?operationID=getAllValuesForBloodTestComponent&name=Availability&startTime=20-JUN-1990%2008%3A03%3A00&endTime=20-JUN-2019%2008%3A03%3A00')
print(response)