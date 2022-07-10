from svProjectFunctions import getSubdivisionForCoordinate, getRandomStatesGivenContinent, getRandomdivisionsGivenState

# randomStates = getRandomStates('Asia')
# randomStates = getRandomStates('Antarctica')

# rst = getSubdivisionForCoordinate(-55.0828346964738,-67.07463330868543)

rst = getRandomStatesGivenContinent("Oceania", "VU")
print(rst)

rst = getRandomdivisionsGivenState('HK', "HK-HK")
print(rst)

rst = getRandomdivisionsGivenState('CN', "CN-31")
print(rst)