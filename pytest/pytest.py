import requests

meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
api_key = 'AIzaSyDVFJCdg8ozDOHNQk_R9_RSMfiuEv6WZJU'
# using my graduate school almar mater, GWU, as an example
location = '2121 I St NW, Washington, DC 20052'

# define the params for the metadata reques
meta_params = {'key': api_key,
               'location': location}
# define the params for the picture request
pic_params = {'key': api_key,
              'location': location,
              'size': "640x640"}

meta_response = requests.get(meta_base, params=meta_params)
pic_response = requests.get(pic_base, params=pic_params)

for key, value in pic_response.headers.items():
    print(f"{key}: {value}")