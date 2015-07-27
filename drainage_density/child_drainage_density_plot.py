## child_drainage_density_plot.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function creates a plot of drainage density against uplift rate for a 
## CHILD modelling run.  The user must specify the input file with the CHILD
## data, the output figure name and the output figure format.  THe input file must
## have the following layout (3 columns):
## mean_hilltop_curvature drainage_density uplift_rate
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## FJC 25/05/15
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.colors as colors
import matplotlib.cm as cmx
from pylab import *
from scipy import stats
import matplotlib.ticker as plticker


def make_plots():
    

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 12

    ###############################
    #                             #
    #   READ IN THE DATA CLOUD    #
    #                             #
    ###############################

    DataDirectory =  './'    
    FileName = 'child_drainage_density_n_0.4_nonlinear.txt'
    OutputFigureName = 'drainage_density_child_n_0.4_nonlinear'
    OutputFigureFormat = 'pdf'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    drainage_density = np.zeros(no_lines)        # drainage density
    mean_cht = np.zeros(no_lines)                # mean hilltop curvature
    e_rate = np.zeros(no_lines)
  
    for i in range (0,no_lines):
        line = lines[i].strip().split(" ")
        #print line
        mean_cht[i] = abs(float(line[0]))
        drainage_density[i] = float(line[1])
        e_rate[i] = float(line[2])

    f.close()
    
    ########################
    #                      #
    #   GET SOME STATS     #
    #                      #
    ########################
   
    # do a linear regression on drainage density vs mean hilltop curvature
    gradient1, intercept1, r_value1, p_value1, st_err1 = stats.linregress(mean_cht[np.isnan(mean_cht)==False], drainage_density[np.isnan(mean_cht)==False])
    print "Linear regression stats (CHT/drainage density):"
    print "Gradient:", gradient1
    print "P value:", p_value1
    print "R2:", r_value1**2
    
    if p_value1 < 0.01:
        p_value = '< 0.01'   
    else:
        p_value = str(p_value1)
        
    line = gradient1*mean_cht+intercept1
    
   # do a power law regression on drainage density vs mean CHT
    drainage_density_log = log10(drainage_density[np.isnan(mean_cht)==False])
    mean_cht_log = log10(mean_cht[np.isnan(mean_cht)==False])
    e_rate_log = log10(e_rate)

    gradient2, intercept2, r_value2, p_value2, st_err2 = stats.linregress(e_rate_log, drainage_density_log)
    print "Power law regression stats (CHT/drainage density):"
    print "Gradient:", gradient2
    print "P value:", p_value2
    print "R2:", r_value2
    print "Standard error", st_err2
    
    x = np.linspace(0, np.max(e_rate), 1000)
    
    intercept2 = 10**intercept2
    print "Intercept", intercept2
    y = intercept2*x**gradient2
    
    ########################    
    #                      #
    #   MAKE SCATTERPLOTS  #
    #                      #
    ########################
    
    fig = plt.figure(1, facecolor='white', figsize=(7,5))
        
    ax = fig.add_subplot(111)
    subplots_adjust(left = 0.2)
    plt.scatter(e_rate, drainage_density, c = mean_cht, lw = 0.1, cmap=cmx.Reds, s=50, zorder=100)
    plt.xlabel('Erosion rate (mm/ka)')
    plt.ylabel('Drainage density (m/m$^2$)')
    plt.title('Nonlinear hillslope sediment transport')
    ax.text(0.8, 0.92, '$n = 0.4$', bbox=dict(facecolor='white', edgecolor='none'), fontsize = 16, transform=ax.transAxes)
    plt.xlim(0,)
    sm = plt.cm.ScalarMappable(cmap=cmx.Reds,norm=plt.normalize(vmin=10, vmax=320))
    sm._A = []
    cbar = plt.colorbar(sm)
    cbar.set_label('Mean hilltop curvature (m$^{-1}$)')

    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    plt.clf()
#    
if __name__ == "__main__":
    make_plots()    

	