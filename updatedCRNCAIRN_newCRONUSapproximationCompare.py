# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 13:44:32 2016

@author: smudd
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 06:38:37 2015

@author: smudd
"""

import os    
import numpy as np
import CRNResults as CRNR
import LSDOSystemTools as LSDost
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
        #from scipy.stats import gaussian_kde



def CollatenewCRONUScomparisonCRNData():
    
    #Directory = "C://code//git_papers//crn_basinwide_paper//Compiled_results//Brauch_vs_newCRONUS//"
    Directory = "T://Papers_LaTeX//crn_basinwide_paper//Compiled_results//Brauch_vs_newCRONUS//"
    Dirname = LSDost.ReformatSeperators(Directory)
    Dirname = LSDost.AppendSepToDirectoryPath(Dirname)
    
    Fileformat = 'svg'
    
    label_size = 8
    axis_size = 12

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size
    rcParams['xtick.major.size'] = 4    
    rcParams['ytick.major.size'] = 4
    rcParams['legend.fontsize'] = label_size
    rcParams['legend.handletextpad'] = 0.05
    rcParams['legend.labelspacing'] =0.1
    rcParams['legend.columnspacing'] =0.1 
    
    P_erate_newCRONUS = []
    D_erate_newCRONUS = []
    P_newCRONUS = []
    D_newCRONUS = []    
       
    # loop through the directory, getting the results from the data    
    for fname in glob(Dirname+"*_CRNResults.csv"):
         
        # get only the file without the data directory
        NoDirFname = LSDost.GetFileNameNoPath(fname)
        
        # Now get the prefix of the file
        splitfname = NoDirFname.split('_CRNResults.csv')
        fprefix = splitfname[0]
        
        print "File prefix is: " + fprefix 
        
        # now read in the data
        thisCRNData = CRNR.CRNResults(fname)        
        
        # Only get the newCRONUS dethier and Palumbo data
        # now get the prefixes
        if "Dethier" in fprefix:
            if "newCRONUS" in fprefix:
                D_erate_newCRONUS = thisCRNData.GetErosionRates_mmperkyr_rho2650() 
        elif "Palumbo" in fprefix:
            if "newCRONUS" in fprefix:
                P_erate_newCRONUS = thisCRNData.GetErosionRates_mmperkyr_rho2650() 
            
    # Convert the data to arrays (to calculate errors)
    P_nC_CAIRN = np.asarray(P_erate_newCRONUS) 
    D_nC_CAIRN = np.asarray(D_erate_newCRONUS) 
    
    #print "P CAIRN is: "
    #print P_nC_CAIRN

    #print "D CAIRN is: "
    #print D_nC_CAIRN    

    # Now get the CRONUScalc data  
    print "Entering second glob loop"
    for fname in glob(Dirname+"*.csv"):
        print "I found comparison data! Name is " + fname   
   
    # Now get the CRONUScalc data  
    print "Entering third glob loop"
    for fname in glob(Dirname+"*Comparison.csv*"):
        
        # get only the file without the data directory
        NoDirFname = LSDost.GetFileNameNoPath(fname)
        
        print "I found comparison data! Name is " + NoDirFname
        
        # Now get the prefix of the file
        splitfname = NoDirFname.split('_newCRONUSCAIRNComparison.csv')
        fprefix = splitfname[0]

        print "File prefix is: " + fprefix 

        print "I am woking with the dataset: " + fprefix



    
        #See if the parameter files exist
        if os.access(fname,os.F_OK):
            this_file = open(fname, 'r')
            lines = this_file.readlines()
            
            # get rid fo the first line
            lines.pop(0)
            
            # create the lists for populating with data
            CAIRN_erate = []
            CAIRN_uncert = [] 
            Report_erate = [] 
            Report_uncert = []
            newCRONUS_erate = [] 
            newCRONUS_uncert = []            
                
            # now get the data into the dict
            for line in lines:
                this_line = LSDost.RemoveEscapeCharacters(line)
                split_line = this_line.split(',')
                
                #print split_line[22]+" " +split_line[23]
                
                #print split_line                
                
                CAIRN_erate.append(float(split_line[16]))
                CAIRN_uncert.append(float(split_line[17]))
                Report_erate.append(float(split_line[20]))
                Report_uncert.append(float(split_line[21])) 
                newCRONUS_erate.append(float(split_line[22]))
                newCRONUS_uncert.append(float(split_line[23]))                 
                              

        # now get the prefixes
        if fprefix == "Dethier":
            D_newCRONUS = newCRONUS_erate
        elif fprefix == "Palumbo":
            P_newCRONUS = newCRONUS_erate

    #print "P_newCRONUS is: "
    #print  P_newCRONUS
    #print "D_newCRONUS is: "
    #print  D_newCRONUS

    P_nC = np.asarray(P_newCRONUS)
    D_nC = np.asarray(D_newCRONUS) 
    
    Perr = np.divide( np.subtract(P_nC_CAIRN,P_nC), P_nC)  
    Derr = np.divide( np.subtract(D_nC_CAIRN,D_nC), D_nC)  
    
    print "The errors are: "
    print Perr
    print Derr
    
    print P_nC
    print P_nC_CAIRN

    # okay, now you should have the errors    
            
    #===========================================================================    
    # now make plots based on these data
    # 3.26 inches = 83 mm, the size of a 1 column figure
    Fig1 = plt.figure(1, facecolor='white',figsize=(3.26,3.26))  

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.13,left=0.13,right=0.95,top=0.95) 
    ax = Fig1.add_subplot(gs[10:100,5:95])   
    
    ax.plot(P_nC,Perr,"o",markersize=5, color = "maroon", label = "Palumbo et al., 2010",markeredgewidth=1)
    ax.plot(D_nC,Derr,"ro",markersize=5, color = "lawngreen", label = "Dethier et al., 2014",markeredgewidth=1)

    ax.spines['top'].set_linewidth(1)
    ax.spines['left'].set_linewidth(1)
    ax.spines['right'].set_linewidth(1)
    ax.spines['bottom'].set_linewidth(1) 
    ax.tick_params(axis='both', width=1) 
    #ax.set_ylim([0.02,0.06])
    
    #plt.title('We are not using this in the paper!! Use CRNCAIRNvsnewCRONUS_erates.py instead!')
    plt.xlabel('$\epsilon_{CRCalc}$ (g cm$^{-2}$ yr$^{-1}$)', fontsize = axis_size)
    plt.ylabel('($\epsilon_{CAIRN-CRCalc}$-$\epsilon_{CRCalc}$)/$\epsilon_{CRCalc}$', fontsize = axis_size)
    #plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend()
    plt.legend(handles, labels, numpoints = 1, 
               loc=4, ncol=1, borderaxespad=1.)
        
    plt.savefig(Dirname+"CAIRN_newCRONUS_emulator.svg",format = Fileformat)
    
    #Fig1.show()


if __name__ == "__main__":
     CollatenewCRONUScomparisonCRNData() 