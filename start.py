import arcpy, sys
from arcpy import env
from bs4 import BeautifulSoup
from handler import *


gbReference = "C:/Users/Noe956/Documents/GIS/HC_IT/Downloads/GIS_DATA_Hidalgo.gdb"

#Setup the workspace we are going to find this data
env.workspace = gbReference

# setup some variables to specify the fields and feature class to grab information.
fields = ["OBJECTID", "PopupInfo"]
feature = "IrrigationDistrictEmergencyContacts"

# Grab data to parse the html string to grab the phone number
datas = getData(feature, fields)

# Collect the object ids in question for update
ids = str([i[0] for i in datas]).replace("[", "(").replace("]", ")")



# Remove the tuples into list
datas = [list(my_tuple) for my_tuple in datas]

for data in datas:
    soup = BeautifulSoup(data[1], 'html.parser') 
    table = soup.find('table')
    collection = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):
            row_data.append(cell.get_text())
        if row_data[0] == "OFFICE":
            collection.append(row_data)
    for col in collection:
        data[1] = col[1]

updateData(feature, "Phone", datas, ids)    

print("DONE SIR")
        
