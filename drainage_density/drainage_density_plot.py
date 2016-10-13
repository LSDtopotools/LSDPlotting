## drainage_density_plot.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function creates a plot of drainage density against mean hilltop
## curvature.  The user needs to specify the OutputFigureName and OutputFigureFormat.  
## It takes two input files.  The first is a text file with the raw data with 4 columns:
## drainage density, mean hilltop curvature, mean basin slope and basin drainage area.
## The second is a text file with the binned data: with 9 columns as follows:
## binned_hilltop_curvature hilltop_curvature_standard_deviation hilltop_curvature_standard_error
## binned_draiange_density drainage_density_standard_deviation drainage_density_standard_error
## binned_slope slope_standard_deviation slope_standard_error
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## FJC 09/01/14
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.colors as colors
import matplotlib.cm as cmx
from pylab import *
from scipy import stats
import matplotlib.ticker as plticker

def make_plots(DEM_name, DataDirectory):
    

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 12

    ###############################
    #                             #
    #   READ IN THE DATA CLOUD    #
    #                             #
    ###############################
  
    FileName = DEM_name+'_drainage_density_cloud.txt'
    OutputFigureName = DEM_name+'_drainage_density'
    OutputFigureFormat = 'pdf'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    drainage_density = np.zeros(no_lines)        # drainage density
    mean_cht = np.zeros(no_lines)                # mean hilltop curvature
    mean_slope = np.zeros(no_lines)              # mean slope
    drainage_area = np.zeros(no_lines)           # drainage area
    m = np.zeros(no_lines)                       # marker size

  
    for i in range (0,no_lines):
        line = lines[i].strip().split(" ")
        #print line
        drainage_density[i] = float(line[0])
        mean_cht[i] = abs(float(line[1]))
        mean_slope[i] = float(line[2])   
        drainage_area[i] = float(line[3])
        m[i] = (drainage_area[i])/10000
        
    f.close()
    
    ################################
    #                              #
    #   READ IN THE BINNED DATA    #
    #                              #
    ################################    

    FileNameBinned = DEM_name+'_drainage_density_binned.txt'
    g = open(DataDirectory + FileNameBinned,'r')
    lines_binned = g.readlines()
    no_lines_binned = len(lines_binned)
    
    #data variables
    dd_binned = np.zeros(no_lines_binned)
    cht_binned = np.zeros(no_lines_binned)
    slope_binned = np.zeros(no_lines_binned)
    cht_stdev = np.zeros(no_lines_binned)
    dd_stdev = np.zeros(no_lines_binned)
    slope_stdev = np.zeros(no_lines_binned)
    cht_sterr = np.zeros(no_lines_binned)
    dd_sterr = np.zeros(no_lines_binned)
    slope_sterr = np.zeros(no_lines_binned)

    
    for i in range (0, no_lines_binned):
        line_binned = lines_binned[i].strip().split(" ")
        if line_binned != -9999:
            cht_binned[i] = float(line_binned[0])
            cht_stdev[i] = float(line_binned[1])
            cht_sterr[i] = float(line_binned[2])
            dd_binned[i] = float(line_binned[3])
            dd_stdev[i] = float(line_binned[4])
            dd_sterr[i] = float(line_binned[5])
            slope_binned[i] = float(line_binned[6])
            slope_stdev[i] = float(line_binned[7])
            slope_sterr[i] = float(line_binned[8])

    g.close()
    
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

    gradient2, intercept2, r_value2, p_value2, st_err2 = stats.linregress(mean_cht_log, drainage_density_log)
    print "Power law regression stats (CHT/drainage density):"
    print "Gradient:", gradient2
    print "P value:", p_value2
    print "R2:", r_value2
    print "Standard error", st_err2
    
    x = np.linspace(0, np.max(mean_cht[np.isnan(mean_cht)==False]), 1000)
    
    intercept2 = 10**intercept2
    print "Intercept", intercept2
    y = intercept2*x**gradient2

    ########################    
    #                      #
    #   MAKE SCATTERPLOTS  #
    #                      #
    ########################
    
    fig = plt.figure(1, facecolor='white', figsize=(5,5))
    
    ax = fig.add_subplot(111)
    subplots_adjust(left = 0.2)
    plt.scatter(mean_cht, drainage_density, s=m, facecolor='0.5', lw = 0.1, alpha = 0.5, label = 'Basin drainage area')
    plt.plot(x, y, 'r--', label = "Regression")
    plt.errorbar(cht_binned, dd_binned, xerr=cht_sterr, yerr=dd_sterr, fmt='rD', ecolor='r', elinewidth=0, markersize=4, capsize=2, label = "Binned data")
    plt.annotate('$y=0.03x^{0.31}$\n$R^2=0.27$\n$p<0.01$', (0.09,0.018), color='r')
    plt.xlabel('Mean hilltop curvature (m$^{-1}$)')
    plt.ylabel('Drainage density (m/m$^2$)')
    loc = plticker.MultipleLocator(base=0.03)
    plt.gca().xaxis.set_major_locator(loc)
    ax.text(0.005,0.03, 'a', bbox=dict(facecolor='white', edgecolor='none'), horizontalalignment='left', verticalalignment='top', fontsize = 16)
    plt.legend(loc=1, numpoints=1)
    plt.setp(gca().get_legend().get_texts(), fontsize='10')
    plt.xlim(0, np.max(mean_cht[np.isnan(mean_cht)==False])+0.01)
    plt.ylim(0,np.max(drainage_density)+0.001)
    
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    plt.clf()
    
if __name__ == "__main__":
    make_plots()    

	