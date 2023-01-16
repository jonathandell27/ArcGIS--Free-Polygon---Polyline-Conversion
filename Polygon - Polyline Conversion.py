import json
import arcpy
import os
import shutil
import time
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
arcpy.AddMessage("start time = {}".format(current_time))

arcpy.AddMessage("All rights reserved to Jonathan Dell!")

username = os.getlogin()
arcpy.AddMessage("Hello {}!".format(username))
arcpy.AddMessage("Starting the process")

# set environment - current ToolBox
currentDirectory = os.getcwd()

#The input layer - must be Polygon or Polyline type
Layer = arcpy.GetParameter(0)

#Output layer - select the file location and file name
newlayer = arcpy.GetParameter(1)

#json1 - the Json file to be converted from the input layer.
#json2 - The Json file after changing the geometry settings.
json1 = r"{}\Layer1.json".format(currentDirectory)
json2 =  r"{}\Layer2.json".format(currentDirectory)


#Convert the input layer to a Json file
arcpy.conversion.FeaturesToJSON(Layer, json1, "FORMATTED")

#Opens the Json files for editing
jfile1 = open(json1,"r+",encoding= "UTF-8")
jfile2 = open(json2,"w",encoding= "UTF-8")

json_object = json.load(jfile1)

#Converts the text from the Json file to a string format
jsonstr = json.dumps(json_object, ensure_ascii=False)


Polygontype = "esriGeometryPolygon"    #Polygon Geometry type (from the Json settings)
Polygonver = "rings"                   #Polygon attributes Geometry type (from the Json settings)
Polylinetype = "esriGeometryPolyline"  #Polyline Geometry type (from the Json settings)
Polylinever ="paths"                   #Polyline attributes Geometry type (from the Json settings)


#Function - change the geometry settings in Json1 file and save it to Json2 file.
def replaceGeometry(x,y,p,r):
    newstring = jsonstr.replace(x,y)
    newstring = newstring.replace(p,r)
    jfile2.write(newstring) #Writing to Json2 file
    jfile2.close() #Turns off the file editing mode

#Identify if the input layer is polygon and change the geometry settings to Polyline layer using the "replaceGeometry" function
if Polygontype in jsonstr:
    arcpy.AddMessage("Input Layer type - polygon")
    arcpy.AddMessage("convert to Polyline type")
    replaceGeometry(Polygontype, Polylinetype, Polygonver, Polylinever)

#Identify if the input layer is Polyline and change the geometry settings to polygon layer using the "replaceGeometry" function
elif Polylinetype in jsonstr:
    arcpy.AddMessage("Input Layer type - Polyline")
    arcpy.AddMessage("convert to polygon type")
    replaceGeometry(Polylinetype, Polygontype, Polylinever, Polygonver)

#Turns off the file editing mode
jfile1.close()

#Convert Json2 to features class a file According to the location the name that defined by the user
arcpy.conversion.JSONToFeatures(json2, r'{}'.format(newlayer))

#Deletes the 2 Json files
os.unlink(json1)
os.unlink(json2)

arcpy.AddMessage("Done!")
end = datetime.now()
End_time = end.strftime("%H:%M:%S")
arcpy.AddMessage("End time = {}".format(End_time))

