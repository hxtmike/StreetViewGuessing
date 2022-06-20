from svProjectFunctions import getRandomLocationInAvailableStates, getVaildGoogleStreetViewPano, getHemiForCoordinate, getIsoCodeForCoordinate

test = getRandomLocationInAvailableStates()

print(test['stateCode'])
print(test['lat'])
print(test['lon'])


# test a remote location in Tibet
# rsps = getVaildGoogleStreetViewPano(33.203053, 83.246762)
rsps = getVaildGoogleStreetViewPano(test['lat'], test['lon'])
print(rsps['location']['lat'])
print(rsps['location']['lng'])
print(rsps['pano_id'])
# print(type(rsps))

hemi = getHemiForCoordinate(rsps['location']['lat'], rsps['location']['lng'])
print(hemi)

isoCode = getIsoCodeForCoordinate(rsps['location']['lat'], rsps['location']['lng'])
print(isoCode)