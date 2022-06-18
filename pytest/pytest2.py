import requests
import xml.dom.minidom

url = "https://api.3geonames.org/?randomland=yes"

rsps =  requests.get(url)

# print(rsps.text)

# xml parse

xmlprs = xml.dom.minidom.parseString(rsps.text)

print(type(xmlprs))
print(xmlprs)

# xmlprs = prs.toxml()

# print(type(xmlprs))
# print(xmlprs)

states = xmlprs.getElementsByTagName("state")
print(states)

print(states[0].childNodes[0].data)