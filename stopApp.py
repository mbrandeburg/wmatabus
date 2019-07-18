import os
import requests
import pandas as pd

key = os.environ['wmataKey']
# print(key)

stopID = 1002872 #Stops: 1002872 for 16&Irving, 1002042 for 7-11, 1001183 for Faraguet
URL = "https://api.wmata.com/NextBusService.svc/json/jPredictions?StopID={}".format(stopID)
HEADER = {'api_key': key} #dictionary with my api auth parameters (it wants my api token)


def busStop(stopID): # we can make stopID automatically populate by time of day?
    r = requests.get(url=URL, params= HEADER)
    data = r.json()
    stopNameList = []
    busNumberList = []
    busDurationList = []
    for i in range(0,len(data['Predictions'])):
        if data['Predictions'][i]['DirectionNum'] == "1":
            stopName = data['StopName']
            busNumber = data['Predictions'][i]['RouteID']
            busDuration = data['Predictions'][i]['Minutes']
            stopNameList.append(stopName)
            busNumberList.append(busNumber)
            busDurationList.append(busDuration)
    return stopNameList, busNumberList, busDurationList
# print(busStop(stopID))

busList = busStop(stopID)
print(busList)
# df = pd.DataFrame(busList, columns=['Stop', 'Bus', 'Minutes'])
# print(df)


# r = requests.get(url=URL, params= HEADER)
# data = r.json()
# print(data['StopName'],"\n")
# for i in range(0,len(data['Predictions'])):
#     # print(data['Predictions'][i]['DirectionNum']) #1 is south, 0 is north 
#     if data['Predictions'][i]['DirectionNum'] == "1": #not integers but strings!
#         # print(data['Predictions'][i]['RouteID']) #bus numbers
#         print("The next {} arrives in {} minutes\n".format(data['Predictions'][i]['RouteID'], data['Predictions'][i]['Minutes']))

# # print(data['Predictions']) #full list of details I can comb from

# ### TODO: TURN INTO FUNCTION, THEN TURN INTO FLASK APP