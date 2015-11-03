## Cosmo code.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#  This scipt displays the outputs of the CRN code that calculates denudation rates from 
#  cosmogenic concentration rates with other code outputs such as CRONUS. 
#  The user needs to prepare a csv table containing the different erosion rates 
#  and their errors.

## Marie-Alice Harel - 2014
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas
from scipy.stats import gaussian_kde

def make_plots():
    
    label_size = 20
    axis_size = 26

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size
    
    #************** USER'S CHOICE********************************#
    
    safi = 1      # Save figures as png (1 to save, otherwise 0):
    zoom = 1  # zoom in plots activated if value is 1
    SaveDirectory = 't:\\Topo_Data\\'  # Where the figures will be saved
    
    #***********************************************************#    
    
    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    data = pandas.read_csv('comp-cosmo-code.csv')
    
    # convert errors in mm/kyr
    data['error_newcode'] = data['error_newcode']*(1e7)/2650
    data['error_cosmocalc'] = data['error_cosmocalc']*(1e7)/2650
    
    # Exctracting the number of zones in the data
    lengzonall = len(data)
    all_list = []
    for zoo in range(1,lengzonall-1):
        if data.zone[zoo]-data.zone[zoo+1] != 0:
           all_list.append(int(data.zone[zoo]))   
    all_list.append(int(data.zone[lengzonall-1])) 
    print "Zones being compared = " +str(all_list)

    #########################
    #                       #
    #      MAKE PLOTS       #
    #                       #
    #########################    
    linetest = range(0,int(np.max(data['my_erate']))+50)
    cmap = plt.cm.jet
    
    
    # FIGURE 1 = ERATE COMPARED TO ERATE
    plt.figure(1, facecolor='white',figsize=(25,10))  

    # Plot 1 = comparison new_code / cosmocalc
    ax = plt.subplot(1,3,1)
    colo = 0   
    for zz in all_list:
        colo = colo + (1.000/len(all_list))
        datazz = data[(data.zone == zz)].copy()
        plt.plot(datazz['erate_cosmocalc']*10, datazz['erate_cmperkyr']*10, "o", markersize=8, color=cmap(colo), label = 'zone '+str(zz))
        plt.errorbar(datazz['erate_cosmocalc']*10, datazz['erate_cmperkyr']*10, xerr=datazz['error_cosmocalc'], yerr=datazz['error_newcode'], fmt='o',color = cmap(colo))
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('erate_COSMOCALC', fontsize = axis_size-2)
    plt.ylabel('erate_NEWCODE_mmperkyr', fontsize = axis_size-2)
    plt.plot(linetest, linetest,color='Grey', label = 'y=x')
    if zoom ==1:
        plt.axis([0, 500, 0, 500])
    plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, numpoints = 1, loc='upper left')
    
    # Plot 2 = comparison new_code / cronus
    ax = plt.subplot(1,3,2)
    colo = 0
    for zz in all_list:
        colo = colo + (1.000/len(all_list))
        datazz = data[(data.zone == zz)].copy()
        plt.plot(datazz['erate_cronus'], datazz['erate_cmperkyr']*10, "o", markersize=8, color=cmap(colo), label = 'zone '+str(zz))
        plt.errorbar(datazz['erate_cronus'], datazz['erate_cmperkyr']*10, xerr=datazz['error_cronus'], yerr=datazz['error_newcode'], fmt='o',color = cmap(colo))
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('erate_CRONUS', fontsize = axis_size-2)
    plt.ylabel('erate_NEWCODE_mmperkyr', fontsize = axis_size-2)
    plt.plot(linetest, linetest,color='Grey', label = 'y=x')
    if zoom ==1:
        plt.axis([0, 500, 0, 500])
    plt.title('Cronus / New_code',fontsize = label_size+6)
            
    # Plot 3 = comparison new_code / my_data
    ax = plt.subplot(1,3,3)
    colo = 0
    for zz in all_list:
        colo = colo + (1.000/len(all_list))
        datazz = data[(data.zone == zz)].copy()
        plt.plot(datazz['my_erate'], datazz['erate_cmperkyr']*10, "o", markersize=8, color=cmap(colo), label = 'zone '+str(zz))
        plt.errorbar(datazz['my_erate'], datazz['erate_cmperkyr']*10, xerr=datazz['error_myerate'], yerr=datazz['error_newcode'], fmt='o',color = cmap(colo))
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('my_erate', fontsize = axis_size-2)
    plt.ylabel('erate_NEWCODE_mmperkyr', fontsize = axis_size-2)
    plt.plot(linetest, linetest,color='Grey', label = 'y=x')
    if zoom ==1:
        plt.axis([0, 500, 0, 500])
    plt.title('My_data / New_code',fontsize = label_size+6)
    plt.tight_layout()
    
    if safi == 1:
        if zoom ==1:
            plt.savefig(SaveDirectory+'fig_cosmo_comparison_zoom.png') 
        else:
            plt.savefig(SaveDirectory+'fig_cosmo_comparison.png') 
        
        
    # FIGURE 2 = DIFFERENCE IN ERATE COMPARED TO ERATE
    plt.figure(2, facecolor='white',figsize=(25,10))  

    # Plot 1 = error new_code / cosmocalc
    ax = plt.subplot(1,3,1)
    colo = 0   
    for zz in all_list:
        colo = colo + (1.000/len(all_list))
        datazz = data[(data.zone == zz)].copy()
        plt.plot(datazz['erate_cmperkyr']*10,(datazz['erate_cosmocalc']-datazz['erate_cmperkyr'])*100/datazz['erate_cmperkyr'], "o", markersize=8, color=cmap(colo), label = 'zone '+str(zz))
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('erate_NEWCODE_mmperkyr', fontsize = axis_size-2)
    plt.ylabel('COSMOCALC-NEWCODE/NEWCODE (%)', fontsize = axis_size-2)
    plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    plt.axis([0, 5000, 0, 0.06])
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, numpoints = 1, loc='upper left')
    
    # Plot 2 = error new_code / cronus
    ax = plt.subplot(1,3,2)
    colo = 0
    for zz in all_list:
        colo = colo + (1.000/len(all_list))
        datazz = data[(data.zone == zz)].copy()
        plt.plot(datazz['erate_cmperkyr']*10,(datazz['erate_cronus']-datazz['erate_cmperkyr']*10)*10/datazz['erate_cmperkyr'], "o", markersize=8, color=cmap(colo), label = 'zone '+str(zz))
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('erate_NEWCODE_mmperkyr', fontsize = axis_size-2)
    plt.ylabel('CRONUS-NEWCODE/NEWCODE (%)', fontsize = axis_size-2)
    plt.title('Cronus / New_code',fontsize = label_size+6)
    plt.axis([0,5000, 0, 50])
           
    # Plot 3 = error new_code / my_data
    ax = plt.subplot(1,3,3)
    colo = 0
    for zz in all_list:
        colo = colo + (1.000/len(all_list))
        datazz = data[(data.zone == zz)].copy()
        plt.plot(datazz['erate_cmperkyr']*10,(datazz['my_erate']-datazz['erate_cmperkyr']*10)*10/datazz['erate_cmperkyr'], "o", markersize=8, color=cmap(colo), label = 'zone '+str(zz))
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('erate_NEWCODE_mmperkyr', fontsize = axis_size-2)
    plt.ylabel('MYDATA-NEWCODE/NEWCODE (%)', fontsize = axis_size-2)
    plt.title('My_data / New_code',fontsize = label_size+6)
    plt.axis([0, 3000, 0, 100])
    plt.tight_layout()
    plt.suptitle('ERROR / erate',fontsize = label_size+6)

    
    if safi == 1:
            plt.savefig(SaveDirectory+'fig_cosmo_ERROR_erate.png') 
            

    # FIGURE 3 = DIFFERENCE IN ERATE COMPARED TO RELIEF
    plt.figure(3, facecolor='white',figsize=(25,10))  

    # Plot 1 = error new_code / cosmocalc
    ax = plt.subplot(1,3,1)
    colo = 0   
    for zz in all_list:
        colo = colo + (1.000/len(all_list))
        datazz = data[(data.zone == zz)].copy()
        plt.plot(datazz['relief'],(datazz['erate_cosmocalc']-datazz['erate_cmperkyr'])*100/datazz['erate_cmperkyr'], "o", markersize=8, color=cmap(colo), label = 'zone '+str(zz))
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('Relief (m)', fontsize = axis_size-2)
    plt.ylabel('COSMOCALC-NEWCODE/NEWCODE (%)', fontsize = axis_size-2)
    plt.title('Cosmocalc / New_code',fontsize = label_size+6)
    plt.axis([0, 6000, 0, 0.035])
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels, numpoints = 1, loc='upper left')
    
    # Plot 2 = error new_code / cronus
    ax = plt.subplot(1,3,2)
    colo = 0
    for zz in all_list:
        colo = colo + (1.000/len(all_list))
        datazz = data[(data.zone == zz)].copy()
        plt.plot(datazz['relief'],(datazz['erate_cronus']-datazz['erate_cmperkyr']*10)*10/datazz['erate_cmperkyr'], "o", markersize=8, color=cmap(colo), label = 'zone '+str(zz))
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('Relief (m)', fontsize = axis_size-2)
    plt.ylabel('CRONUS-NEWCODE/NEWCODE (%)', fontsize = axis_size-2)
    plt.title('Cronus / New_code',fontsize = label_size+6)
    plt.axis([0,6000, 0, 35])
           
    # Plot 3 = error new_code / my_data
    ax = plt.subplot(1,3,3)
    colo = 0
    for zz in all_list:
        colo = colo + (1.000/len(all_list))
        datazz = data[(data.zone == zz)].copy()
        plt.plot(datazz['relief'],(datazz['my_erate']-datazz['erate_cmperkyr']*10)*10/datazz['erate_cmperkyr'], "o", markersize=8, color=cmap(colo), label = 'zone '+str(zz))
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('Relief (m)', fontsize = axis_size-2)
    plt.ylabel('MYDATA-NEWCODE/NEWCODE (%)', fontsize = axis_size-2)
    plt.title('My_data / New_code',fontsize = label_size+6)
    plt.axis([0, 6000, 0, 100])
    plt.tight_layout()
    plt.suptitle('ERROR / Relief',fontsize = label_size+6)

    
    if safi == 1:
            plt.savefig(SaveDirectory+'fig_cosmo_ERROR_relief.png') 
                    
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    print 'Done.'
    plt.show()
      

if __name__ == "__main__":
    make_plots()