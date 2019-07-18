import os
import requests

key = os.environ['wmataKey']
# print(key)

stopID = 1002872 #Stops: 1002872 for 16&Irving, 1002042 for 7-11, 1001183 for Faraguet
URL = "https://api.wmata.com/NextBusService.svc/json/jPredictions?StopID={}".format(stopID)
HEADER = {'api_key': key} #dictionary with my api auth parameters (it wants my api token)

r = requests.get(url=URL, params= HEADER)
data = r.json()
print(data['StopName'],"\n")
for i in range(0,len(data['Predictions'])):
    # print(data['Predictions'][i]['DirectionNum']) #1 is south, 0 is north 
    if data['Predictions'][i]['DirectionNum'] == "1": #not integers but strings!
        # print(data['Predictions'][i]['RouteID']) #bus numbers
        print("The next {} arrives in {} minutes\n".format(data['Predictions'][i]['RouteID'], data['Predictions'][i]['Minutes']))

# print(data['Predictions']) #full list of details I can comb from