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

def CRNCAIRNvsnewCRONUS_erates():

    Dirname = "T://Papers_LaTeX//crn_basinwide_paper//Compiled_results//"        
    #Dirname = "C://code//git_papers//crn_basinwide_paper//Compiled_results//"
    #Fname = "Palumbo*_CompareResults.csv"
    
    SiteNames = []
    SiteDicts = []
    PaperNames = []    
    
    # loop through the directory, getting the results from the data    
    for fname in glob(Dirname+"*_newCRONUSCAIRNComparison.csv"):
        
        # get only the file without the data directory
        NoDirFname = LSDost.GetFileNameNoPath(fname)
        
        # Now get the prefix of the file
        splitfname = NoDirFname.split('_newCRONUSCAIRNComparison.csv')
        fprefix = splitfname[0]

        print "File prefix is: " + fprefix 

        # add to the sitenames list and create a holding dictionary
        SiteNames.append(fprefix)
        thisdict = {}

        # now get the prefixes
        if fprefix == "Bierman":
            PaperNames.append("Bierman et al., 2005")
        elif fprefix == "Dethier":
            PaperNames.append("Dethier et al., 2014")
        elif fprefix == "Kirchner":
            PaperNames.append("Kirchner et al., 2001")                
        elif fprefix == "Munak":
            PaperNames.append("Munack et al., 2014")            
        #elif fprefix == "Scherler":
        #    PaperNames.append("Scherler et al., 2014")
        #elif fprefix == "Safran":
        #    PaperNames.append("Safran et al., 2005") 
        elif fprefix == "Palumbo":
            PaperNames.append("Palumbo et al., 2010")   
        
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
                
                # get the maximum and minimum erosion rates
                if (float(split_line[16]) > max_erate):
                    max_erate = float(split_line[16])
                if (float(split_line[20]) > max_erate):
                    max_erate = float(split_line[20]) 
                                    
                if (float(split_line[16]) < min_erate):
                    min_erate = float(split_line[16])
                if (float(split_line[20]) < min_erate):
                    min_erate = float(split_line[20]) 
            
            Ce = np.asarray(CAIRN_erate)
            CnC = np.asarray(newCRONUS_erate)
            Cerr = np.divide( np.subtract(Ce,CnC), Ce)  
            
            
            thisdict["CAIRNvsnewCRONUSerr"] = Cerr  

            thisdict["CAIRN_erate"] = CAIRN_erate
            thisdict["CAIRN_uncert"] = CAIRN_uncert
            thisdict["Report_erate"] = Report_erate
            thisdict["Report_uncert"] = Report_uncert     
            thisdict["newCRONUS_erate"] = newCRONUS_erate
            thisdict["newCRONUS_uncert"] = newCRONUS_uncert                  
            SiteDicts.append(thisdict)  
            

    label_size = 10
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
    
    # make a line between the maximum and minimum erate
    one_line = np.linspace(min_erate,max_erate,1000)
        
    # now make plots based on these data
    Fig1 = plt.figure(1, facecolor='white',figsize=(4.72,4.72))  

    # generate a 120,90 grid. 
    gs = GridSpec(100,75,bottom=0.13,left=0.13,right=0.98,top=0.85) 
    ax = Fig1.add_subplot(gs[10:100,5:75])


    cmap = plt.cm.jet   
    colo = 0 
    
    for index,thisdict in enumerate(SiteDicts):
        
        colo = colo + (1.000/len(SiteDicts))
        #plt.errorbar(thisdict['CAIRN_erate'], thisdict['newCRONUS_erate'], 
        #             thisdict['CAIRN_uncert'], thisdict['newCRONUS_uncert'], fmt='.',color = cmap(colo), linewidth = 1.5)
        #plt.plot(thisdict['CAIRN_erate'], thisdict['newCRONUS_erate'], "o", markersize=4, 
        #         color=cmap(colo), label = PaperNames[index],markeredgewidth=1.)
        plt.plot(thisdict['CAIRN_erate'], thisdict['CAIRNvsnewCRONUSerr'], "o", markersize=4, 
                 color=cmap(colo), label = PaperNames[index],markeredgewidth=1.)
         

    #plt.plot(self.CRNData['AvgProdScaling'],self.CRNData['Error_CR'],color=cmap(self.CRNData['basin_relief']),"o", markersize=8     )
    #plt.errorbar(datazz['erate_cosmocalc']*10, datazz['erate_cmperkyr']*10, xerr=datazz['error_cosmocalc'], yerr=datazz['error_newcode'], fmt='o',color = cmap(colo))  
    ax.spines['top'].set_linewidth(1.5)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['right'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5) 
    
    # This gets all the ticks, and pads them away from the axis so that the corners don't overlap        
    ax.tick_params(axis='both', width=1.5, pad = 2)
    for tick in ax.xaxis.get_major_ticks():
            tick.set_pad(3)
    for tick in ax.yaxis.get_major_ticks():
            tick.set_pad(3)
            
    # logarithmic axes
    #ax.set_yscale('log')
    #ax.set_xscale('log')
            
    plt.xlabel('CAIRN denudation rate (mm/kyr)', fontsize = axis_size)
    plt.ylabel('($E_{CAIRN}$-$E_{newCRONUS}$)/$E_{CAIRN}$', fontsize = axis_size) 
    handles, labels = ax.get_legend_handles_labels()    
    plt.legend(handles, labels, numpoints = 1, bbox_to_anchor=(0., 1.02, 1., .102), 
               loc=3, ncol=2, mode="expand", borderaxespad=0.)

    #plt.show()       
    Fileformat = "svg"
    plt.savefig(Dirname+"CAIRN_vs_newCRONUS_erate_err.svg",format = Fileformat)
    
        

if __name__ == "__main__":
    CRNCAIRNvsnewCRONUS_erates()         
    