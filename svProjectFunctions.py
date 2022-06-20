import requests
import json
import os

def tryGetRequestsUntilSuccess(url, params=None, **kwargs):
    # counter i
    i = 0

    while True:
        try:
            response =  requests.get(url, params=params, **kwargs)
            if response.status_code == 200:
                return response
        except:
            i += 1
            print(f"the requests failed {i} times, retry")

def getRandomLocationInAvailableStates():

    # load the states data with street view
    with open('./static/states.json', 'r') as statesDataFile:
        statesDataStr = statesDataFile.read()
    statesDataJson = json.loads(statesDataStr)

    # make a list of only available state iso codes
    statesIsoList = []
    for state in statesDataJson:
        statesIsoList.append(state['iso'])
    # print(statesIsoList)    

    # get a random location in available states
    randomlandUrl = "https://api.3geonames.org/"
    randomlandParam = {'randomland': 'yes', 'json': 'yes'} 
    while True:
        response = tryGetRequestsUntilSuccess(randomlandUrl, params=randomlandParam) 
        # print(response.text)
        responseJson = json.loads(response.text)
        # there might be no value in the state tag
        try:
            responseStateIso = responseJson['nearest']['state']
            responseLat = responseJson['nearest']['latt']
            responseLon = responseJson['nearest']['longt']
        except:
            # print(response.text)
            continue
        # print(responseStateIso)

        # make the returning values
        result = { 'stateCode' : responseStateIso, 'lat': responseLat, 'lon': responseLon }
        # check whether the state iso code is available or not
        if responseStateIso in statesIsoList:
            # print(responseStateIso) 
            return result

def getVaildGoogleStreetViewPano(lat, lon):
    # check ggl api loaded
    if not os.environ.get("Google_API_KEY"):
        raise RuntimeError("Google_API_KEY not set")
    gglapikey = os.environ.get("Google_API_KEY")

    # request ggl street view metadata
    # prerequisite
    gglSvMetadataUrl = "https://maps.googleapis.com/maps/api/streetview/metadata"
    gglSvMetadataParam = {"location": f"{lat}, {lon}", "radius": 1000 ,"key": gglapikey, "source": "outdoor"}


    # try to get a vaild coordinate, increase the radius every time
    while True:
        response = tryGetRequestsUntilSuccess(gglSvMetadataUrl, params=gglSvMetadataParam)
        responseJson = json.loads(response.text)

        # increase the radius and retry
        if responseJson['status'] == "OK":
            return responseJson
        else:
            # print(response.text)
            gglSvMetadataParam['radius'] *= 10
            # print(f"the radius is increased to {gglSvMetadataParam['radius']}")

def getHemiForCoordinate(lat,lon):
    if int(lat) >= 0:
        return "North"
    else:
        return "South"

def getIsoCodeForCoordinate(lat,lon):
    
    if not os.environ.get("Geonames_username"):
        raise RuntimeError("Geonames_username not set")
    geousername = os.environ.get("Geonames_username")

    # prerequisite
    isoCodeUrl = "http://api.geonames.org/countryCode"
    isoCodeParam = {'lat':lat, 'lng':lon, 'username': geousername}

    # get feedback from geonames api
    response = tryGetRequestsUntilSuccess(isoCodeUrl, params=isoCodeParam)
    return response.text[0:2]
    # responseJson = json.loads(response.text)

def getContinentForIsoCode(isoCode):
    