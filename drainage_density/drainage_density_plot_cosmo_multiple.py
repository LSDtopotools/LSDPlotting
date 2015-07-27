## drainage_density_plot.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function creates two subplots: of drainage density against CRN-derived erosion
## rate for two field sites.  The user needs to specify the OutputFigureName and
## OutputFigureFormat.  It takes two input text files, one for each field site.  They
## should have the following layout with 9 columns:
## drainage_density mean_slope slope_standard_deviation slope_standard_error 
## cosmogenic_erosion_rate cosmogenic_erosion_error drainage_area 
## mean_hilltop_curvature mean_hilltop_curvature_standard_error
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## FJC 21/01/14
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib as mpl
import matplotlib.cm as cmx
from pylab import *
from scipy import stats

def make_plots():
    

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 26
    
    #norm = mpl.colors.Normalize(vmin=0, vmax=6)
    
    ########################
    #                      #
    #   READ IN THE DATA   #
    #                      #
    ########################

    DataDirectory =  './'    
    FileName = 'boulder_creek_drainage_density_cosmo.txt'
    OutputFigureName = 'drainage_density_cosmo_multiple'
    OutputFigureFormat = 'pdf'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    drainage_density = np.zeros(no_lines)        # drainage density
    mean_slope = np.zeros(no_lines)              # mean slope
    slope_stdev = np.zeros(no_lines)             # standard deviation of slope
    slope_sterr = np.zeros(no_lines)             # standard error of slope
    erosion_rate = np.zeros(no_lines)            # cosmo erosion rate
    cosmo_error = np.zeros(no_lines)             # error on cosmo dates
    drainage_area = np.zeros(no_lines)           # drainage area
    mean_cht = np.zeros(no_lines)                # mean hilltop curvature
    cht_sterr = np.zeros(no_lines)               # standard error of curvature

  
    for i in range (0,no_lines):
        line = lines[i].strip().split(" ")
        #print line
        drainage_density[i] = float(line[0])
        mean_slope[i] = float(line[1])
        slope_stdev[i] = float(line[2])
        slope_sterr[i] = float(line[3])
        erosion_rate[i] = float(line[4])
        cosmo_error[i] = float(line[5])
        drainage_area[i] = float(line[6])/1000000
        mean_cht[i] = float(line[7])
        cht_sterr[i] = float(line[8])
        
    f.close()
    
    FileName2 = 'fr1m_nogaps_drainage_density_cosmo.txt'
    g = open(DataDirectory + FileName2,'r')  # open file
    lines2 = g.readlines()   # read in the data
    no_lines2 = len(lines2)   # get the number of lines (=number of data)

    # data variables
    drainage_density2 = np.zeros(no_lines2)        # drainage density
    mean_slope2 = np.zeros(no_lines2)              # mean slope
    slope_stdev2 = np.zeros(no_lines2)             # standard deviation of slope
    slope_sterr2 = np.zeros(no_lines2)             # standard error of slope
    erosion_rate2 = np.zeros(no_lines2)            # cosmo erosion rate
    cosmo_error2 = np.zeros(no_lines2)             # error on cosmo dates
    drainage_area2 = np.zeros(no_lines2)           # drainage area
    mean_cht2 = np.zeros(no_lines2)                # mean hilltop curvature
    cht_sterr2 = np.zeros(no_lines2)               # standard error of curvature

  
    for i in range (0,no_lines2):
        line2 = lines2[i].strip().split(" ")
        #print line
        drainage_density2[i] = float(line2[0])
        mean_slope2[i] = float(line2[1])
        slope_stdev2[i] = float(line2[2])
        slope_sterr2[i] = float(line2[3])
        erosion_rate2[i] = float(line2[4])
        cosmo_error2[i] = float(line2[5])
        drainage_area2[i] = float(line2[6])/1000000
        mean_cht2[i] = float(line2[7])
        cht_sterr2[i] = float(line2[8])
        
    g.close()
    
    
    #############################    
    #                           #
    #   DO SOME STATS TO GET N  #
    #                           #
    #############################
    
    erosion_rate = erosion_rate*10**-3
    cosmo_error = cosmo_error*10**-3
    
    drainage_density_log = log10(drainage_density)
    erosion_rate_log = log10(erosion_rate)
    
    gradient, intercept, r_value, p_value, st_err = stats.linregress(erosion_rate_log, drainage_density_log)
    print "Power law regression stats (erosion/drainage density) for ", FileName
    print "Gradient:", gradient
    print "P value:", p_value
    print "R2:", r_value
    print "Standard error", st_err
    
    x = np.linspace(0, np.max(erosion_rate)+0.1, 1000)
    
    intercept = 10**intercept
    y = intercept*x**gradient
    print "Intercept:", intercept
    
    erosion_rate2 = erosion_rate2*10**-3
    cosmo_error2 = cosmo_error2*10**-3
    
    drainage_density_log2 = log10(drainage_density2)
    erosion_rate_log2 = log10(erosion_rate2)
    
    gradient2, intercept2, r_value2, p_value2, st_err2 = stats.linregress(erosion_rate_log2, drainage_density_log2)
    print "Power law regression stats (erosion rate/drainage density) for ", FileName2
    print "Gradient:", gradient2
    print "P value:", p_value2
    print "R2:", r_value2
    print "Standard error", st_err2
    
    x2 = np.linspace(0, np.max(erosion_rate2)+0.1, 1000)
    
    intercept2 = 10**intercept2
    y2 = intercept2*x2**gradient2
    print "Intercept:", intercept2
    
    
    ########################    
    #                      #
    #   MAKE SCATTERPLOTS  #
    #                      #
    ########################
    
    fig = plt.figure(1, facecolor='white', figsize=(20,10))
    subplots_adjust(left = 0.1, wspace=0.3, hspace=0.3)
    
    ax = fig.add_subplot(121)    
    plt.title('Boulder Creek, CO')
    plt.errorbar(erosion_rate, drainage_density, xerr=cosmo_error, fmt='ko', lw = 1, alpha = 1, markersize=0, zorder=1)
    plt.scatter(erosion_rate, drainage_density, c=drainage_area, cmap=cmx.Reds, lw = 2, s=300, alpha = 1, label = 'Basin drainage area', zorder=2)
    sm = plt.cm.ScalarMappable(cmap=cmx.Reds,norm=plt.normalize(vmin=0, vmax=5))
    sm._A = []
    plt.plot(x,y, 'k--')
    plt.annotate('$D_d=2E^{1.99}$\n$R^2=0.65$\n$p<0.01$', (0.005,0.018), color='k', fontsize=32, bbox=dict(facecolor='white', edgecolor='black', boxstyle='square, pad=0.3'))
    ax.text(0.0023,0.026, 'a', bbox=dict(facecolor='white', edgecolor='none'), horizontalalignment='left', verticalalignment='top', fontsize = 32)
    plt.ylabel('Drainage density (m/m$^2$)')
    plt.xlabel('Erosion rate (m/kyr)')
    plt.xlim(0, np.max(erosion_rate)+0.01)
    plt.ylim(0,np.max(drainage_density)+0.001)
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
   
    ax = fig.add_subplot(122)  
    plt.title('Feather River, CA')
    plt.errorbar(erosion_rate2, drainage_density2, xerr=cosmo_error2, fmt='ko', lw = 1, alpha = 1, markersize=0, zorder=1)
    plt.scatter(erosion_rate2, drainage_density2, c=drainage_area2, cmap=cmx.Reds, lw = 2, s=300, alpha = 1, label = 'Basin drainage area', zorder=2)
    plt.annotate('$D_d=0.1E^{0.91}$\n$R^2=0.76$\n$p<0.01$', (0.15,0.0015), color='k', fontsize=32, bbox=dict(facecolor='white', edgecolor='black', boxstyle='square, pad=0.3'))
    ax.text(0.006,0.0188, 'b', bbox=dict(facecolor='white', edgecolor='none'), horizontalalignment='left', verticalalignment='top', fontsize = 32)
    plt.plot(x2,y2, 'k--')
    plt.ylabel('Drainage density (m/m$^2$)')
    plt.xlabel('Erosion rate (m/kyr)')
    plt.xlim(0, np.max(erosion_rate2)+0.01)
    plt.ylim(0,np.max(drainage_density2)+0.001)
    yticks = ax.yaxis.get_major_ticks()
    yticks[0].label1.set_visible(False)
    
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(sm, cax=cbar_ax)
    cbar.set_label('Basin drainage area (km$^2$)')

    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    plt.clf()
    
    
if __name__ == "__main__":
    make_plots()    

	