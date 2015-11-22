# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 06:38:37 2015

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



def CollateCRNData():
    
    Directory = "C://basin_data//CosmoPaper//Results//Compiled//"
    #Directory = "T://Papers_LaTeX//crn_basinwide_paper//Compiled_results//"
    Dirname = LSDost.ReformatSeperators(Directory)
    Dirname = LSDost.AppendSepToDirectoryPath(Dirname)
    
    Fileformat = 'svg'
    
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
    
    #===========================================================================    
    # now make plots based on these data
    Fig1 = plt.figure(1, facecolor='white',figsize=(10,7.5))  

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.1,left=0.1,right=0.95,top=0.95) 
    ax = Fig1.add_subplot(gs[10:100,5:75])
    
    # this gets the colors to map to specific sites
    cmap = plt.cm.jet    
    colo = 0       
    
    
    for index,CRNObj in enumerate( CRNDataList):
        colo = colo + (1.000/len(CRNprefixes))
        ax.plot(CRNObj.GetAverageCombinedScaling(),CRNObj.GetError_CR(), "o",
                markersize=10, color=cmap(colo), label = CRNprefixes[index],markeredgewidth=2.5)

    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5) 
    
 
    
    
    plt.xlabel('Production factor', fontsize = axis_size-2)
    plt.ylabel('($\epsilon_{CR}$-$\epsilon_{BERC}$)/$\epsilon_{BERC}$', fontsize = axis_size-2)
    #plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, numpoints = 1, loc='upper right')
        
    plt.savefig(Dirname+"Production_vs_error.svg",format = Fileformat)
    
    #Fig1.show()
     
    Fig1.clf()     



    # These don't work in my version of matplotlib...I must update (!)
    # have found a workaround below    
    #plt.rcParams['xtick.major.linewidth'] = 4
    #plt.rcParams['xtick.minor.width'] = 2
 

    #===========================================================================   
    # now make plots based on these data
    Fig2 = plt.figure(1, facecolor='white',figsize=(10,7.5))  

    plt.rcParams['xtick.major.size'] = 20    
    plt.rcParams['xtick.minor.size'] = 10
    plt.rcParams['ytick.major.size'] = 10

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.1,left=0.1,right=0.95,top=0.95) 
    ax = Fig2.add_subplot(gs[10:100,5:75])
    
    # this gets the colors to map to specific sites
    cmap = plt.cm.jet    
    colo = 0       

    for index,CRNObj in enumerate( CRNDataList):
        colo = colo + (1.000/len(CRNprefixes))
        ax.plot(CRNObj.GetErosionRates(),CRNObj.GetError_CR(), "o", markersize=10, 
                color=cmap(colo), label = CRNprefixes[index],markeredgewidth=2.5)

    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    #ax.tick_params(axis='both', width=2.5)
    ax.set_xscale('log') 
    
    # This gets all the ticks, and pads them away from the axis so that the corners don't overlap
    # the which command tells the program to get major and minor ticks 
    ax.tick_params(axis='both', width=2.5, pad = 2, which = 'both')
    for tick in ax.xaxis.get_major_ticks():
        tick.set_pad(10)   

    for tick in ax.yaxis.get_major_ticks():
        tick.set_pad(10)  

    #for tick in ax.xaxis.get_minor_ticks():
    #    tick.tick_params(width = 2.5)  
        
        
    plt.xlabel('$\epsilon_{BERC}$ g cm$^{-2}$ yr$^{-1}$', fontsize = axis_size-2)
    plt.ylabel('($\epsilon_{CR}$-$\epsilon_{BERC}$)/$\epsilon_{BERC}$', fontsize = axis_size-2)
    #plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, numpoints = 1, loc='upper right')
        
    #plt.show()    
    plt.savefig(Dirname+"Erosion_vs_error.svg",format = Fileformat)    
    Fig2.clf()    
        
    #===========================================================================   
    # now make plots based on these data
    Fig3 = plt.figure(1, facecolor='white',figsize=(10,7.5))  

    plt.rcParams['xtick.major.size'] = 10    
    #plt.rcParams['xtick.minor.size'] = 10
    plt.rcParams['ytick.major.size'] = 10

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.1,left=0.1,right=0.95,top=0.95) 
    ax = Fig3.add_subplot(gs[10:100,5:75])
    
    # this gets the colors to map to specific sites
    cmap = plt.cm.jet    
    colo = 0       

    for index,CRNObj in enumerate( CRNDataList):
        colo = colo + (1.000/len(CRNprefixes))
        ax.plot(CRNObj.GetAverageCombinedScaling(),CRNObj.GetError_CC(), "o",
                markersize=10, color=cmap(colo), label = CRNprefixes[index],markeredgewidth=2.5)

    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    #ax.tick_params(axis='both', width=2.5)
    
    # This gets all the ticks, and pads them away from the axis so that the corners don't overlap
    # the which command tells the program to get major and minor ticks 
    ax.tick_params(axis='both', width=2.5, pad = 2, which = 'both')
    for tick in ax.xaxis.get_major_ticks():
        tick.set_pad(10)   

    for tick in ax.yaxis.get_major_ticks():
        tick.set_pad(10)  

    #for tick in ax.xaxis.get_minor_ticks():
    #    tick.tick_params(width = 2.5)  
        
        
    plt.xlabel('Production factor', fontsize = axis_size-2)
    plt.ylabel('($\epsilon_{CC}$-$\epsilon_{BERC}$)/$\epsilon_{BERC}$', fontsize = axis_size-2)
    #plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, numpoints = 1, loc='upper right')
        
    #plt.show()    
    plt.savefig(Dirname+"CSOMOCALC_vs_error.svg",format = Fileformat)        
    Fig3.clf() 

        
    #===========================================================================   
    # now make plots based on these data
    Fig4 = plt.figure(1, facecolor='white',figsize=(10,7.5))  

    plt.rcParams['xtick.major.size'] = 10    
    #plt.rcParams['xtick.minor.size'] = 10
    plt.rcParams['ytick.major.size'] = 10

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.1,left=0.1,right=0.95,top=0.95) 
    ax = Fig4.add_subplot(gs[10:100,5:75])
    
    # this gets the colors to map to specific sites
    cmap = plt.cm.jet    
    colo = 0       

    for index,CRNObj in enumerate( CRNDataList):
        colo = colo + (1.000/len(CRNprefixes))
        ax.plot(CRNObj.GetAverageCombinedScaling(),CRNObj.GetError_CR_em(), "o",
                markersize=10, color=cmap(colo), label = CRNprefixes[index],markeredgewidth=2.5)

    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    #ax.tick_params(axis='both', width=2.5)
    
    # This gets all the ticks, and pads them away from the axis so that the corners don't overlap
    # the which command tells the program to get major and minor ticks 
    ax.tick_params(axis='both', width=2.5, pad = 2, which = 'both')
    for tick in ax.xaxis.get_major_ticks():
        tick.set_pad(10)   

    for tick in ax.yaxis.get_major_ticks():
        tick.set_pad(10)  

    #for tick in ax.xaxis.get_minor_ticks():
    #    tick.tick_params(width = 2.5)  
        
        
    plt.xlabel('Production factor', fontsize = axis_size-2)
    plt.ylabel('($\epsilon_{CC-CRONUS}$-$\epsilon_{BERC}$)/$\epsilon_{BERC}$', fontsize = axis_size-2)
    #plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, numpoints = 1, loc='upper right')
        
    #plt.show()    
    plt.savefig(Dirname+"CSOMOCALC_CRem_vs_error.svg",format = Fileformat)           
    Fig4.clf()         

if __name__ == "__main__":
    CollateCRNData() 