from svProjectFunctions import getRandomLocationInAvailableStates, getVaildGoogleStreetViewPano, getHemiForCoordinate, getIsoCodeForCoordinate, getStateForIsoCode, getContinentForIsoCode, getSubdivisionForCoordinate

# check the invalid state code option
test = getRandomLocationInAvailableStates()

print(test['stateCode'])
print(test['lat'])
print(test['lon'])
print()



# test a remote location in Tibet
# rsps = getVaildGoogleStreetViewPano(33.203053, 83.246762)
rsps = getVaildGoogleStreetViewPano(test['lat'], test['lon'])
print(rsps['location']['lat'])
print(rsps['location']['lng'])
print(rsps['pano_id'])
print()
# print(type(rsps))

hemi = getHemiForCoordinate(rsps['location']['lat'], rsps['location']['lng'])
print(hemi)

isoCode = getIsoCodeForCoordinate(rsps['location']['lat'], rsps['location']['lng'])
# the UK GB problem
# isoCode = getIsoCodeForCoordinate(51,0)
print(isoCode)

state = getStateForIsoCode(isoCode)
print(state)

continent = getContinentForIsoCode(isoCode)
print(continent)

division = getSubdivisionForCoordinate(rsps['location']['lat'], rsps['location']['lng'])
print(division['divisionCode'])
print(division['divisionName'])
