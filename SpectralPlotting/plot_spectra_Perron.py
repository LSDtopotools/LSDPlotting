## plot_binned_radialPSD.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## DTM 10/12/2012
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import sys
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams

def make_plots(file_id):
    

    # Set up fonts for plots    
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 8
    rcParams['legend.numpoints'] = 1
    OutputFigureFormat='png'
    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    # open file    
    #FileName1 = 'test_binned_radialPSD.txt'
    FileName1 = file_id+'_binned_radialPSD.txt'
    #OutputFigureName = 'radial_PSD'
    #OutputFigureFormat = 'eps'
    f1 = open(FileName1,'r')  # open file
    lines = f1.readlines()   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)
    # data variables
    # data variables
    radial_frequency_binned = np.zeros(no_lines-1)      
    PSD_binned = np.zeros(no_lines-1)            
    wavelength_binned = np.zeros(no_lines-1)
    R_sq = np.zeros(no_lines-1)
    Beta = np.zeros(no_lines-1)             
    Background = np.zeros(no_lines-1)             
    CI95 = np.zeros(no_lines-1)             
    CI99 = np.zeros(no_lines-1)             
    
    for i in range (1,no_lines-1):
        line = lines[i].strip().split(" ")
        #print line
        radial_frequency_binned[i] = float(line[0])
        wavelength_binned[i] = float(line[1])        
        PSD_binned[i] = float(line[2])
        R_sq[i] = float(line[3])
        Beta[i] = float(line[4])
        Background[i] = float(line[5])
        CI95[i] = float(line[6])
        CI99[i] = float(line[7])
    f1.close()
    
    #FileName2 = 'test_radialPSD.txt'
    FileName2 = file_id+'_radialPSD.txt'
    f2 = open(FileName2,'r')  # open file
    lines = f2.readlines()   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)
    # data variables
    radial_frequency = np.zeros(no_lines-1)      
    wavelength = np.zeros(no_lines-1)
    amplitude = np.zeros(no_lines-1)  
    norm_amplitude = np.zeros(no_lines-1)                       

    
    for i in range (1,no_lines-1):
        line = lines[i].strip().split(" ")
        #print line
        radial_frequency[i] = float(line[0])
        wavelength[i] = float(line[1])        
        amplitude[i] = float(line[2])       
        norm_amplitude[i] = np.log(float(line[3]))
    f2.close()


    rollover_freq = radial_frequency_binned[Beta==max(Beta)]    
    #########################
    #                       #
    #   MAKE PSD plot       #
    #                       #
    #########################    
    
    plt.figure(1, facecolor='white',figsize=[4,8])
    ax1 = plt.subplot(3,1,1)
    ax1.axvline(x=rollover_freq,linestyle='dashed',color='black') 
    #ax1.vlines(rollover_freq,10**-9,10**2,linestyles='dashed')
    ax1.plot(radial_frequency, amplitude,".", alpha = 0.10, markeredgewidth = 0, color = '0.0')
    ax1.plot(radial_frequency_binned, PSD_binned,"o",color='white', markeredgecolor="red")
    ax1.plot(radial_frequency_binned, Background,"-b")
    ax1.set_yscale('log')
    ax1.set_xscale('log')
    ax1.set_xlim(xmax=0.003)
    ax1.grid(True)
    xmin,xmax = ax1.get_xlim()    
    ax1.annotate('a', xy=(0.95,0.85), xycoords='axes fraction',backgroundcolor='white',horizontalalignment='right', verticalalignment='bottom', fontsize=rcParams['font.size']+2) 
    ax1.set_ylabel('DFT mean-squared amplitude (m$^2$)')
    
    ax2 = plt.subplot(3,1,2)
    ax2.axvline(x=rollover_freq,linestyle='dashed',color='black')     
    series1 = ax2.plot(radial_frequency_binned[Beta != -9999], R_sq[Beta != -9999],"o", color="blue", label = 'R$^2$')
    ax2.set_ylabel('R$^2$')
    ax2.set_xscale('log')
    ax2.set_xlim(xmax=1)
    ax2.set_ylim(ymin=0.9*np.min(R_sq[Beta  > 0]),ymax=1)
    ax2.xaxis.grid(True)
    ax2.annotate('b', xy=(0.95,0.85), xycoords='axes fraction',backgroundcolor='white',horizontalalignment='right', verticalalignment='bottom', fontsize=rcParams['font.size']+2) 
    
    ax3 = plt.subplot(3,1,2).twinx()
    series2 = ax3.plot(radial_frequency_binned[Beta != -9999], Beta[Beta != -9999],"d",color='white', markeredgecolor="red", label = 'Beta')
    ax3.set_ylabel('Beta')
    ax3.set_xscale('log')
    ax3.set_ylim(ymin=0.8*np.min(Beta[Beta > 0]),ymax=1.25*np.max(Beta[Beta > 0]))
    ax3.set_xlim(xmin,xmax)
    series = series1+series2
    labels = [l.get_label() for l in series]
    ax2.legend(series, labels, loc=3)
    
    
    ax4 = plt.subplot(3,1,3)
    ax4.axhspan(0, np.log(np.max(CI99)), alpha = 0.2) 
    ax4.axhspan(0, np.log(np.max(CI95)), alpha = 0.2)    
    ax4.plot(radial_frequency, norm_amplitude,".", alpha = 0.75, markeredgewidth = 0, color = '0.0')
    ax4.set_ylabel('Normalised Power')
    ax4.set_xlabel('Radial Frequency (m$^{-1}$)')    
    ax4.set_xscale('log')
    ax4.set_xlim(xmin,xmax)    
    ax4.grid(True)
    ax4.annotate('c', xy=(0.95,0.85), xycoords='axes fraction',backgroundcolor='white',horizontalalignment='right', verticalalignment='bottom', fontsize=rcParams['font.size']+2) 
    plt.tight_layout()
    plt.subplots_adjust(right=0.85)
    #plt.show()
    plt.savefig(file_id+'_spectrum.' + OutputFigureFormat, format=OutputFigureFormat)
    
if __name__ == "__main__":
    #file_id = "/home/s1143956/LSD_Datastore/LH_paper_dems/gm_30m_dem"
    file_id = "T://analysis_for_papers//Noel_spectral//SwathTest"
    #file_id = "T://analysis_for_papers//Noel_spectral//BedTest"
    #make_plots(sys.argv[1])
    make_plots(file_id)