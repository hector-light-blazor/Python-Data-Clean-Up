import arcpy, numpy

LegacyStreetType = []
directionalData = ['N', 'S', 'E', 'W']

class AddressParser:
    # init constructor
    def __init__(self, objectid, fullRoadName, preDir="", stType="", postDir=""):
        self.roadName = fullRoadName.strip()
        self.fullRoadName = ""
        self.splitRoadArr = fullRoadName.split()
        self.splitLen = len(self.splitRoadArr)
        self.lastPos  = self.splitLen - 1 if self.splitLen > 0 else 0
        self.preDir = preDir.strip() if preDir is not None else ""
        self.stType = stType.strip() if stType is not None else ""
        self.postDir = postDir.strip() if postDir is not None else ""
        self.objectid = objectid
        self.hasData = len(self.roadName) > 1
        self.isEmpty = len(self.roadName) == 0
        if self.splitLen > 0:
            self.processRoadParts()
    
    def processRoadParts(self):
        global directionalData
        global LegacyStreetType
        startPart = self.splitRoadArr[0]
        endPart = self.splitRoadArr[self.lastPos]
        firstPartFound = False
        secondPartFound = False
        if startPart in directionalData:
            self.preDir = startPart.strip()
            self.splitRoadArr.pop(0)
            firstPartFound = True
        
        if endPart in directionalData:
            self.postDir = endPart.strip()
            secondPartFound = True
            if firstPartFound:
                endIndex = len(self.splitRoadArr) - 1
                self.splitRoadArr.pop(endIndex)
            else:
                self.splitRoadArr.pop(self.lastPos)
        if secondPartFound == False:
            if endPart in LegacyStreetType:
                self.stType = endPart
                if firstPartFound:
                    endIndex = len(self.splitRoadArr) - 1
                    self.splitRoadArr.pop(endIndex)
                else:
                    self.splitRoadArr.pop(self.lastPos)
        else:
            lastIndex = len(self.splitRoadArr) - 1
            endPart = self.splitRoadArr[lastIndex]
            if endPart in LegacyStreetType:
                self.stType = endPart
                self.splitRoadArr.pop(lastIndex)
        for letter in self.splitRoadArr:
            self.fullRoadName += letter + " "
        self.fullRoadName = self.fullRoadName.strip()

    def getField(self):
        return self.fieldData
    
    def getObjectId(self):
        return self.objectid
    
    def getFullName(self):
        return self.fullRoadName
    
    def getStreetType(self):
        return self.stType
    
    def getPreDirect(self):
        return self.preDir
    
    def getPostDirect(self):
        return self.postDir
    
    def hasPreDir(self):
        global directionalData
        return self.hasData and len(self.splitRoadArr[0]) == 1 and self.splitRoadArr[0] in directionalData
    
    def hasPostDir(self):
        global directionalData
        return self.hasData and len(self.splitRoadArr[self.lastPos]) == 1 and self.splitRoadArr[self.lastPos] in directionalData
    
    def hasStType(self):
        global LegacyStreetType
        results = None
        found = None
        for parts in self.splitRoadArr:
            found = LegacyStreetType.index(parts) if parts in LegacyStreetType else None
            results = parts
        if results is not None:
            self.stType = results
            return True
        return False
        # for streetType in LegacyStreetType:
        #     if streetType in self.roadName:
        #         results = True
        #         self.stType = streetType
        #         break
        # return results
        #return self.hasData and  len(self.stType) == 0 and self.splitRoadArr[self.lastPos] in LegacyStreetType
    
    def getIsEmpty(self):
        return self.isEmpty
    
    def getPrefixDir(self):
        if self.hasData and len(self.splitRoadArr[0]) == 1:
            return self.splitRoadArr[0]
    
    def getStType(self):
        if self.hasData:
            return self.stType
        
    def getPostDir(self):
        if self.hasData:
            return self.splitRoadArr[self.lastPos]
        
    def getRoadName(self):
        results = ""
        if len(self.stType) > 0 and len(self.preDir) > 0 and len(self.postDir) > 0:
            start = 1
            end = self.splitLen - 2
            for index in range(start, end):
                results += self.splitRoadArr[index] + " "
        elif len(self.stType) > 0 and len(self.preDir) > 0:
            start = 1
            end = self.splitLen - 1
            for index in range(start, end):
                results += self.splitRoadArr[index] + " "
        elif len(self.preDir) > 0 and len(self.postDir) > 0:
            start = 1
            for index in range(start, self.lastPos):
                results += self.splitRoadArr[index] + " "
        elif len(self.preDir) == 0 and len(self.postDir) > 0:
            for index in range(self.lastPos):
                results += self.splitRoadArr[index] + " "
        elif len(self.stType) == 0 and len(self.preDir) == 0:
            start = 0
            end = self.splitLen
            for index in range(start, end):
                results += self.splitRoadArr[index] + " "
        elif len(self.preDir) == 0 and len(self.stType) > 0:
            for index in range(self.lastPos):
                results += self.splitRoadArr[index] + " "
        elif len(self.preDir) > 0 and len(self.stType) == 0:
            start = 1
            end = self.splitLen
            for index in range(start, end):
                results += self.splitRoadArr[index] + " "

        return results.strip()

def test():
    hello = AddressParser("1", "none", None)

def processPreDirData(data):
    return AddressParser(data[0], data[1], data[2], "")

def processPostDirData(data):
    return AddressParser(data[0],data[1], "", "", data[2])

def processStTypeData(data):
    return AddressParser(data[0], data[1],"", data[2])


def processRoadData(data):
    return AddressParser(data[0], data[1],data[2], data[3])

def processMainData(data):
    return AddressParser(data[0], data[1], "", "")

def findPreDirValue(arr, item):
    for i, val in enumerate(arr):
        if val.getObjectId() == item:
            return i, val.getPrefixDir()
    return None, None

def findStTypeValue(arr, item):
    for i, val in enumerate(arr):
        if val.getObjectId() == item:
            return i, val.getStType()
    return None, None

def findPostDirValue(arr, item):
    for i, val in enumerate(arr):
        if val.getObjectId() == item:
            return i, val.getPostDir()
    return None, None

def findRoadName(arr, item):
    for i, val in enumerate(arr):
        if val.getObjectId() == item:
            return i, val.getRoadName()
    return None, None

def findValues(arr, item):
    for i, val in enumerate(arr):
        if val.getObjectId() == item:
            return i, val.getFullName()
    return None, None

def findTest():
    return None, None


def grabObjectIds(data):
    allObjectsIdsForUpdate = str([i.getObjectId() for i in data]).replace("[", "(").replace("]", ")")
    return allObjectsIdsForUpdate
def mainProcess(fs, fields):
    dirtyValues = [processMainData(row) for row in arcpy.da.SearchCursor(fs, fields)]
    objectIdsForUpdate = grabObjectIds(dirtyValues)
    if len(objectIdsForUpdate) == 2:
        return "Nothing To Update Main Process"
    with arcpy.da.UpdateCursor(fs, ['PrefixDir','StreetName','StreetType', 'SuffixDirect', 'objectid'], where_clause="objectid in %s" % objectIdsForUpdate) as cursor:
        #Loop through all the rows
        for row in cursor:
            #Search the prefixValue
            indexValue, value = findValues(dirtyValues, row[4])
            # if prefixvalue is not None
            if value is not None and indexValue is not None:
                row[0] = dirtyValues[indexValue].getPreDirect()
                row[1] = dirtyValues[indexValue].getFullName()
                row[2] = dirtyValues[indexValue].getStType()
                row[3] = dirtyValues[indexValue].getPostDirect()
                cursor.updateRow(row) #finally update the row
                dirtyValues.pop(indexValue) # Remove from the list making it smaller
    return "Main Process Update Completed"

def startPreDirProcess(fs, fields):
    prefixDirValuesDirty = [processPreDirData(row) for row in arcpy.da.SearchCursor(fs, fields)]
    filterPreDirOnlyUpdates = [i for i in prefixDirValuesDirty if i.hasPreDir()]
    objectIdsForUpdate = grabObjectIds(filterPreDirOnlyUpdates)
    if len(objectIdsForUpdate) == 2:
        return "Nothing To Update Pre Dir"
    with arcpy.da.UpdateCursor(fs, ['PrefixDir', 'objectid'], where_clause="objectid in %s" % objectIdsForUpdate) as cursor:
        #Loop through all the rows
        for row in cursor:
            #Search the prefixValue
            indexValue, value = findPreDirValue(filterPreDirOnlyUpdates, row[1])
            # if prefixvalue is not None
            if value is not None and indexValue is not None:
                row[0] = value
                cursor.updateRow(row) #finally update the row
                filterPreDirOnlyUpdates.pop(indexValue) # Remove from the list making it smaller
    return "Pre Dir Update Completed"


def startPostDirProcess(fs, fields):
    postDirValuesDirty = [processPostDirData(row) for row in arcpy.da.SearchCursor(fs, fields)]
    filterPostDirOnlyUpdates = [i for i in postDirValuesDirty if i.hasPostDir()]
    objectIdsForUpdate = grabObjectIds(filterPostDirOnlyUpdates)
    if len(objectIdsForUpdate) == 2:
        return "Nothing To Update Post Dir"
    with arcpy.da.UpdateCursor(fs, ['SuffixDirect', 'objectid'], where_clause="objectid in %s" % objectIdsForUpdate) as cursor:
        #Loop through all the rows
        for row in cursor:
            #Search the post Dir Value
            indexValue, value = findPostDirValue(filterPostDirOnlyUpdates, row[1])
            # if prefixvalue is not None
            if value is not None and indexValue is not None:
                row[0] = value
                cursor.updateRow(row) #finally update the row
                filterPostDirOnlyUpdates.pop(indexValue) # Remove from the list making it smaller
    return "Post Dir Update Completed"

def startStTypeProcess(fs, fields):
    StreetTypeValuesDirty = [processStTypeData(row) for row in arcpy.da.SearchCursor(fs, fields)]
    filterStreetTypeOnlyValues = [i for i in StreetTypeValuesDirty if i.hasStType()]
    objectIdsForUpdate = grabObjectIds(filterStreetTypeOnlyValues)
    if len(objectIdsForUpdate) == 2:
        return "Nothing To Update Street Type"
    with arcpy.da.UpdateCursor(fs, ['StreetType', 'objectid'], where_clause="objectid in %s" % objectIdsForUpdate) as cursor:
        #Loop through all the rows
        for row in cursor:
            #Search the prefixValue
            indexValue, value = findStTypeValue(filterStreetTypeOnlyValues, row[1])
            # if prefixvalue is not None
            if value is not None and indexValue is not None:
                row[0] = value
                cursor.updateRow(row) #finally update the row
                filterStreetTypeOnlyValues.pop(indexValue) # Remove from the list making it smaller
    return "Street Type Completed"

def startRoadNameProcess(fs, fields):
    roadNames = [processRoadData(row) for row in arcpy.da.SearchCursor(fs, fields)]
    objectIdsForUpdate = grabObjectIds(roadNames)
    if len(objectIdsForUpdate) == 2:
        return "Nothing To Update Road Names"
    with arcpy.da.UpdateCursor(fs, ['StreetName', 'objectid'], where_clause="objectid in %s" % objectIdsForUpdate) as cursor:
        #Loop through all the rows
        for row in cursor:
            #Search the prefixValue
            indexValue, value = findRoadName(roadNames, row[1])
            # if prefixvalue is not None
            if value is not None and indexValue is not None:
                row[0] = value
                cursor.updateRow(row) #finally update the row
                roadNames.pop(indexValue) # Remove from the list making it smaller
    return "Road Name Completed"

def cleanData(data):
    if data is None:
        return ""
    elif len(data) > 0:
        data = data.strip()
    return data

def getLegacyData(fs, fields):
    LegacyStreetType = [row for row in arcpy.da.SearchCursor(fs, fields)]
    
def unique_values(table, field):  ##uses numpy
    global LegacyStreetType
    data = arcpy.da.TableToNumPyArray(table, [field])
    holdArr = numpy.unique(data[field])
    dataClean = [d for d in holdArr if len(d) > 0]
    LegacyStreetType = dataClean
    print(LegacyStreetType)

def getData(table, fields):
    htmls = [row for row in arcpy.da.SearchCursor(table, fields)]
    return htmls

def updateData(table, field, datas, objectIdsForUpdate):
    with arcpy.da.UpdateCursor(table, [field, 'OBJECTID'], where_clause="objectid in %s" % objectIdsForUpdate) as cursor:
        #Loop through all the rows
        for row in cursor:
            phone = [x[1] for x in datas if x[0] == row[1]]
            if len(phone) == 1:
                row[0] = phone[0]
                cursor.updateRow(row)
    return "Road Name Completed"
    
    
    