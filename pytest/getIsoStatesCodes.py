import json
import requests
import os
from svProjectFunctions import tryGetRequestsUntilSuccess

# Make sure API key is set
if not os.environ.get("Google_API_KEY"):
    raise RuntimeError("Google_API_KEY not set")

# load data from json file which contain all available street view countries
with open('./stateToContinent.json', 'r') as stateDataFile:
    stateDataStr = stateDataFile.read()
stateDataJson = json.loads(stateDataStr)

# print(stateDataStr)
# print(stateDataJson[0])

url = "https://maps.googleapis.com/maps/api/geocode/json?"
rparams = {'key': os.environ.get("Google_API_KEY"),
           'address': ""}

# get iso code for each state
for state in stateDataJson:
    rparams["address"] = state["state"]
    # response = requests.get(url, params=rparams)
    response = tryGetRequestsUntilSuccess(url, params=rparams)
    responseJson = json.loads(response.text)

    if responseJson["results"][0]['address_components'][0]['short_name']:
        state['iso'] = responseJson["results"][0]['address_components'][0]['short_name']

    print(f'{state},')
# print(type(stateDataJson))

# for state in stateDataJson:
# print(f"{state['state']}  {state['continent']}")


# print(type(response))
# print(response.text)
# responseJson = json.loads(response)

