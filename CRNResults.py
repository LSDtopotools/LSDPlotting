# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 20:53:44 2015

@author: smudd
"""

# This contains the CRNResults object, used for interpreting and plotting
# CRN data

import LSDOSystemTools as LSDOst
import os
import numpy as np

class CRNResults(object):

    # The constructor: it needs a filename to read    
    def __init__(self,FileName):
        
        # This gets the filename without the .csv
        file_prefix = LSDOst.GetFilePrefix(FileName)
        
        print "Loading a file, the file prefix is: " + file_prefix
        
        if file_prefix.endswith('_CRNResults'):
            file_prefix = file_prefix[:-11]           
            self.FilePrefix = file_prefix
        else:
            self.FilePrefix = 'NULL'

        print "The object file prefix is: " + self.FilePrefix
        
        #See if the parameter files exist
        if os.access(FileName,os.F_OK):
            this_file = open(FileName, 'r')
            lines = this_file.readlines()
            
            # get rid of the header
            del lines[0:3]
            
            # Now get a list with the names of the parameters
            self.VariableList = lines[0].split(',')
            
            # get rid of the names
            del lines[0]             
            
            # now you need to make a dict that contains a vist for each varaible name
            DataDict = {}  
            for name in self.VariableList:
                DataDict[name] = []
                
            # now get the data into the dict
            for line in lines:
                this_line = LSDOst.RemoveEscapeCharacters(line)
                split_line = this_line.split(',')
                
                for index,name in enumerate(self.VariableList):
                    if name == 'sample_name':
                        DataDict[name].append(split_line[index])
                    elif name == 'nuclide':
                        DataDict[name].append(split_line[index])
                    else:
                        DataDict[name].append(float(split_line[index]))
                    #print "Name is: " + name
                    
                #print "Finished assimilating Data Dict"
          
            self.CRNData = DataDict
        else:
            self.VariableList = []
            self.CRNData = {}


    # This gets errors between the various outputs
    def GetErrorsBetweenMethods(self):
        ErateLSD = self.CRNData['erate_g_percm2_peryr']
        ErateCOSMOCALC = self.CRNData['eff_erate_COSMOCALC'] 
        ErateCRONUSlike = self.CRNData['eff_erate_COSMOCALC_emulating_CRONUS']
        
        # get the errors (as a fraction of the erosion rate)
        diffCC = np.subtract(ErateLSD,ErateCOSMOCALC)
        #diffCC = np.abs(diffCC)
        ErrorCC = np.subtract(diffCC,ErateLSD)
        
        diffCR = np.subtract(ErateLSD,ErateCRONUSlike)
        ErrorCR = np.subtract(diffCR,ErateLSD)
        
        return ErrorCC, ErrorCR
        


    def GetParameterNames(self,PrintToScreen = False):
        
        if PrintToScreen:        
            print self.VariableList
            
        return self.VariableList 

    def GetErosionRates(self,PrintToScreen = False):
        ERate = self.CRNData['erate_g_percm2_peryr']
        
        if PrintToScreen:
            print ERate
        return ERate

    def GetErosionRatesUncert(self,PrintToScreen = False):
        ERateU = self.CRNData['total_uncert']
        
        if PrintToScreen:
            print ERateU
        return ERateU

    def GetSampleName(self,PrintToScreen = False):
        SampleName = self.CRNData['sample_name']
        
        if PrintToScreen:
            print SampleName
        return SampleName

    def GetNuclide(self,PrintToScreen = False):
        Nuclide = self.CRNData['nuclide']
        
        if PrintToScreen:
            print Nuclide
        return Nuclide

    def GetLatitude(self,PrintToScreen = False):
        Latitude = self.CRNData['latitude'] 
        
        if PrintToScreen:
            print Latitude
        return Latitude

    def GetLongitude(self,PrintToScreen = False):
        Longitude = self.CRNData['longitude'] 
        
        if PrintToScreen:
            print Longitude
        return Longitude
        

    def TraslateToReducedShapefile(self,FileName):
        # Parse a delimited text file of volcano data and create a shapefile

        import osgeo.ogr as ogr
        import osgeo.osr as osr


        #  set up the shapefile driver
        driver = ogr.GetDriverByName("ESRI Shapefile")

        # Get the path to the file
        this_path = LSDOst.GetPath(FileName)
        DataName = self.FilePrefix
        
        FileOut = this_path+DataName+".shp"
        
        print "The filename will be: " + FileOut

        # delete the existing file
        if os.path.exists(FileOut):
            driver.DeleteDataSource(FileOut)

        # create the data source
        data_source = driver.CreateDataSource(FileOut)
        
        # create the spatial reference, WGS84
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)

        print "Creating the layer"

        # create the layer
        layer = data_source.CreateLayer("CRNData", srs, ogr.wkbPoint)

        print "Adding the field names"

        # Add the fields we're interested in
        field_name = ogr.FieldDefn("SampleName", ogr.OFTString)
        field_name.SetWidth(24)
        layer.CreateField(field_name)
        field_region = ogr.FieldDefn("Nuclide", ogr.OFTString)
        field_region.SetWidth(24)
        layer.CreateField(field_region)
        layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("EffERate", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("EffERateU", ogr.OFTReal))

        sample_name = self.GetSampleName()
        nuclide = self.GetNuclide()
        Latitude = self.GetLatitude()
        Longitude = self.GetLongitude()
        ERateU = self.GetErosionRatesUncert()
        ERate = self.GetErosionRates()
        
        print "lengths are: "
        print "SN: " + str(len(sample_name))
        print "N: " + str(len(Latitude))
        print "Lat: " + str(len(nuclide))
        print "Long: " + str(len(Longitude))
        print "Erate: " + str(len(ERate))
        print "ErateU: " + str(len(ERateU))
        
        # Process the text file and add the attributes and features to the shapefile
        for index,name in enumerate(sample_name):
            
            # create the feature
            feature = ogr.Feature(layer.GetLayerDefn())
            
            # Set the attributes using the values from the delimited text file
            feature.SetField("SampleName", name)
            feature.SetField("Nuclide", nuclide[index])
            feature.SetField("Latitude", Latitude[index])
            feature.SetField("Longitude", Longitude[index])
            feature.SetField("EffERate", ERate[index])
            feature.SetField("EffERateU", ERateU[index])

            # create the WKT for the feature using Python string formatting
            wkt = "POINT(%f %f)" %  (float(Longitude[index]), float(Latitude[index]))

            # Create the point from the Well Known Txt
            point = ogr.CreateGeometryFromWkt(wkt)

            # Set the feature geometry using the point
            feature.SetGeometry(point)
            # Create the feature in the layer (shapefile)
            layer.CreateFeature(feature)
            # Destroy the feature to free resources
            feature.Destroy()

        # Destroy the data source to free resources
        data_source.Destroy()

    def TraslateToReducedGeoJSON(self,FileName):
        # Parse a delimited text file of volcano data and create a shapefile

        import osgeo.ogr as ogr
        import osgeo.osr as osr


        #  set up the shapefile driver
        driver = ogr.GetDriverByName("GeoJSON")

        # Get the path to the file
        this_path = LSDOst.GetPath(FileName)
        DataName = self.FilePrefix
        
        FileOut = this_path+DataName+".geojson"
        
        print "The filename will be: " + FileOut

        # delete the existing file
        if os.path.exists(FileOut):
            driver.DeleteDataSource(FileOut)

        # create the data source
        data_source = driver.CreateDataSource(FileOut)
        
        # create the spatial reference, WGS84
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)

        print "Creating the layer"

        # create the layer
        layer = data_source.CreateLayer("CRNData", srs, ogr.wkbPoint)

        print "Adding the field names"

        # Add the fields we're interested in
        field_name = ogr.FieldDefn("SampleName", ogr.OFTString)
        field_name.SetWidth(48)
        layer.CreateField(field_name)
        field_region = ogr.FieldDefn("Nuclide", ogr.OFTString)
        field_region.SetWidth(48)
        layer.CreateField(field_region)
        layer.CreateField(ogr.FieldDefn("Latitude", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("Longitude", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("EffERate", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("EffERateU", ogr.OFTReal))

        sample_name = self.GetSampleName()
        nuclide = self.GetNuclide()
        Latitude = self.GetLatitude()
        Longitude = self.GetLongitude()
        ERateU = self.GetErosionRatesUncert()
        ERate = self.GetErosionRates()
        
        print "lengths are: "
        print "SN: " + str(len(sample_name))
        print "N: " + str(len(Latitude))
        print "Lat: " + str(len(nuclide))
        print "Long: " + str(len(Longitude))
        print "Erate: " + str(len(ERate))
        print "ErateU: " + str(len(ERateU))
        
        # Process the text file and add the attributes and features to the shapefile
        for index,name in enumerate(sample_name):
            
            # create the feature
            feature = ogr.Feature(layer.GetLayerDefn())
            
            # Set the attributes using the values from the delimited text file
            feature.SetField("SampleName", name)
            feature.SetField("Nuclide", nuclide[index])
            feature.SetField("Latitude", Latitude[index])
            feature.SetField("Longitude", Longitude[index])
            feature.SetField("EffERate", ERate[index])
            feature.SetField("EffERateU", ERateU[index])

            # create the WKT for the feature using Python string formatting
            wkt = "POINT(%f %f)" %  (float(Longitude[index]), float(Latitude[index]))

            # Create the point from the Well Known Txt
            point = ogr.CreateGeometryFromWkt(wkt)

            # Set the feature geometry using the point
            feature.SetGeometry(point)
            # Create the feature in the layer (shapefile)
            layer.CreateFeature(feature)
            # Destroy the feature to free resources
            feature.Destroy()

        # Destroy the data source to free resources
        data_source.Destroy()

                