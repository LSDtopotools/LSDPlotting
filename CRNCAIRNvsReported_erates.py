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

    #Dirname = "C://basin_data//CosmoPaper//Results//Compiled//"
    Dirname = "T://Papers_LaTeX//crn_basinwide_paper//Compiled_results//"   
    #Fname = "Palumbo*_CompareResults.csv"
    
    SiteNames = []
    SiteDicts = []
    PaperNames = []  
    PaperColours = []
    
    # loop through the directory, getting the results from the data    
    for fname in glob(Dirname+"*_ErateComparisonNew.csv"):
        
        # get only the file without the data directory
        NoDirFname = LSDost.GetFileNameNoPath(fname)
        
        # Now get the prefix of the file
        splitfname = NoDirFname.split('_ErateComparisonNew.csv')
        fprefix = splitfname[0]

        print "File prefix is: " + fprefix 

        # add to the sitenames list and create a holding dictionary
        SiteNames.append(fprefix)
        thisdict = {}

        # now get the prefixes
        if fprefix == "Bierman":
            PaperNames.append("Bierman et al., 2005")
            PaperColours.append("blue")
        elif fprefix == "Dethier":
            PaperNames.append("Dethier et al., 2014")
            PaperColours.append("lawngreen")
        elif fprefix == "Kirchner":
            PaperNames.append("Kirchner et al., 2001") 
            PaperColours.append("yellow")               
        elif fprefix == "Munack":
            PaperNames.append("Munack et al., 2014")
            PaperColours.append("orange")
        elif fprefix == "Scherler":
            PaperNames.append("Scherler et al., 2014")
            PaperColours.append("black")
        elif fprefix == "Safran":
            PaperNames.append("Safran et al., 2005")
            PaperColours.append("powderblue")
        elif fprefix == "Palumbo":
            PaperNames.append("Palumbo et al., 2010")
            PaperColours.append("maroon")   
        
        print "I am woking with the dataset: " + fprefix
        
        min_erate = 5
        max_erate = 5000
    
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


    #cmap = plt.cm.jet   
    #colo = 0 
    
    # plot the 1:1 line
    plt.plot(one_line,one_line,'k-',linewidth = 2)
    
    for index,thisdict in enumerate(SiteDicts):
        
        #colo = colo + (1.000/len(SiteDicts))
        plt.errorbar(thisdict['BERC_erate'], thisdict['Report_erate'], 
                     thisdict['BERC_uncert'], thisdict['Report_uncert'], fmt='.',color = PaperColours[index], linewidth = 1.5)
        plt.plot(thisdict['BERC_erate'], thisdict['Report_erate'], "o", markersize=4, 
                 color=PaperColours[index], label = PaperNames[index],markeredgewidth=1.)
        

    ax.annotate("1:1 line",
            xy=(3000, 3000), xycoords='data',
            xytext=(200, 4000), textcoords='data',
            arrowprops=dict(arrowstyle="fancy", #linestyle="dashed",
                            color="0.5",
                            shrinkB=5,
                            connectionstyle="arc3,rad=-0.3",
                            ),
            )


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
    ax.set_yscale('log')
    ax.set_xscale('log')
            
    plt.xlabel('CAIRN denudation rate (mm/kyr)', fontsize = axis_size)
    plt.ylabel('Reported denudation rate (mm/kyr)', fontsize = axis_size) 
    handles, labels = ax.get_legend_handles_labels()    
    plt.legend(handles, labels, numpoints = 1, bbox_to_anchor=(0., 1.02, 1., .102), 
               loc=3, ncol=2, mode="expand", borderaxespad=0.)

    #plt.show()       
    Fileformat = "svg"
    plt.savefig(Dirname+"CAIRN_vs_Reported_erates.svg",format = Fileformat)
    
        

if __name__ == "__main__":
    CRBERCvsReported_erates()         
    