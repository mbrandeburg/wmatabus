import os
import requests
import pandas as pd
from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

key = 'e13626d03d8e4c03ac07f95541b3091b'
# key = os.environ['wmataKey']
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

df = pd.DataFrame(busList[0], columns=['Stop'])
df['Bus'] = busList[1]
df['Time'] = busList[2]
print(df)

### TODO: 1) DEPLOY TO HEROKU

location1 = busList[0][0]
bus1 = busList[1][0]
bus2 = busList[1][1]
bus3 = busList[1][2]
time1 = busList[2][0]
time2 = busList[2][1]
time3 = busList[2][2]

## FLASK RENDER THE WEBPAGE:
@app.route("/")
def webFramesUnique():
    return render_template('index.html', data=df.to_html(), location1=location1, bus1=bus1, bus2=bus2, time1=time1, time2=time2, bus3=bus3, time3=time3)

if __name__ == "__main__":
    # gunicorn -w 4 -b 0.0.0.0:8000 stopApp:app --timeout 500
    # procfile: https://stackoverflow.com/questions/38851564/heroku-gunicorn-procfile
    app.run(host='0.0.0.0', port=8000) 


## WORKING WITH THE API:
# r = requests.get(url=URL, params= HEADER)
# data = r.json()
# print(data['StopName'],"\n")
# for i in range(0,len(data['Predictions'])):
#     # print(data['Predictions'][i]['DirectionNum']) #1 is south, 0 is north 
#     if data['Predictions'][i]['DirectionNum'] == "1": #not integers but strings!
#         # print(data['Predictions'][i]['RouteID']) #bus numbers
#         print("The next {} arrives in {} minutes\n".format(data['Predictions'][i]['RouteID'], data['Predictions'][i]['Minutes']))

# # print(data['Predictions']) #full list of details I can comb from
