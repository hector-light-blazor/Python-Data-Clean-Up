import arcpy, sys
from arcpy import env
from handler import *




# Setup Legacy Data
AustinStreetShapefileReference = "C:/Users/Noe956/Documents/GIS/HC_IT/DataReference/AustinStreetsLine/AustinStreets.shp"

unique_values(AustinStreetShapefileReference, 'street_typ')

print("Done Gathering Legacy Street Type")

# Change Environment to the correct gis database clean up..
env.workspace = "C:/Users/Noe956/Documents/GIS/HC_IT/GIS_DATA_Hidalgo.gdb"


feature_address_points = "Address_Points"

feature_road_centerlines = "Road_Centerlines"

fields_address_points = ['fullname', 'objectid', 'prd']

update_address_points = ['prd', 'objectid']


print("PARSING DIRTY DATA")

# prefixDirValuesDirtyAddressPoints = startPreDirProcess(feature_address_points, ['fullname', 'objectid', 'prd'])

# Update the fields address
responseFromPostDir = startPostDirProcess(feature_road_centerlines, ['objectid', 'fullname', 'SuffixDirect'])
print(responseFromPostDir)

responseFromPreDir = startPreDirProcess(feature_road_centerlines, ['objectid', 'fullname', 'PrefixDir'])
print(responseFromPreDir)

responseFromStreetType = startStTypeProcess(feature_road_centerlines, ['objectid', 'fullname', 'StreetType'])
print(responseFromStreetType)

#Road Names must be final from street type and pre directional. Is dependant on those values.
responseRoadNames = startRoadNameProcess(feature_road_centerlines, ['objectid', 'fullname', 'PrefixDir', 'StreetType'])
print(responseRoadNames)


print("Done Updating Everything")


