import arcpy
from arcpy import env
from handler import *



env.workspace = "C:/Users/Noe956/Documents/GIS/HC_IT/GIS_DATA_Hidalgo.gdb"


feature_address_points = "Address_Points";

feature_road_centerlines = "Road_Centerlines";

fields_address_points = ['fullname', 'objectid', 'prd']

update_address_points = ['prd', 'objectid']


print("PARSING DIRTY DATA")
test()
# prefixDirValuesDirtyAddressPoints = startProcess(feature_address_points, ['fullname', 'objectid', 'prd'])

prefixDirValuesDirtyRoadCenterlines = startProcess(feature_road_centerlines, ['fullname', 'objectid', 'PrefixType'])
#['fullname', 'objectid', 'PrefixDir'])

#Get Only the ones that have single letter and prd is empty
hasSingleLetter = [i for i in prefixDirValuesDirtyRoadCenterlines if i.hasStType()]

# get all the objects ids that specify the condition from hasSingleLetter..
allObjectsSingleLetter = str([i.getObjectId() for i in hasSingleLetter]).replace("[", "(").replace("]", ")")

print(len(hasSingleLetter))
print(len(allObjectsSingleLetter))
print("STARTING THE PROCESS")
# Get all the rows that we need to update
with arcpy.da.UpdateCursor(feature_road_centerlines, ['PrefixType', 'objectid'], where_clause="objectid in %s" % allObjectsSingleLetter) as cursor:
    #Loop through all the rows
    for row in cursor:
        #Search the prefixValue
        indexValue, prefixValue = findValue(hasSingleLetter, row[1])
        # if prefixvalue is not None
        if prefixValue is not None and indexValue is not None:
            row[0] = prefixValue
            cursor.updateRow(row) #finally update the row
            hasSingleLetter.pop(indexValue)

print("Done Update Prefix")


