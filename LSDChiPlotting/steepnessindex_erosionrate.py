## steepnessindex-vs-erosionrate.py
##
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function plots the steepness index in chi-plots (see Perron and Royden, 2012) against denudation rates for a given zone.
## A linear regression is performed to calculate the n and K values with a boostrapping method.
## Relevant parameters (n, m/n, K, p-value...) are displayed on the figure.
## The user needs to specify the name of the zone in the code.
##
## mharel 2014
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy import stats
import csv
import collections
import random
import bisect

def make_plots():
    
    label_size = 20
    #title_size = 30
    axis_size = 26

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size


    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    # open file
    # =================================
    Dirr = 'zone35'        # name of zone directory
    newDirr = 'zone24'     # name in the new referencing system
    # =================================
    
    DataDirectory =   't:\\Topo_Data\\general\\Old_zone_ref\\'+Dirr+'\\visu\\'  
    FileName = 'data-'+Dirr+'-sensi.txt'
    
    #DataDirectory =  't:\\Topo_Data\\general\\Fixed_movern\\'+Dirr+'\\visu\\'   
    #FileName = 'data-'+Dirr+'-fixed.txt'
  
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()   # read in the data
    n_lines = len(lines)   # get the number of lines (=number of data)
    n_data = n_lines -1
    
    # data variables initialization
    erosion_rate = np.zeros(n_data) # erosion rate from cosmogenics
    sd_erosion_rate = np.zeros(n_data) # erosion rate from cosmogenics
    basin_area = np.zeros(n_data)  # drainage area
    m_over_n = np.zeros(n_data) # m over n
    mean_steepness = np.zeros(n_data) # mean slope in chi-plot (main stem + tributaries)
    sd_steepness = np.zeros(n_data) # standard deviation for slope in chi-plot (main stem + tributaries)
   
    
    print "Reading " + FileName
    line = lines[0].strip().split(" ")

    for i in range (0,n_data):
        line = lines[i+1].strip().split(" ")
        erosion_rate[i] = float(line[1])*10**(-6)
        sd_erosion_rate[i] = float(line[2])*10**(-6) 
        basin_area[i] = float(line[3])
        m_over_n[i] = float(line[4]) 
        mean_steepness[i] = float(line[5]) 
        sd_steepness[i] = float(line[6])
       
    f.close()
        
    #########################
    #                       #
    #   MAKE CHI-PLOTS      #
    #                       #
    #########################    

    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # PLOT OF MEAN CHI m-VALUE (+ERROR) AGAINST EROSION RATE  
    plt.figure(1, facecolor='white',figsize=(10,7.5))    
    ax = plt.subplot(1,1,1)
    
    plt.plot(erosion_rate, mean_steepness, "o", markersize=8, color='r')
    ax.errorbar(erosion_rate, mean_steepness, yerr=sd_steepness, fmt='o')
    #plt.plot(erosion_rate, mean_steepness + sd_steepness, ".", linewidth=0.25, color='k')
    #plt.plot(erosion_rate, mean_steepness - sd_steepness, ".", linewidth=0.25, color='k')
  
  
    # Configure final plot
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('Erosion rate', fontsize = axis_size)
    plt.ylabel('Mean gradient in $\chi$ space', fontsize = axis_size)
    plt.title('$m/n$: '+str(m_over_n[0]), fontsize = label_size)
    
 #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # PLOT OF MEAN CHI m-VALUE AGAINST EROSION RATE, WITH BASIN AREA
    plt.figure(2, facecolor='white',figsize=(10,7.5))    
    ax = plt.subplot(1,1,1)
    
    plt.plot(erosion_rate, mean_steepness, "o", markersize=8, color='r')
    plt.scatter(erosion_rate, mean_steepness, s=basin_area/50000, alpha=0.1)

    # Configure final plot
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('Erosion rate', fontsize = axis_size)
    plt.ylabel('Mean gradient in $\chi$ space', fontsize = axis_size)
    plt.title('$m/n$: '+str(m_over_n[0]), fontsize = label_size)
    
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # PLOT OF MEAN CHI m-VALUE (+ERROR) AGAINST EROSION RATE   LOG-LOG + FIT
    fig, ax = plt.subplots(1,1,1,figsize=(10,7.5))
    fig.set_facecolor('white')

    xlog = np.log10(erosion_rate)
    ylog = np.log10(mean_steepness) 
    xerrlog = 0.434 * sd_erosion_rate / erosion_rate
    yerrlog = 0.434 * sd_steepness / mean_steepness
    # Relative error displayed in log-log plot, explained here : http://faculty.washington.edu/stuve/log_error.pdf
    ax.errorbar(xlog, ylog, xerr=xerrlog, yerr=yerrlog, fmt='o',color='b')       
    im = ax.scatter(xlog, ylog, s=70, c=basin_area, marker='o',cmap=plt.cm.jet, zorder=10)
    cb = plt.colorbar(im)
    #fig.colorbar(im, ax=ax)
    cb.set_label('Basin Area (m2)',fontsize=20)

    # Linear fitting y = ax+b : fit = np.polyfit(xlog, ylog, 1, full=True)
    # Second method linear fit :
    slope, intercept, r_value, p_value, std_err = stats.linregress(xlog, ylog)
    nn = 1/slope
    kk = (10**(-intercept*nn))/(1000**(m_over_n[0]*nn))
    
    #------------------------------------------------------------
    # BOOTSTRAPPING on K (and n)
    # The idea would be to re-sample the data and recalculate K and n after removing 1 data point randomly (with replacement, 
    # the same number of times as there are points in the dataset). Then take the mean K of these values and the standard deviation as 
    # a measure of the error on K. 
    n_li = []
    K_li = []
    for ii in range(n_data):
        slope, intercept, r_value, p_value, std_err = stats.linregress(np.delete(xlog, ii), np.delete(ylog, ii))
        n_li.append(1/slope)
        K_li.append((10**(-intercept*nn))/(1000**(m_over_n[0]*nn)))
    n_li.append(nn)
    K_li.append(kk)    
    
    mean_n = np.mean(n_li)
    sd_n = np.std(n_li)
    print '<mean_n> = ' +str(mean_n)
    #print 'n_bootst = ' +str(n_li)
    # CHECKING INDIVIDUAL K VALUES TO EVALUATE THE SENSITIVITY TO INTERCEPT
    #sensi_K = erosion_rate/ [(1000**(m_over_n[0]*nn)) * mean_steepness**nn]
    sensi_K = erosion_rate/ [(1000**(m_over_n[0]*mean_n)) * mean_steepness**mean_n]
    mean_K = np.mean(sensi_K)
    sd_K = np.std(sensi_K)
    print '<mean_K> = '+str(mean_K)+'    correct units'
    #------------------------------------------------------------    
    
    
    print 'slope = ', slope
    print 'intercept = ', intercept
    print 'r value = ', r_value
    print  'p_value = ', p_value
    print 'standard error = ', std_err
    print 'n = ', mean_n
    print 'K = ', mean_K , ' correct unit'
    line = slope*xlog+intercept
    plt.plot(xlog,line,'m-',xlog,ylog,'o')

    # Configure final plot
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('LOG Erosion rate', fontsize = axis_size-2)
    plt.ylabel('LOG Mean $\chi$ slope', fontsize = axis_size-2)
    plt.title(''+str(newDirr)+',  $m/n$ = '+str(m_over_n[0]), fontsize = label_size+4)
    #plt.text(3.6,3.9,'Linear fit y(x)=ax+b', color='m')
    ax.annotate('Linear fit y(x)=ax+b', xy=(0, 0), xycoords='axes fraction', fontsize=20,
                xytext=(1, -60), textcoords='offset points',
                ha='left', va='top',color='g')
    ax.annotate('R2 = '+str(r_value**2), xy=(0, 0), xycoords='axes fraction', fontsize=20,
                xytext=(1, -80), textcoords='offset points',
                ha='left', va='top',color='g')  
    ax.annotate('p = '+str(p_value), xy=(0, 0), xycoords='axes fraction', fontsize=20,
                xytext=(1, -100), textcoords='offset points',
                ha='left', va='top',color='g') 
    ax.annotate('n = '+str(mean_n), xy=(0.55, 0), xycoords='axes fraction', fontsize=20,
                xytext=(1, -80), textcoords='offset points',
                ha='left', va='top',color='b')   
    ax.annotate('K = '+str(mean_K), xy=(0.55, 0), xycoords='axes fraction', fontsize=20,
                xytext=(1, -100), textcoords='offset points',
                ha='left', va='top',color='b')           
    fig.subplots_adjust(bottom=0.25, right=0.7)

    #----------------------------------------------------------------------------------
    plt.savefig('t:\\Topo_Data\\post-traitement\\chi_plot_'+newDirr+'.png') 
    plt.show()
      

if __name__ == "__main__":
    make_plots()