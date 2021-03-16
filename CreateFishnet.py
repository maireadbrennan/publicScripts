"""
THIS SCRIPT CREATES A 200mX200m FISHNET GRID OVER AN INPUT SHAPEFILE
To create an ArcToolbox tool with which to execute this script, do the following.
1 In ArcMap > Catalog > Toolboxes > My Toolboxes, either select an existing toolbox
or right-click on My Toolboxes and use New > Toolbox to create (then rename) a new one.
2 Drag (or use ArcToolbox > Add Toolbox to add) this toolbox to ArcToolbox.
3 Right-click on the toolbox in ArcToolbox, and use Add > Script to open a dialog box.
4 In this Add Script dialog box, use Label to name the tool being created, and press Next.
5 In a new dialog box, browse to the .py file to be invoked by this tool, and press Next.
6 In the next dialog box, specify the following inputs (using dropdown menus wherever possible)
before pressing OK or Finish.
DISPLAY NAME            DATA TYPE           PROPERTY>DIRECTION>VALUE            PROPERTY>DIRECTION>OBTAINEDFROM
Input                   Feature Layer               Input
7 To later revise any of this, right-click to the tool's name and select Properties.
"""
# Import necessary modules
import sys, os, string, math, arcpy, traceback
# Set the environment for all outputs generated in the script not asking for user input
arcpy.env.workspace = 'C:\Users\mb2252\Desktop\GEOSPATIALFINAL'
# Allow output file to overwrite any existing file of the same name
arcpy.env.overwriteOutput = True

try:
    # MAKE SURE YOU ARE IN A PROJECTED COORDINATE SYSTEM!
    # Gather and name input layer
    nameOfInputFeatureLayer = arcpy.GetParameterAsText(0)
    arcpy.AddMessage("The input layer is" + nameOfInputFeatureLayer)

    # Create a fishnet grid for Baltimore
    out_feature_class = "Baltimore_fishnet.shp"
    out_feature_class_clip = "Baltimore_fishnet_clip.shp"
    templateExtent = nameOfInputFeatureLayer
    describe = arcpy.Describe(templateExtent)
    arcpy.CreateFishnet_management(out_feature_class, str(describe.extent.lowerLeft),
                                   str(describe.extent.XMin) + " " + str(describe.extent.YMax + 10),"200", "200", "","",
                                   str(describe.extent.upperRight), "LABELS",templateExtent,"POLYGON")

    arcpy.AddMessage('\n' + "The origin_coord is " + str(describe.extent.lowerLeft))
    arcpy.AddMessage('\n' + "The y_axis_coord is " + str(describe.extent.XMin) + " " +str(describe.extent.YMax + 10))
    arcpy.AddMessage('\n' + "The cell_width is 200 and the cell_height is 200")
    arcpy.AddMessage('\n' + "The corner_coord is " +str(describe.extent.upperRight))
    
    # Calculating Geometry of a shapefile and outputs it
    arcpy.AddMessage('\n' + "The input feature layer name is " + out_feature_class_clip)

    arcpy.Clip_analysis(out_feature_class, templateExtent,out_feature_class_clip,"")
    
    # Request user input of data type = Shapefile and direction = Output
    nameOfOutputShapefile = "geometry_fishnet.shp"
    arcpy.AddMessage("The output shapefile name is " + nameOfOutputShapefile + "\n")

    # Replicate the input shapefile and add a new field to the replica
    arcpy.CopyFeatures_management(out_feature_class_clip, nameOfOutputShapefile)

    arcpy.AddField_management(nameOfOutputShapefile, "ShapeType", "TEXT", 10)
    arcpy.CalculateField_management(nameOfOutputShapefile,"ShapeType","!shape.type!","PYTHON_9.3")
 
    arcpy.AddField_management(nameOfOutputShapefile, "Parts",  "INTEGER", 10)
    arcpy.CalculateField_management(nameOfOutputShapefile,"Parts","!shape.partCount!","PYTHON_9.3")
        
    arcpy.AddField_management(nameOfOutputShapefile, "SqMeters", "DOUBLE", 20, 5)
    arcpy.CalculateField_management(nameOfOutputShapefile,"SqMeters","!shape.area@squaremeters!","PYTHON_9.3")
        
    arcpy.AddField_management(nameOfOutputShapefile, "Meters", "DOUBLE", 20, 5)
    arcpy.CalculateField_management(nameOfOutputShapefile,"Meters","!shape.length@meters!","PYTHON_9.3")

    # Add fishnet to the map! 
    # Get the map document
    mxd = arcpy.mapping.MapDocument("CURRENT")
    # Get the data frame
    df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
    # Create a new layer
    newlayer = arcpy.mapping.Layer(out_feature_class)
    # add the layer to the map at the top of the table of contents in the current data frame (0)
    arcpy.mapping.AddLayer(df, newlayer,"TOP")

except Exception as e:
    # If unsuccessful, end gracefully by indicating why
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message)
    # ... and where
    exceptionreport = sys.exc_info()[2]
    fullermessage = traceback.format_tb(exceptionreport)[0]
    arcpy.AddError("at this location: \n\n" + fullermessage + "\n")
