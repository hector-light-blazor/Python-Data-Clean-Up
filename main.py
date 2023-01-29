import arcpy, sys
from arcpy import env
from handler import *




# Setup Legacy Data
AustinStreetShapefileReference = "C:/Users/Noe956/Documents/GIS/HC_IT/DataReference/AustinStreetsLine/AustinStreets.shp"

unique_values(AustinStreetShapefileReference, 'street_typ')

print("Donge Gathering Legacy Street Type")

# Change Environment to the correct gis database clean up..
env.workspace = "C:/Users/Noe956/Documents/GIS/HC_IT/GIS_DATA_Hidalgo.gdb"


feature_address_points = "Address_Points"

feature_road_centerlines = "Road_Centerlines"

fields_address_points = ['fullname', 'objectid', 'prd']

update_address_points = ['prd', 'objectid']


print("PARSING DIRTY DATA")

# prefixDirValuesDirtyAddressPoints = startPreDirProcess(feature_address_points, ['fullname', 'objectid', 'prd'])

# Get Road Name
roadNameDirty = startRoadNameProcess(feature_road_centerlines, ['objectid', 'fullname', 'PrefixDir', 'PrefixType'])
#['fullname', 'objectid', 'PrefixDir'])

print("done road name dirty")

#Get Only the ones that have single letter and prd is empty
#hasSingleLetter = [i for i in prefixDirValuesDirtyRoadCenterlines if i.hasStType()]

# get all the objects ids that specify the condition from hasSingleLetter..
allObjectsSingleLetter = str([i.getObjectId() for i in roadNameDirty]).replace("[", "(").replace("]", ")")

print(len(allObjectsSingleLetter))
print("STARTING THE PROCESS")

if len(allObjectsSingleLetter) == 2:
    sys.exit("No Objects Ids")

# Get all the rows that we need to update
with arcpy.da.UpdateCursor(feature_road_centerlines, ['StreetName', 'objectid'], where_clause="objectid in %s" % allObjectsSingleLetter) as cursor:
    #Loop through all the rows
    for row in cursor:
        #Search the prefixValue
        indexValue, roadValue = findRoadName(roadNameDirty, row[1])
        # if prefixvalue is not None
        if roadValue is not None and indexValue is not None:
            row[0] = roadValue
            cursor.updateRow(row) #finally update the row
            roadNameDirty.pop(indexValue)

print("Done Update Prefix")


