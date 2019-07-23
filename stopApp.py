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
def busStop(stopNum, intGiven): 
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
        if data['Predictions'][i]['DirectionNum'] == intGiven:
            stopName = data['StopName']
            busNumber = data['Predictions'][i]['RouteID']
            busDuration = data['Predictions'][i]['Minutes']
            if intGiven == "0": #if northbound, we only care about buses 42 and 43
                if busNumber == "42":
                    stopNameList.append(stopName)
                    busNumberList.append(busNumber)
                    busDurationList.append(busDuration)
                elif busNumber == "43":
                    stopNameList.append(stopName)
                    busNumberList.append(busNumber)
                    busDurationList.append(busDuration)
            else: #ignoring for south-bound
                stopNameList.append(stopName)
                busNumberList.append(busNumber)
                busDurationList.append(busDuration)
    return stopNameList, busNumberList, busDurationList
# print(busStop(stopID, "1"))

## call function - takes a string, but 1 is south, 0 is north 
busList = busStop(stopID, "1")
busList2 = busStop(stopID2, "0")

### pull out results for webpage variables
## in case there are fewer than 3 buses coming past a given stop (i.e. late and end of service)
# southbound
if len(busList[0]) >= 3:
    location1 = busList[0][0]
    bus1 = busList[1][0]
    bus2 = busList[1][1]
    bus3 = busList[1][2]
    time1 = busList[2][0]
    time2 = busList[2][1]
    time3 = busList[2][2]
elif len(busList[0]) == 2:
    location1 = busList[0][0]
    bus1 = busList[1][0]
    bus2 = busList[1][1]
    bus3 = "No more in service"
    time1 = busList[2][0]
    time2 = busList[2][1]
    time3 = "N/A"
elif len(busList[0]) == 1:
    location1 = busList[0][0]
    bus1 = busList[1][0]
    bus2 = "No more in service"
    bus3 = "No more in service"
    time1 = busList[2][0]
    time2 = "N/A"
    time3 = "N/A"
elif len(busList[0]) == 0:
    location1 = "No more in service"
    bus1 = "No more in service"
    bus2 = "No more in service"
    bus3 = "No more in service"
    time1 = "N/A"
    time2 = "N/A"
    time3 = "N/A"
# northbound
if len(busList2[0]) >= 3:
    location2 = busList2[0][0]
    bus2x1 = busList2[1][0]
    bus2x2 = busList2[1][1]
    bus2x3 = busList2[1][2]
    time2x1 = busList2[2][0]
    time2x2 = busList2[2][1]
    time2x3 = busList2[2][2]
elif len(busList2[0]) == 2:
    location2 = busList2[0][0]
    bus2x1 = busList2[1][0]
    bus2x2 = busList2[1][1]
    bus2x3 = "No more in service"
    time2x1 = busList2[2][0]
    time2x2 = busList2[2][1]
    time2x3 = "N/A"
elif len(busList2[0]) == 1:
    location2 = busList2[0][0]
    bus2x1 = busList2[1][0]
    bus2x2 = "No more in service"
    bus2x3 = "No more in service"
    time2x1 = busList2[2][0]
    time2x2 = "N/A"
    time2x3 = "N/A"
elif len(busList2[0]) == 0:
    location2 = "No more in service"
    bus2x1 = "No more in service"
    bus2x2 = "No more in service"
    bus2x3 = "No more in service"
    time2x1 = "N/A"
    time2x2 = "N/A"
    time2x3 = "N/A"

## FLASK RENDER THE WEBPAGE:
## main webpage
@app.route("/")
def webFramesUnique():
    return render_template('index.html', location1=location1, bus1=bus1, bus2=bus2, time1=time1, time2=time2, bus3=bus3, time3=time3, location2=location2)

## alternate route webpage
@app.route("/route2")
def webFramesUnique2():
    return render_template('index2.html', location1=location1, bus1=bus2x1, bus2=bus2x2, time1=time2x1, time2=time2x2, bus3=bus2x3, time3=time2x3, location2=location2)

## favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

### INITAITE IT VIA FLASK
if __name__ == "__main__":
    app.run() #unsetting for heroku - normally: app.run(host='0.0.0.0', port=8000) 
    # gunicorn -w 4 -b 0.0.0.0:8000 stopApp:app --timeout 500
    