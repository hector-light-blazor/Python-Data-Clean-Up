import arcpy
class AddressParser:
    # init constructor
    def __init__(self, objectid, fullRoadName, fieldData):
        self.roadName = fullRoadName.strip()
        self.splitRoadArr = fullRoadName.split()
        self.splitLen = len(self.splitRoadArr)
        self.fieldData = fieldData.strip() if fieldData is not None else ""
        self.objectid = objectid
        self.hasData = len(self.roadName) > 1
        self.isEmpty = len(self.roadName) == 0
    
    def getField(self):
        return self.fieldData
    
    def getObjectId(self):
        return self.objectid
    
    def hasSingle(self):
        hasPrefix = ['N', 'S', 'E', 'W']
        return self.hasData and len(self.splitRoadArr[0]) == 1 and len(self.fieldData) == 0 and self.splitRoadArr[0] in hasPrefix
    
    def hasStType(self):
        return self.hasData and len(self.splitRoadArr[self.splitLen - 1]) >= 2 and len(self.fieldData) == 0
    
    def getIsEmpty(self):
        return self.isEmpty
    
    def getPrefixDir(self):
        if self.hasData and len(self.splitRoadArr[0]) == 1:
            return self.splitRoadArr[0]
    
    def getStType(self):
        if self.hasData and len(self.splitRoadArr[self.splitLen - 1]) >= 2:
            return self.splitRoadArr[self.splitLen - 1]
            
             

def test():
    hello = AddressParser("1", "none", None)
    print(hello.getField())

def processData(data):
    return AddressParser(data[1], data[0], data[2])


def findValue(arr, item):
    for i, val in enumerate(arr):
        if val.getObjectId() == item:
            return i, val.getStType()
    return None, None

def findTest():
    return None, None


def startProcess(fs, fields):
    prefixDirValuesDirty = [processData(row) for row in arcpy.da.SearchCursor(fs, fields)]
    return prefixDirValuesDirty
    
    
    