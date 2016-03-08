# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 16:53:22 2015

@author: smudd
"""

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats import gaussian_kde
from glob import glob
import LSDOSystemTools as LSDOst

# This function looks for all of the CRN_results files in a 
# directory DataDirectory
def GatherCRNResults(DataDirectory):
    
    data_prefixes = [] 
    CRNresults = []
    
    for FileName in glob(DataDirectory+"*CRNResults.csv"):
               
        # This gets the filename without the .csv
        file_prefix = LSDOst.GetFilePrefix(FileName)
       
        # Now get rid of the _CRNResults
        if file_prefix.endswith('_CRNResults'):
            file_prefix = file_prefix[:-11]
        else:
            print "You don't seem to have a CRNResults file"

        print "The file prefix is: " + file_prefix

        # Now you need to find all the sources in the makefile
        f = open(FileName,'r')  # open file
        lines = f.readlines()   # read in the data
        f.close()
        
        # get rid of the header
        del lines[0:4]
        
        erate_ours = []
        erate_ours_uncert = []
        erate_COSMOCALC = []
        shielding= []
        total_production = []
        
        theseCRNResults = {}
        
        for line in lines:
            split_line = line.split(',')
            
            erate_ours.append(float(split_line[7]))
            erate_ours_uncert.append(float(split_line[8]))
            erate_COSMOCALC.append(float(split_line[25]))
            shielding.append(float(split_line[16]))
            total_production.append(float(split_line[12]))
        

       
        theseCRNResults['erate_g_percm2_peryr'] = erate_ours
        theseCRNResults['total_uncert'] =erate_ours_uncert
        theseCRNResults['eff_erate_COSMOCALC'] = erate_COSMOCALC
        theseCRNResults['AverageShielding'] = shielding
        theseCRNResults['AvgProdScaling'] = total_production
        
        print "Erosion rates are: "
        print theseCRNResults['erate_g_percm2_peryr']
        
                
        
        data_prefixes.append(file_prefix)
        CRNresults.append(theseCRNResults)
        
    return data_prefixes, CRNresults          
       
# This function looks for all of the CRONUSResults files in a 
# directory DataDirectory
def GatherCRONUSResults(DataDirectory):
    
    data_prefixes = [] 
    CRONUSresults = []
    
    for FileName in glob(DataDirectory+"*CRONUSResults.csv"):
               
        # This gets the filename without the .csv
        file_prefix = LSDOst.GetFilePrefix(FileName)
       
        # Now get rid of the _CRNResults
        if file_prefix.endswith('_CRONUSResults'):
            file_prefix = file_prefix[:-14]
        else:
            print "You don't seem to have a CRONUSResults file"
    
        # okay, now load the data
        data = pandas.read_csv(FileName)
        
        data_prefixes.append(file_prefix)
        CRONUSresults.append(data)
        
    return data_prefixes, CRONUSresults          


