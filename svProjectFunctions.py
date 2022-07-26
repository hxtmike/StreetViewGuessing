import requests
import json
import os
import random
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

# make a list of only available state iso code
# set up a dict of "iso: {state:stateName, continent:continentName}
statesIsoList = []
statesIsoDict = {}
continentsStatesDict = {}

for state in statesDataJson:
    statesIsoList.append(state['iso'])
    statesIsoDict[state['iso']] = {"state":state['state'], "continent":state['continent']}

    # if the key was not exist, create one
    if not state['continent'] in continentsStatesDict:
        continentsStatesDict[state['continent']] = {}
    
    # deal with UK/GB issue, delete item 'UK'
    if state['iso'] == 'UK':
        continue

    continentsStatesDict[state['continent']][state['iso']] = state['state']

# print(statesIsoList)    
# print(statesIsoDict)

# for con in continentsStatesDict:
#     print(con)
#     print(continentsStatesDict[con])


# load the subdivision database
with open('./static/iso-3166-2.json', 'r') as divisionsDataFile:
    divisionsDataStr = divisionsDataFile.read()
divisionsDataJson = json.loads(divisionsDataStr)
# the dict which is covering 237 states is too large, cut it
divisionsSelectedDict = {}

for iso in statesIsoList:
    # print(iso)
    # print(divisionDataJson[iso])
    if iso == 'UK':
        continue
    # the dict of iso-3166-2 could be simplified
    divisionsSelectedDict[iso] = divisionsDataJson[iso]['divisions']

# print(divisionSelectedDict)


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
    if float(lat) >= 0:
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

        # print(f"{lat}\n{lon}\n{i}\n{responseJson}")
        # print()
    try:   
        stddivisionCode = f"{isoCode}-{responseJson['codes'][0]['code']}"
        return stddivisionCode
    except:
        # "unknown division"
        return 1

def getStateForIsoCode(isoCode):
    return statesIsoDict[isoCode]['state']

def getContinentForIsoCode(isoCode):
    return statesIsoDict[isoCode]['continent']

# input is code of answer, but returning value is full name of it
def getRandomOptionsGivenAnswer(Range, answerCode, multipleDict):
    #first, check if the answer in the list, if not then directly return error message
    if not answerCode in multipleDict[Range]:
        # the answer is not in the range 
        return 1
    
    returnValue = []
    # return 4 options, so check the number of item
    # print(len(multipleDict[Range]))
    if len(multipleDict[Range]) < 5:
        # check the right or wrong for each answer
        for item in multipleDict[Range]:
            # print(state)
            if item == answerCode:
                returnValue.append([multipleDict[Range][item], True])
            else:
                returnValue.append([multipleDict[Range][item], False])
        # random the organised list
        # print(returnValue)
    else:
        # get 4 values for return 4 options
        shortList = random.sample(multipleDict[Range].keys(), 4)
        # print(shortList)
        if answerCode in shortList:
            # check the right or wrong for each answer
            for item in shortList:
                # print(state)
                if item == answerCode:
                    returnValue.append([multipleDict[Range][item], True])
                else:
                    returnValue.append([multipleDict[Range][item], False])
        else:
            for item in shortList:
                returnValue.append([multipleDict[Range][item], False])
            # randomly replace the first element of the list, same as del a random item in the list
            returnValue[0] = [multipleDict[Range][answerCode], True]
            
    random.shuffle(returnValue)
    return returnValue
        # 
        # if answerCode in shortList:


def getRandomStatesGivenContinent(continent, stateIso):
    return getRandomOptionsGivenAnswer(continent, stateIso, continentsStatesDict)

def getRandomdivisionsGivenState(state, divisionIso):
    return getRandomOptionsGivenAnswer(state, divisionIso, divisionsSelectedDict)

def getResultForWeb(state = 0):
    if state == 0:
        originalRandomCoordinate = getRandomLocationInAvailableStates()
    else:
        originalRandomCoordinate = getRandomLocationInAvailableStates(isoCode = state)
    originalRandomLat = originalRandomCoordinate['lat']
    originalRandomLon = originalRandomCoordinate['lon']
    # print(originalRandomLat)
    # print(originalRandomLon)
    # print()

    validGoogleCoordinate = getVaildGoogleStreetViewPano(originalRandomLat, originalRandomLon)
    panoId = validGoogleCoordinate['pano_id']
    lat = validGoogleCoordinate['location']['lat']
    lon = validGoogleCoordinate['location']['lng']
    # print(panoId)
    # print(lat)
    # print(lon)
    # print()

    stateCode = getIsoCodeForCoordinate(lat, lon)
    # print(stateCode)
    # print()

    divisionCode = getSubdivisionForCoordinate(lat, lon)
    # print(divisionCode)
    # print()

    hemi = getHemiForCoordinate(lat, lon)
    # print(hemi)
    # print()

    continent = getContinentForIsoCode(stateCode)
    # print(continent)
    # print()

    stateOptions = getRandomStatesGivenContinent(continent, stateCode)
    # print(stateOptions)
    # print()

    # deal with unknown division issue
    if divisionCode == 1:
        divisionOptions = 2
    else:
        divisionOptions = getRandomdivisionsGivenState(stateCode, divisionCode)
        # print(divisionOptions)
        # print()

    return {'panoId':panoId, 'lat':lat, 'lon':lon, 'hemi': hemi, 'continent':continent, 'state':stateOptions, 'division': divisionOptions}
    # for last 2 keys
    # returning code 1 means "could not find value with given iso code"
    # returning code 2 means "unknown division"