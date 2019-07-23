import os
import requests
import pandas as pd
from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)
key = os.environ['wmataKey']

##Stops: 1002872 for 16&Irving, 1002042 for 7-11, 1001183 for Faraguet
stopID = 1002872 
stopID2 = 1001183

## Bustop function
# TODO: can we make stopID automatically populate by time of day?
def busStop(stopNum): 
    ## Engage the API
    URL = "https://api.wmata.com/NextBusService.svc/json/jPredictions?StopID={}".format(stopNum)
    HEADER = {'api_key': key} #dictionary with my api auth parameters (it wants my api token)
    ## work with API data
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
busList2 = busStop(stopID2)

# df = pd.DataFrame(busList[0], columns=['Stop'])
# df['Bus'] = busList[1]
# df['Time'] = busList[2]

# df2 = pd.DataFrame(busList2[0], columns=['Stop'])
# df['Bus'] = busList2[1]
# df['Time'] = busList2[2]
# print(df)

location1 = busList[0][0]
bus1 = busList[1][0]
bus2 = busList[1][1]
bus3 = busList[1][2]
time1 = busList[2][0]
time2 = busList[2][1]
time3 = busList[2][2]

location2 = busList2[0][0]
bus2x1 = busList2[1][0]
bus2x2 = busList2[1][1]
bus2x3 = busList2[1][2]
time2x1 = busList2[2][0]
time2x2 = busList2[2][1]
time2x3 = busList2[2][2]

## FLASK RENDER THE WEBPAGE:
## main webpage
@app.route("/")
def webFramesUnique():
    return render_template('index.html', location1=location1, bus1=bus1, bus2=bus2, time1=time1, time2=time2, bus3=bus3, time3=time3, location2=location2)

## alternate route webpage
@app.route("/route2")
def webFramesUnique2():
    return render_template('index2.html', location1=location2x1, bus1=bus2x1, bus2=bus2x2, time1=time2x1, time2=time2x2, bus3=bus2x3, time3=time2x3, location2=location2)

## favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

### INITAITE IT VIA FLASK
if __name__ == "__main__":
    app.run() #unsetting for heroku - normally: app.run(host='0.0.0.0', port=8000) 
    # gunicorn -w 4 -b 0.0.0.0:8000 stopApp:app --timeout 500
    







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
