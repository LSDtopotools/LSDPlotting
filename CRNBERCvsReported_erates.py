# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 10:44:16 2015

@author: smudd
"""

import LSDOSystemTools as LSDost
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
import os
import numpy as np

def CRBERCvsReported_erates():

    Dirname = "C://basin_data//CosmoPaper//Results//Compiled//"
    #Fname = "Palumbo*_CompareResults.csv"
    
    SiteNames = []
    SiteDicts = []    
    
    # loop through the directory, getting the results from the data    
    for fname in glob(Dirname+"*_ErateComparison.csv"):
        
        # get only the file without the data directory
        NoDirFname = LSDost.GetFileNameNoPath(fname)
        
        # Now get the prefix of the file
        splitfname = NoDirFname.split('_ErateComparison.csv')
        fprefix = splitfname[0]

        print "File prefix is: " + fprefix 

        # add to the sitenames list and create a holding dictionary
        SiteNames.append(fprefix)
        thisdict = {}
        
        print "I am woking with the dataset: " + fprefix
        
        min_erate = 5
        max_erate = 100
    
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
                
            # now get the data into the dict
            for line in lines:
                this_line = LSDost.RemoveEscapeCharacters(line)
                split_line = this_line.split(',')
                
                #print split_line                
                
                BERC_erate.append(float(split_line[16]))
                BERC_uncert.append(float(split_line[17]))
                Report_erate.append(float(split_line[20]))
                Report_uncert.append(float(split_line[21])) 
                
                # get the maximum and minimum erosion rates
                if (float(split_line[16]) > max_erate):
                    max_erate = float(split_line[16])
                if (float(split_line[20]) > max_erate):
                    max_erate = float(split_line[20]) 
                                    
                if (float(split_line[16]) < min_erate):
                    min_erate = float(split_line[16])
                if (float(split_line[20]) < min_erate):
                    min_erate = float(split_line[20])                 

            thisdict["BERC_erate"] = BERC_erate
            thisdict["BERC_uncert"] = BERC_uncert
            thisdict["Report_erate"] = Report_erate
            thisdict["Report_uncert"] = Report_uncert                     
            SiteDicts.append(thisdict)  
            

    label_size = 18
    axis_size = 26

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size
    rcParams['xtick.major.size'] = 10    
    rcParams['ytick.major.size'] = 10    
    
    # make a line between the maximum and minimum erate
    one_line = np.linspace(min_erate,max_erate,1000)
        
    # now make plots based on these data
    Fig1 = plt.figure(1, facecolor='white',figsize=(10,7.5))  

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.1,left=0.1,right=0.95,top=0.95) 
    ax = Fig1.add_subplot(gs[5:100, 10:75])    


    cmap = plt.cm.jet   
    colo = 0 
    
    # plot the 1:1 line
    plt.plot(one_line,one_line,'k-',linewidth = 2.5)
    
    for index,thisdict in enumerate(SiteDicts):
        
        colo = colo + (1.000/len(SiteDicts))
        plt.plot(thisdict['BERC_erate'], thisdict['Report_erate'], "o", markersize=8, color=cmap(colo), label = SiteNames[index])
        plt.errorbar(thisdict['BERC_erate'], thisdict['Report_erate'], thisdict['BERC_uncert'], thisdict['Report_uncert'], fmt='o',color = cmap(colo), linewidth = 1.5)


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
            
    # logarithmic axes
    ax.set_yscale('log')
    ax.set_xscale('log')
            
    plt.xlabel('BERC erosion rate (mm/kyr)', fontsize = axis_size-6)
    plt.ylabel('Reported erosion rate (mm/kyr)', fontsize = axis_size-6) 
    handles, labels = ax.get_legend_handles_labels()    
    plt.legend(handles, labels, numpoints = 1, loc='lower right')

    #plt.show()       
    Fileformat = "svg"
    plt.savefig(Dirname+"BERC_vs_Reported_erates.svg",format = Fileformat)
    
        

if __name__ == "__main__":
    CRBERCvsReported_erates()         
    