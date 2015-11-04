# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 20:53:44 2015

@author: smudd
"""

import LSDOSystemTools as LSDOst
import os

class CRNResults(object):

    # The constructor: it needs a filename to read    
    def __init__(self,FileName):
        
        # This gets the filename without the .csv
        file_prefix = LSDOst.GetFilePrefix(FileName)
        
        if file_prefix.endswith('_CRONUSResults'):
            file_prefix = file_prefix[:-14]           
            self.FilePrefix = file_prefix
        else:
            self.FilePrefix = 'NULL'

        
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
                
                # the first two elements are strings
                DataDict[self.VariableList[0]].append(split_line[0])
                DataDict[self.VariableList[1]].append(split_line[1])
                
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



    def GetParameterNames(self,PrintToScreen = False):
        
        if PrintToScreen:        
            print self.VariableList
            
        return self.VariableList 

    def GetErosionRates(self,PrintToScreen = False):
        ERate = self.CRNData['erate_g_percm2_peryr']
        
        if PrintToScreen:
            print ERate
        return ERate
        
        