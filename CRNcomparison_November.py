# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 06:38:37 2015

@author: smudd
"""

import CRNResults as CRNR
import LSDOSystemTools as LSDost
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
        #from scipy.stats import gaussian_kde



def CollateCRNData():

    Directory = "C://basin_data//CosmoPaper//Results//Compiled//"
    Dirname = LSDost.ReformatSeperators(Directory)
    Dirname = LSDost.AppendSepToDirectoryPath(Dirname)
    
    # This list will store the crn data
    CRNDataList = []  
    CRNprefixes = []
    
    label_size = 18
    axis_size = 26

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size
       
    # loop through the directory, getting the results from the data    
    for fname in glob(Dirname+"*_CRNResults.csv"):
        
        # get only the file without the data directory
        NoDirFname = LSDost.GetFileNameNoPath(fname)
        
        # Now get the prefix of the file
        splitfname = NoDirFname.split('_CRNResults.csv')
        fprefix = splitfname[0]
        
        # now produce the cronus name from this prefix
        CRONUS_name = Dirname+fprefix+"_CRONUS.csv"
        
        print "File prefix is: " + fprefix 
        print "Cronus_name is: " + CRONUS_name
        
        # now read in the data
        thisCRNData = CRNR.CRNResults(fname)        

        # read in the Cronus data and get the errors
        thisCRNData.ReadCRONUSData(CRONUS_name)
        thisCRNData.GetErrorsBetweenMethods()
        thisCRNData.GetErrorsBetweenCRONUS()
        
        CRNDataList.append(thisCRNData)
        CRNprefixes.append(fprefix)
        
    # now make plots based on these data
    Fig1 = plt.figure(1, facecolor='white',figsize=(10,7.5))  

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.1,left=0.1,right=0.95,top=0.95) 
    
    for index,CRNObj in enumerate( CRNDataList):
        plt.plot(self.CRNData['erate_g_percm2_peryr'],self.CRNData['Error_CR'],
                    c=self.CRNData['basin_relief'], s=50, edgecolor='', 
                    cmap=plt.get_cmap("autumn_r"))
        
        
        
    
        
    
        
    
        
        
        

if __name__ == "__main__":
    CollateCRNData() 