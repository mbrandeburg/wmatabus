import os
import requests

key = os.environ['wmataKey']
# print(key)

stopID = 1001195 #dummy stop ID
URL = "https://api.wmata.com/NextBusService.svc/json/jPredictions?StopID={}".format(stopID)
HEADER = {'api_key': key} #dictionary with my api auth parameters (it wants my api token)

r = requests.get(url=URL, params= HEADER)
data = r.json()
print(data)