## chi_seg_plot.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function creates a chi-elevation plot (see Perron and Royden, 2012; An 
## integral approach to bedrock river profile analysis), for river profiles
## stored in the *.tree file. The trunk channel is highlighted distinctly from
## the tributary channels. The user needs to specify the FileName,
## OutputFigureName and OutputFIgureFormat in the code.
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## DTM 07/11/2012
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##
## DAV 18/1/2013 - Modified from the chi_plot.py file. Plots segments from the 
## best_fit_tree.chi_tree file generated in Chile_test3.
##
## Improvements to make:
## plot segments as proper lines?
## ...lots more!
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-  

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.colors as colors

def make_plots():
    

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 12

    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    # open file
    DataDirectory =  ''    
    FileName = 'best_fit_tree.chi_tree'
    OutputFigureName = 'chi_seg_plot'
    OutputFigureFormat = 'png'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()[4:]   # read in the data  (skip header lines)
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    channel_num = np.zeros(no_lines, dtype=np.int)     # channel number
    chi = np.zeros(no_lines)            # chi
    elev = np.zeros(no_lines)           # elevation
    best_elev = np.zeros(no_lines)  # 'best fit' elevation
    
    for i in range (0,no_lines):
        line = lines[i].strip().split(" ")
        #print line
        channel_num[i] = int(float(line[0]))
        chi[i] = float(line[1])
        elev[i] = float(line[2])
        best_elev[i] = float(line[3])
   
    f.close() 
        
    #########################
    #                       #
    #  MAKE SEGMENT-PLOTS   #
    #                       #
    #########################    
    
    plt.figure(1, facecolor='white')
    
    # swap for 'elev' to plot the real chi-elevation plot etc.
    plt.plot(chi, best_elev, "r.", mew=0, markersize=2)  # plot formatting
 
    # Configure final plot
    plt.xlabel('$\chi$ [m]')
    plt.ylabel('Elevation [m]')

    #plt.show()
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    
if __name__ == "__main__":
    make_plots()