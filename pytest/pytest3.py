import json
import requests
import os

# Make sure API key is set
if not os.environ.get("Google_API_KEY"):
    raise RuntimeError("Google_API_KEY not set")

with open('./stateToContinent.json', 'r') as stateDataFile:
    stateDataStr = stateDataFile.read()

# print(stateDataStr)

url = "https://maps.googleapis.com/maps/api/geocode/json?"

rparams = {'key': os.environ.get("Google_API_KEY"),
           'address': ""}

stateDataJson = json.loads(stateDataStr)
# print(stateDataJson[0])

for state in stateDataJson:
    rparams["address"] = state["state"]
    response = requests.get(url, params=rparams)
    responseJson = json.loads(response.text)

    if responseJson["results"][0]['address_components'][0]['short_name']:
        state['iso'] = responseJson["results"][0]['address_components'][0]['short_name']

    print(f"{state},")
# print(type(stateDataJson))

# for state in stateDataJson:
# print(f"{state['state']}  {state['continent']}")


# print(type(response))
# print(response.text)
# responseJson = json.loads(response)

