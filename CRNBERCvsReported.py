# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:45:24 2015

@author: smudd
"""

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
import os
        #from scipy.stats import gaussian_kde



def CRBERCvsReported():

    Dirname = "C://basin_data//CosmoPaper//Results//Compiled//"
    #Fname = "Palumbo*_CompareResults.csv"
    
    SiteNames = []
    SiteDicts = []    
    
    # loop through the directory, getting the results from the data    
    for fname in glob(Dirname+"*_CompareResults.csv"):
        
        # get only the file without the data directory
        NoDirFname = LSDost.GetFileNameNoPath(fname)
        
        # Now get the prefix of the file
        splitfname = NoDirFname.split('_CompareResults.csv')
        fprefix = splitfname[0]

        print "File prefix is: " + fprefix 

        # add to the sitenames list and create a holding dictionary
        SiteNames.append(fprefix)
        thisdict = {}
    
        #See if the parameter files exist
        if os.access(fname,os.F_OK):
            this_file = open(fname, 'r')
            lines = this_file.readlines()
            
            # get rid fo the first line
            lines.pop(0)
            
            # create the lists for populating with data
            BERC_erate = []
            BERC_uncert = [] 
            Report_erate = [] 
            Report_uncert = []
            BERC_shield = []
            Report_shield = []
                
            # now get the data into the dict
            for line in lines:
                this_line = LSDost.RemoveEscapeCharacters(line)
                split_line = this_line.split(',')
                BERC_erate.append(float(split_line[4]))
                BERC_uncert.append(float(split_line[5]))
                Report_erate.append(float(split_line[6]))
                Report_uncert.append(float(split_line[7])) 
                BERC_shield.append(float(split_line[2])) 
                Report_shield.append(float(split_line[3])) 
                
            thisdict["BERC_erate"] = BERC_erate
            thisdict["BERC_uncert"] = BERC_uncert
            thisdict["Report_erate"] = Report_erate
            thisdict["Report_uncert"] = Report_uncert
            thisdict["BERC_shield"] = BERC_shield
            thisdict["Report_shield"] = Report_shield                        
            SiteDicts.append(thisdict)  
            
    
    # This list will store the crn data
    CRNDataList = []  
    CRNprefixes = []
    
    label_size = 18
    axis_size = 26

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size
    rcParams['xtick.major.size'] = 10    
    rcParams['ytick.major.size'] = 10       
        
    # now make plots based on these data
    Fig1 = plt.figure(1, facecolor='white',figsize=(10,7.5))  

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.1,left=0.1,right=0.95,top=0.95) 
    ax = Fig1.add_subplot(gs[5:100, 10:75])    

   
    cmap = plt.cm.jet   
    colo = 0    
    
    for index,thisdict in enumerate(SiteDicts):
        
        colo = colo + (1.000/len(SiteDicts))
        plt.plot(thisdict['BERC_shield'], thisdict['Report_shield'], "o", markersize=8, color=cmap(colo), label = SiteNames[index])

    #plt.plot(self.CRNData['AvgProdScaling'],self.CRNData['Error_CR'],color=cmap(self.CRNData['basin_relief']),"o", markersize=8     )
    #plt.errorbar(datazz['erate_cosmocalc']*10, datazz['erate_cmperkyr']*10, xerr=datazz['error_cosmocalc'], yerr=datazz['error_newcode'], fmt='o',color = cmap(colo))  
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    
    # This gets all the ticks, and pads them away from the axis so that the corners don't overlap        
    ax.tick_params(axis='both', width=2.5, pad = 2)
    for tick in ax.xaxis.get_major_ticks():
            tick.set_pad(10)
    for tick in ax.yaxis.get_major_ticks():
            tick.set_pad(10)
            
    plt.xlabel('BERC topographic shielding', fontsize = axis_size-6)
    plt.ylabel('Reported topographic shielding', fontsize = axis_size-6) 
    handles, labels = ax.get_legend_handles_labels()    
    plt.legend(handles, labels, numpoints = 1, loc='lower right')
    plt.show()       
        

if __name__ == "__main__":
    CRBERCvsReported()         
    