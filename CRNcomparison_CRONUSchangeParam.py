# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 11:19:46 2016

@author: smudd
"""

    
import numpy as np
import CRNResults as CRNR
import LSDOSystemTools as LSDost
from glob import glob
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.gridspec import GridSpec
        #from scipy.stats import gaussian_kde



def CRONUS_diff_params():
    
    #Directory = "C://basin_data//CosmoPaper//Results//Compiled//"
    Directory = "T://Papers_LaTeX//crn_basinwide_paper//Compiled_results//"
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

    fname = Dirname+"Scherler_CRNResults.csv"

    # get only the file without the data directory
    NoDirFname = LSDost.GetFileNameNoPath(fname)
        
    # Now get the prefix of the file
    splitfname = NoDirFname.split('_CRNResults.csv')
    fprefix = splitfname[0]
        
    # now produce the cronus name from this prefix
    CRONUS_name1 = Dirname+fprefix+"_CRONUSEmulator.csv"
    CRONUS_name2 = Dirname+fprefix+"_CRONUSEmulator_Modified.csv"
    CRONUS_name3 = Dirname+fprefix+"_CRONUSEmulator_Modified2.csv"
            
    print "File prefix is: " + fprefix 
    print "Cronus_name is: " + CRONUS_name1
        
    # now read in the data. We need 3 objects for 3 different results
    thisCRNData1 = CRNR.CRNResults(fname)
    thisCRNData2 = CRNR.CRNResults(fname)
    thisCRNData3 = CRNR.CRNResults(fname)
       
     # read in the Cronus data and get the errors
    thisCRNData1.ReadCRONUSData(CRONUS_name1)
    thisCRNData1.GetErrorsBetweenMethods()
    thisCRNData1.GetErrorsBetweenCRONUS()

    thisCRNData2.ReadCRONUSData(CRONUS_name2)
    thisCRNData2.GetErrorsBetweenMethods()
    thisCRNData2.GetErrorsBetweenCRONUS()

    thisCRNData3.ReadCRONUSData(CRONUS_name3)
    thisCRNData3.GetErrorsBetweenMethods()
    thisCRNData3.GetErrorsBetweenCRONUS()           
            
    #===========================================================================    
    # now make plots based on these data
    # 3.26 inches = 83 mm, the size of a 1 column figure
    Fig1 = plt.figure(1, facecolor='white',figsize=(3.26,3.26))  

    # generate a 120,90 grid. 
    # gendepth a grid. 
    gs = GridSpec(100,100,bottom=0.06,left=0.1,right=1.0,top=1.0) 
    ax = Fig1.add_subplot(gs[10:90,10:95])  
    
    ax.plot(thisCRNData1.GetAverageCombinedScaling(),thisCRNData1.GetError_CR(), "o",
                markersize=4, color="black", label = "CRONUS2.2 default",markeredgewidth=1)
    ax.plot(thisCRNData2.GetAverageCombinedScaling(),thisCRNData2.GetError_CR(), "o",
                markersize=4, color="grey", label = "Updated spallation",markeredgewidth=1)                
    ax.plot(thisCRNData3.GetAverageCombinedScaling(),thisCRNData3.GetError_CR(), "o",
                markersize=4, color="white", label = "Updated spallation, muons",markeredgewidth=1)    
    

    ax.spines['top'].set_linewidth(1)
    ax.spines['left'].set_linewidth(1)
    ax.spines['right'].set_linewidth(1)
    ax.spines['bottom'].set_linewidth(1) 
    ax.tick_params(axis='both', width=1) 
       
    plt.xlabel('Production factor ($S_{tot}$)', fontsize = axis_size)
    plt.ylabel('($\epsilon_{CR2.2}$-$\epsilon_{CAIRN}$)/$\epsilon_{CAIRN}$', fontsize = axis_size)
    #plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend()
    plt.legend(handles, labels, numpoints = 1, 
               loc=1, ncol=1, borderaxespad=1.)


    #plt.show()    
    plt.savefig(Dirname+"CRONUS_update_spallation_and_muons.svg",format = Fileformat)  
    
   

if __name__ == "__main__":
    CRONUS_diff_params() 