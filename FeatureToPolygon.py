"""
THIS SCRIPT CONVERTS ALL THE SHAPEFILES IN A FOLDER INTO POLYGON 

To create an ArcToolbox tool with which to execute this script, do the following.
1   In  ArcMap > Catalog > Toolboxes > My Toolboxes, either select an existing toolbox
    or right-click on My Toolboxes and use New > Toolbox to create (then rename) a new one.
2   Drag (or use ArcToolbox > Add Toolbox to add) this toolbox to ArcToolbox.
3   Right-click on the toolbox in ArcToolbox, and use Add > Script to open a dialog box.
4   In this Add Script dialog box, use Label to name the tool being created, and press Next.
5   In a new dialog box, browse to the .py file to be invoked by this tool, and press Next.
6   In the next dialog box, specify the following input (using dropdown menus wherever possible)
    before pressing the Finish button.
        DISPLAY NAME        DATA TYPE    
        Which Folder?       Folder
7   To later revise any of this, right-click to the tool's name and select Properties.  
"""

try:
    
    # Import necessary modules
    import sys, os, string, math, arcpy, traceback
    
    # Request user input of data type = Folder
    nameOfFolder            = sys.argv[1]

    # Override previous output
    arcpy.env.overwriteOutput = True

    # Designate that folder as the current workspace
    arcpy.env.workspace     = nameOfFolder

    # Echo the name of the current workspace
    #arcpy.AddMessage('\n' + "Below are the shapefiles in " + nameOfFolder)

    # Create a list of all shapefile names in the workspace
    listOfShapefileNames    = arcpy.ListFeatureClasses()

    # Execute CopyFeatures for each input shapefile
    for nextShapefile in listOfShapefileNames:
        nameOfOutputShapefile = "c72_Line_Polygon_" + nextShapefile[13:]
        arcpy.AddMessage("    Creating " + nameOfOutputShapefile)
        # Use the FeatureToPolygon function to form new areas
        arcpy.FeatureToPolygon_management(nextShapefile, nameOfOutputShapefile)
        
        # Add a layer for that new shapefile to the active data frame (which is necessary because 
        # there was no user-specified output shapefile with its DIRECTION set to OUTPUT)
        currentMap          = arcpy.mapping.MapDocument("CURRENT")
        currentDataFrame    = currentMap.activeDataFrame
        layerToBeDisplayed  = arcpy.mapping.Layer(nameOfOutputShapefile)
        arcpy.mapping.AddLayer(currentDataFrame, layerToBeDisplayed,"TOP")
        del currentMap

    # Add a blank line at the bottom of the printed list      
    arcpy.AddMessage('\n')

except Exception as e:
    # If unsuccessful, end gracefully by indicating why
    arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
    # ... and where
    exceptionreport = sys.exc_info()[2]
    fullermessage   = traceback.format_tb(exceptionreport)[0]
    arcpy.AddError("at this location: \n\n" + fullermessage + "\n")
