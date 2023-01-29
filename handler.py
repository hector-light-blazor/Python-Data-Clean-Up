import arcpy, numpy

LegacyStreetType = []

class AddressParser:
    # init constructor
    def __init__(self, objectid, fullRoadName, preDir="", preType=""):
        self.roadName = fullRoadName.strip()
        self.splitRoadArr = fullRoadName.split()
        self.splitLen = len(self.splitRoadArr)
        self.preDir = preDir.strip() if preDir is not None else ""
        self.preType = preType.strip() if preType is not None else ""
        self.objectid = objectid
        self.hasData = len(self.roadName) > 1
        self.isEmpty = len(self.roadName) == 0
    
    def getField(self):
        return self.fieldData
    
    def getObjectId(self):
        return self.objectid
    
    def hasSingle(self):
        hasPrefix = ['N', 'S', 'E', 'W']
        return self.hasData and len(self.splitRoadArr[0]) == 1 and len(self.preDir) == 0 and self.splitRoadArr[0] in hasPrefix
    
    def hasStType(self):
        global LegacyStreetType
        return self.hasData and  len(self.preType) == 0 and self.splitRoadArr[self.splitLen - 1] in LegacyStreetType
    
    def getIsEmpty(self):
        return self.isEmpty
    
    def getPrefixDir(self):
        if self.hasData and len(self.splitRoadArr[0]) == 1:
            return self.splitRoadArr[0]
    
    def getStType(self):
        if self.hasData:
            return self.splitRoadArr[self.splitLen - 1]
        
    def getRoadName(self):
        results = ""
        if len(self.preType) > 0 and len(self.preDir) > 0:
            start = 1
            end = self.splitLen - 1
            for index in range(start, end):
                results += self.splitRoadArr[index] + " "
        elif len(self.preType) == 0 and len(self.preDir) == 0:
            start = 0
            end = self.splitLen
            for index in range(start, end):
                results += self.splitRoadArr[index] + " "
        elif len(self.preDir) == 0 and len(self.preType) > 0:
            for index in range(self.splitLen - 1):
                results += self.splitRoadArr[index] + " "
        elif len(self.preDir) > 0 and len(self.preType) == 0:
            start = 1
            end = self.splitLen
            for index in range(start, end):
                results += self.splitRoadArr[index] + " "

        return results.strip()
                
            
             

def test():
    hello = AddressParser("1", "none", None)
    print(hello.getField())

def processPreDirData(data):
    return AddressParser(data[1], data[0], data[2], "")

def processPreTypeData(data):
    return AddressParser(data[1], data[0],"", data[2])


def processRoadData(data):
    return AddressParser(data[0], data[1],data[2], data[3])

def findValue(arr, item):
    for i, val in enumerate(arr):
        if val.getObjectId() == item:
            return i, val.getStType()
    return None, None

def findRoadName(arr, item):
    for i, val in enumerate(arr):
        if val.getObjectId() == item:
            return i, val.getRoadName()
    return None, None

def findTest():
    return None, None


def startPreDirProcess(fs, fields):
    prefixDirValuesDirty = [processPreDirData(row) for row in arcpy.da.SearchCursor(fs, fields)]
    return prefixDirValuesDirty


def startPreTypeProcess(fs, fields):
    prefixDirValuesDirty = [processPreTypeData(row) for row in arcpy.da.SearchCursor(fs, fields)]
    return prefixDirValuesDirty

def startRoadNameProcess(fs, fields):
    roadNames = [processRoadData(row) for row in arcpy.da.SearchCursor(fs, fields)]
    return roadNames

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
    
    
    
    