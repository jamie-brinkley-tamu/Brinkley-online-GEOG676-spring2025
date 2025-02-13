# -*- coding: utf-8 -*-

import time
import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "graduatedcolor"
        self.description = "Create a graduated color map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        """Define the tool parameters."""
        # Original project name
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )

        # Which layer you want to classify to create a color map
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayertoClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
         )    

        # Output folder location
        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            direction="Input"
         )
        
        # Output project name
        param3 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
         )
        params = [param0, param1, param2, param3] 
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Define Progressor Variables
        readTime = 3 # The time for users to read the progress
        start = 0 # Beginning position of the progressor
        max = 100 # End position
        step = 33 # The progress interval to move the progressor along

        # Setup Progressor
        arcpy.SetProgressor("step", "Validating Project File...", start, max, step)
        time.sleep(readTime) # Pause the execution for 3 seconds
        # Add Message to the Results Pane
        arcpy.AddMessage("Validating Project File...")

        # Project File
        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText) # Param 0 is the input project file

        # Grabs the First Instance of a map from the .aprx
        campus = project.listMaps('Map')[0] # Access to the first map

        # Increment Progressor
        arcpy.SetProgressorPosition(start + step) # Now is 33% completed
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        # Loop throught he layers of the map
        for layer in campus.listLayers():
            # Check if the layer is a Feature Layer
            if layer.isFeatureLayer:
                # Copy the layer's Symbology
                symbology = layer.symbology
                # Make sure the symbology has renderer attribute
                if hasattr(symbology, 'renderer'):
                    # Check Layer Name
                    if layer.name == parameters[1].valueAsText: # Check if the layer name matches the input layer

                        # Increment Progressor
                        arcpy.SetProgressorPosition(start + step*2) # Now is 66% completed
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and classifying...")

                        # Update the Copy's Renderer to "Graduated Colors Renderer"
                        symbology.updateRenderer('GraduatedColorsRenderer')

                        # Tell arcpy which field we want to base our chloropleth off of
                        symbology.renderer.classificationField = "Shape_Area"

                        # Set how many classes we'll have for the map
                        symbology.renderer.breakCount = 5

                        # Set Color Ramp
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 classes)')[0]

                        # Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")
                    else:
                        print("No layers found")

        # Increment Progressor
        arcpy.SetProgressorPosition(start + step*3) # Now is 99% completed
        arcpy.SetProgressorLabel("Saving...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        project.saveACopy(parameters[2].valueAsText + "\\" + parameters[3].valueAsText + ".aprx")
        # Param 2 is the folder location and param 3 is the name of the new project
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return