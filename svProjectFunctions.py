import requests
import json
import os

# login by usernames and ids
# add geoname username
if not os.environ.get("Geonames_username"):
    raise RuntimeError("Geonames_username not set")
geousername = os.environ.get("Geonames_username")
# check ggl api loaded
if not os.environ.get("Google_API_KEY"):
    raise RuntimeError("Google_API_KEY not set")
gglapikey = os.environ.get("Google_API_KEY")

# load the states data with street view
with open('./static/states.json', 'r') as statesDataFile:
    statesDataStr = statesDataFile.read()
statesDataJson = json.loads(statesDataStr)

# make a list of only available state iso codes
# set up a dict of "iso: {state:stateName, continent:continentName}
statesIsoList = []
statesIsoDict = {}
continentsStatesDict = {}

for state in statesDataJson:
    statesIsoList.append(state['iso'])
    statesIsoDict[state['iso']] = {"state":state['state'], "continent":state['continent']}

    # if the key was not exist, create one
    if not state['continent'] in continentsStatesDict:
        continentsStatesDict[state['continent']] = []
    
    # deal with UK/GB issue
    if state['iso'] == 'UK':
        continue

    continentsStatesDict[state['continent']].append({'iso': state['iso'], 'state': state['state']})

# print(statesIsoList)    
# print(statesIsoDict)

for con in continentsStatesDict:
    print(con)
    for stat in continentsStatesDict[con]:
        print(stat)


# load the subdivision database
with open('./static/iso-3166-2.json', 'r') as divisionsDataFile:
    divisionsDataStr = divisionsDataFile.read()
divisionDataJson = json.loads(divisionsDataStr)

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

def getRandomLocationInAvailableStates(isoCode = "yes"):

    # check the if the isocode vaild
    if (not isoCode in statesIsoList) and (isoCode != "yes"):
        return "invalid state code"           

    # get a random location in available states
    randomlandUrl = "https://api.3geonames.org/"
    randomlandParam = {'randomland': isoCode, 'json': 'yes'} 

    while True:
        response = tryGetRequestsUntilSuccess(randomlandUrl, params=randomlandParam) 
        # print(response.text)
        
        responseJson = response.json()
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

    # request ggl street view metadata
    # prerequisite
    gglSvMetadataUrl = "https://maps.googleapis.com/maps/api/streetview/metadata"
    gglSvMetadataParam = {"location": f"{lat}, {lon}", "radius": 1000 ,"key": gglapikey, "source": "outdoor"}

    # try to get a vaild coordinate, increase the radius every time
    while True:
        response = tryGetRequestsUntilSuccess(gglSvMetadataUrl, params=gglSvMetadataParam)
        responseJson = response.json()

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

    # prerequisite
    isoCodeUrl = "http://api.geonames.org/countryCode"
    isoCodeParam = {'lat':lat, 'lng':lon, 'username': geousername}

    # get feedback from geonames api
    response = tryGetRequestsUntilSuccess(isoCodeUrl, params=isoCodeParam)
    return response.text[0:2]
    # responseJson = json.loads(response.text)

def getSubdivisionForCoordinate(lat,lon):
    
    isoCode = getIsoCodeForCoordinate(lat,lon)    

    # prerequisite
    subdivisionUrl = 'http://api.geonames.org/countrySubdivisionJSON'
    subdivisionParam = {'lat':lat, 'lng':lon, 'username': geousername}
    
    response = tryGetRequestsUntilSuccess(subdivisionUrl, params=subdivisionParam)
    responseJson = response.json()

    stddivisionCode = f"{isoCode}-{responseJson['codes'][0]['code']}"
    stddivisionName = divisionDataJson[isoCode]['divisions'][stddivisionCode]

    return {'divisionCode': stddivisionCode, 'divisionName': stddivisionName}

def getStateForIsoCode(isoCode):
    return statesIsoDict[isoCode]['state']

def getContinentForIsoCode(isoCode):
    return statesIsoDict[isoCode]['continent']

def getRandomStates(continent, exclusion = None):
    