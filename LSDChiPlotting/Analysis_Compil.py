## Analysis_Compil.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This script displays the results contained in the compil-data-MAH.csv 
## table. Relationships between chi-plot parameters, erosion rates and 
## environmental parameters (temperature, precipitation, % vegetation ...)
## are displayed. The user needs to specify the filter for the data, and 
## the figures output. 
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## Marie-Alice Harel - June 2014
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy import stats
import csv
import pandas
from scipy.stats import gaussian_kde

def make_plots():
    
    label_size = 20
    #title_size = 30
    axis_size = 28

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size
    
    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    # Choose dataset
    #=============================
    #datach = 1   # all data + trustworthy
    datach = 2   # fixed m/n

    # Save figures as png (1 to save, otherwise 0):
    #==============================
    safi = 1
    
    # Extra figures :
    bonus = 0
    
    # Where you want to save the figures:
    SaveDirectory = 't:\\Topo_Data\\post-traitement\\'
    
    # Color map choice :
    #==============================
    my_cmap = plt.cm.Blues    # for Greys or Blues
    #my_cmap = None            # for colors
    
    
    # Load the data into a DataFrame
    if datach == 1:
        data = pandas.read_csv('compil-data-MAH.csv')
    elif datach == 2:
        data = pandas.read_csv('fixed_movern_trustworthy.csv')
    data.info()
    
    # Filtering of data : 
    #====================
    
    # Choose a filter :
    #--------------------
    #   1 = realistic n and K
    #   2 = trustworthy n and K (visual on log-log)
    #   3 = area of basins
    #   4 = non-NAN m/n value (for PDF figure)
    #   5 = Selection of a parameter

    filtr = 5
    
    
    # FILTER 1  = realistic values of n and K
    if filtr==1:
        dataff = data[(data.zone == 8) & (data.zone ==31) & (data.zone == 64)].copy()
        selectitl = 'Zones 8, 31 and 64'
        
    # FILTER 2  = climate sub-group
    elif filtr==2:
        dataff = data[(data.zone > 0.1)].copy()
        dataf = data[(data.p_loglog_linregress <= 0.1)].copy()
        dataff = dataf[(dataf.clim==5)]
        selectitl = 'Polar trustworthy climate'       
    
    # FILTER 3  = area above threshold
    elif filtr==3:
        dataff = data[(data.zone > 0.1)].copy()
        dataff = data[(data.area > 15e6)].copy()
        selectitl = 'Area above 15km^2'
        
    # FILTER 4  = non-NAN m/n value (for PDF figure)
    elif filtr==4:
        dataff = data[(data.zone > 0.1)].copy()
        dataff = data[(0.5<data.m_over_n) &(data.m_over_n <0.6)].copy()
        selectitl = '0.5< m/n <0.6'
        
    # FILTER 5  = Selection of a specific parameter value
    elif filtr==5:
        dataff = data[(data.zone > 0.1)].copy()
        dataff = data[(data.p_loglog_linregress <= 0.1)].copy()
        selectitl = 'p<=0.1 data'        
        
    # FILTER 6  = Rock type
    elif filtr==6:
        dataff = data[(data.rock==4)]
        selectitl = 'Mixed rocks'           
    
    else:
        print "Check the value of the filter."
        
    
    # Definition of the variables according to selected filter
    #----------------------------------------------------------
    
    # Selection of granite lithology (with and without filter)
    data_granite = data[(data.litho >= 1)].copy()
    data_graniteff = dataff[(dataff.litho >= 1)].copy()
    
    # Selection of areas with tectonic activity (see Portenga and Bierman for def)
    data_active = data[(data.activity == 1)].copy()
    data_activeff = dataff[(dataff.activity == 1)].copy()  
    
    # The following terminaisons stand for :
    #    a = active tectonics
    #    g = granite
    #    ff = filtered data
    
    y_n = data['n'] 
    y_n_a = data_active['n']
    y_n_g = data_granite['n']
    y_n_ff = dataff['n']
    y_n_ff_a = data_activeff['n']    
    y_n_ff_g = data_graniteff['n']
    
    y_K = data['K'] 
    y_K_g = data_granite['K']
    y_K_a = data_active['K']
    y_K_ff = dataff['K'] 
    y_K_ff_g = data_graniteff['K'] 
    y_K_ff_a = data_activeff['K'] 
    
    y_mn = data['m_over_n'] 
    y_mn_g = data_granite['m_over_n']
    y_mn_a = data_active['m_over_n']
    y_mn_ff = dataff['m_over_n']
    y_mn_ff_g = data_graniteff['m_over_n'] 
    y_mn_ff_a = data_activeff['m_over_n'] 
    
    x_erate = data['erate']
    x_erate_g = data_granite['erate']
    x_erate_a = data_active['erate']
    x_erate_log = np.log10(x_erate)
    x_erate_log_a = np.log10(data_active['erate'])
    x_erate_log_g = np.log10(data_granite['erate'])
    x_erate_ff = dataff['erate']
    x_erate_ff_a = data_activeff['erate']
    x_erate_ff_g = data_graniteff['erate']
    x_erate_ff_log = np.log10(x_erate_ff)
    x_erate_ff_log_a = np.log10(data_activeff['erate'])
    x_erate_ff_log_g = np.log10(data_graniteff['erate'])

    
    x_rock = data['rock']
    x_rock_g = data_granite['rock']
    x_rock_a = data_active['rock']
    x_rock_ff = dataff['rock']
    x_rock_ff_g = data_graniteff['rock']
    x_rock_ff_a = data_activeff['rock']    
    
    x_temp = data['MAT']
    x_temp_g = data_granite['MAT']
    x_temp_a = data_active['MAT']
    x_temp_ff = dataff['MAT']
    x_temp_ff_g = data_graniteff['MAT']
    x_temp_ff_a = data_activeff['MAT']
    
    x_precip = data['MAP']
    x_precip_g = data_granite['MAP']
    x_precip_a = data_active['MAP']
    x_precip_ff = dataff['MAP']
    x_precip_ff_g = data_graniteff['MAP']
    x_precip_ff_a = data_activeff['MAP']    
    
    x_eleva = data['elevation']
    x_eleva_g = data_granite['elevation']
    x_eleva_a = data_active['elevation']
    x_eleva_ff = dataff['elevation']
    x_eleva_ff_g = data_graniteff['elevation']
    x_eleva_ff_a = data_activeff['elevation']    

    x_lat = data['Latitude']
    x_lat_g = data_granite['Latitude']
    x_lat_a = data_active['Latitude']
    x_lat_ff = dataff['Latitude']
    x_lat_ff_g = data_graniteff['Latitude']
    x_lat_ff_a = data_activeff['Latitude']
    
    x_veg = data['vegetation']
    x_veg_g = data_granite['vegetation']
    x_veg_a = data_active['vegetation']
    x_veg_ff = dataff['vegetation']
    x_veg_ff_g = data_graniteff['vegetation']
    x_veg_ff_a = data_activeff['vegetation']

    x_sei = data['seismicity']
    x_sei_g = data_granite['seismicity']
    x_sei_a = data_active['seismicity']
    x_sei_ff = dataff['seismicity']
    x_sei_ff_g = data_graniteff['seismicity']
    x_sei_ff_a = data_activeff['seismicity']

    x_area = data['area']
    x_area_g = data_granite['area']
    x_area_a = data_active['area']    
    x_area_ff = dataff['area']
    x_area_ff_g = data_graniteff['area']
    x_area_ff_a = data_activeff['area']
    
    x_mchisl = data['Mean_chi_slope']
    x_mchisl_g = data_granite['Mean_chi_slope']
    x_mchisl_a = data_active['Mean_chi_slope']
    x_mchisl_ff = dataff['Mean_chi_slope']
    x_mchisl_ff_g = data_graniteff['Mean_chi_slope']
    x_mchisl_ff_a = data_activeff['Mean_chi_slope']
    
    x_clim = data['clim']
    x_clim_g = data_granite['clim']
    x_clim_a = data_active['clim']
    x_clim_ff = dataff['clim']
    x_clim_ff_g = data_graniteff['clim']
    x_clim_ff_a = data_activeff['clim']    
    
    
    # Definition of variables for climate zones
    #-------------------------------------------
    
    data_arid = data[(data.clim == 1)]
    data_tropical = data[(data.clim == 2)]
    data_temperate = data[(data.clim == 3)]
    data_cold = data[(data.clim == 4)]
    data_polar = data[(data.clim == 5)]
    
    data_aridff = dataff[(dataff.clim == 1)]
    data_tropicalff = dataff[(dataff.clim == 2)]
    data_temperateff = dataff[(dataff.clim == 3)]
    data_coldff = dataff[(dataff.clim == 4)]
    data_polarff = dataff[(dataff.clim == 5)]

    # Mean steepness
    x_mchisl_arid = data_arid['Mean_chi_slope']
    x_mchisl_tropical = data_tropical['Mean_chi_slope']
    x_mchisl_temperate = data_temperate['Mean_chi_slope']
    x_mchisl_cold = data_cold['Mean_chi_slope']
    x_mchisl_polar = data_polar['Mean_chi_slope']
    x_mchisl_arid_ff = data_aridff['Mean_chi_slope']
    x_mchisl_tropical_ff = data_tropicalff['Mean_chi_slope']
    x_mchisl_temperate_ff = data_temperateff['Mean_chi_slope']
    x_mchisl_cold_ff = data_coldff['Mean_chi_slope']
    x_mchisl_polar_ff = data_polarff['Mean_chi_slope']
    
    # erosion rate
    x_erate_arid = data_arid['erate']
    x_erate_tropical = data_tropical['erate']
    x_erate_temperate = data_temperate['erate']
    x_erate_cold = data_cold['erate']
    x_erate_polar = data_polar['erate']
    x_erate_arid_ff = data_aridff['erate']
    x_erate_tropical_ff = data_tropicalff['erate']
    x_erate_temperate_ff = data_temperateff['erate']
    x_erate_cold_ff = data_coldff['erate']
    x_erate_polar_ff = data_polarff['erate']
                 
    # Precipitation
    x_precip_arid_ff = data_aridff['MAP']
    x_precip_tropical_ff = data_tropicalff['MAP']
    x_precip_temperate_ff = data_temperateff['MAP']
    x_precip_cold_ff = data_coldff['MAP']
    x_precip_polar_ff = data_polarff['MAP']
    
    # Temperature
    x_temp_arid_ff = data_aridff['MAT']
    x_temp_tropical_ff = data_tropicalff['MAT']
    x_temp_temperate_ff = data_temperateff['MAT']
    x_temp_cold_ff = data_coldff['MAT']
    x_temp_polar_ff = data_polarff['MAT']
                 
    # m over n 
    y_mn_arid = data_arid['m_over_n']
    y_mn_tropical = data_tropical['m_over_n']
    y_mn_temperate = data_temperate['m_over_n']
    y_mn_cold = data_cold['m_over_n']
    y_mn_polar = data_polar['m_over_n']

    y_mn_arid_ff = data_aridff['m_over_n']
    y_mn_tropical_ff = data_tropicalff['m_over_n']
    y_mn_temperate_ff = data_temperateff['m_over_n']
    y_mn_cold_ff = data_coldff['m_over_n']
    y_mn_polar_ff = data_polarff['m_over_n']

    # n 
    y_n_arid = data_arid['n']
    y_n_tropical = data_tropical['n']
    y_n_temperate = data_temperate['n']
    y_n_cold = data_cold['n']
    y_n_polar = data_polar['n']

    y_n_arid_ff = data_aridff['n']
    y_n_tropical_ff = data_tropicalff['n']
    y_n_temperate_ff = data_temperateff['n']
    y_n_cold_ff = data_coldff['n']
    y_n_polar_ff = data_polarff['n']
    
    # K
    y_K_arid = data_arid['K']
    y_K_tropical = data_tropical['K']
    y_K_temperate = data_temperate['K']
    y_K_cold = data_cold['K']
    y_K_polar = data_polar['K']

    y_K_arid_ff = data_aridff['K']
    y_K_tropical_ff = data_tropicalff['K']
    y_K_temperate_ff = data_temperateff['K']
    y_K_cold_ff = data_coldff['K']
    y_K_polar_ff = data_polarff['K']
    #########################
    #                       #
    #      MAKE PLOTS       #
    #                       #
    #########################    

    maxn = np.max(dataff['n']) +1
    maxK = np.max(dataff['K'])
    #maxK = 1e-5
    maxmn = np.max(data['m_over_n']) +0.1
    maxarea = np.max(np.log10(data['area']))
    minarea = np.min(np.log10(data['area']))

    if bonus ==1 :
            
        # EROSION RATE PLOTS (LOG)
        #==========================
    
        # n = f(LOG Erate) 
        #--------------------------    
        
        plt.figure(1, facecolor='white',figsize=(16,20))  
        
        ax = plt.subplot(3,2,5)
        plt.plot(x_erate_log, y_n, "o", markersize=8, color='b')
        plt.plot(x_erate_log_g, y_n_g, "o", markersize=8, color='r')
        plt.plot(x_erate_log_a, y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG (Erosion rate)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
    
        ax = plt.subplot(3,2,6)
        plt.plot(x_erate_ff_log, y_n_ff, "o", markersize=8, color='b')
        plt.plot(x_erate_ff_log_g, y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(x_erate_ff_log_a, y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG (Erosion rate)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title(selectitl, fontsize = label_size)
        plt.suptitle('LOG EROSION RATE',fontsize = label_size)
        
        # m/n = f(LOG Erate) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        plt.plot(x_erate_log, y_mn, "o", markersize=8, color='b')
        plt.plot(x_erate_log_g, y_mn_g, "o", markersize=8, color='r')
        plt.plot(x_erate_log_a, y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('LOG (Erosion rate)', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
    
        ax = plt.subplot(3,2,4)
        plt.plot(x_erate_ff_log, y_mn_ff, "o", markersize=8, color='b')
        plt.plot(x_erate_ff_log_g, y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(x_erate_ff_log_a, y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('LOG (Erosion rate)', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title(selectitl, fontsize = label_size)
        
    
        # K = f(LOG Erate) 
        #--------------------------    
        
        ax = plt.subplot(3,2,1)
        plt.plot(x_erate_log, np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(x_erate_log_g, np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(x_erate_log_a, np.log10(y_K_a), "+", markersize=8, color='w')
        #ax.errorbar(x1,y2, xerr=data['erate_sigma'], yerr=data['Std_K'], fmt='o')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K', fontsize = label_size)
        #plt.axis([0, 9, 0, maxK])
    
           
        ax = plt.subplot(3,2,2)
        plt.plot(x_erate_ff_log, np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(x_erate_ff_log_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(x_erate_ff_log_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title(selectitl, fontsize = label_size)
        #plt.axis([0, 9, 0, maxK])
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_LOG_ERATE.png') 

    
        # SEISMICITY PLOTS
        #==========================
        
        # n = f(SEISMICITY) 
        #--------------------------    
        
        plt.figure(2, facecolor='white',figsize=(16,20))  
        
        ax = plt.subplot(3,2,5)
        plt.plot(x_sei, y_n, "o", markersize=8, color='b')
        plt.plot(x_sei_g, y_n_g, "o", markersize=8, color='r')
        plt.plot(x_sei_a, y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('seismicity', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
    
        ax = plt.subplot(3,2,6)
        plt.plot(x_sei_ff, y_n_ff, "o", markersize=8, color='b')
        plt.plot(x_sei_ff_g, y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(x_sei_ff_a, y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('seismicity', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title(selectitl, fontsize = label_size)
        plt.suptitle('SEISMICITY',fontsize = label_size)
        
        # m/n = f(LOG Erate) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        plt.plot(x_sei, y_mn, "o", markersize=8, color='b')
        plt.plot(x_sei_g, y_mn_g, "o", markersize=8, color='r')
        plt.plot(x_sei_a, y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
    
        ax = plt.subplot(3,2,4)
        plt.plot(x_sei_ff, y_mn_ff, "o", markersize=8, color='b')
        plt.plot(x_sei_ff_g, y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(x_sei_ff_a, y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title(selectitl, fontsize = label_size)
        
    
        # K = f(LOG Erate) 
        #--------------------------    
        
        ax = plt.subplot(3,2,1)
        plt.plot(x_sei, np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(x_sei_g, np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(x_sei_a, np.log10(y_K_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K', fontsize = label_size)
        #plt.axis([0, 9, 0, maxK])
    
           
        ax = plt.subplot(3,2,2)
        plt.plot(x_sei_ff, np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(x_sei_ff_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(x_sei_ff_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title(selectitl, fontsize = label_size)
        #plt.axis([0, 9, 0, maxK])
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_SEISMICITY.png') 
            
    
    
        # ROCK TYPE PLOTS
        #====================
        
        # K = f(Rock_type) 
        #--------------------------    
        
        plt.figure(3, facecolor='white',figsize=(16,20))    
        
        ax = plt.subplot(3,2,1)
        plt.plot(x_rock, np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(x_rock_g, np.log10(y_K_g), "o", markersize=8, color='r')   
        plt.plot(x_rock_a, np.log10(y_K_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K)', fontsize = label_size)
        plt.axis([0, 5, 0, np.log10(maxK)])
        #plt.legend( ('all data', 'granite'), loc='upper left', numpoints = 1)
        plt.suptitle('1=Igneous / 2=Sedimentary / 3=Metamorphic / 4=Mixed',fontsize = label_size)
        
        ax = plt.subplot(3,2,2)
        plt.plot(x_rock_ff, np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(x_rock_ff_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(x_rock_ff_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.axis([0, 5, 0, np.log10(maxK)])
        plt.title(selectitl, fontsize = label_size)
        
        
        # m/n = f(Rock_type) 
        #--------------------------    
           
        ax = plt.subplot(3,2,3)
        plt.plot(x_rock, y_mn, "o", markersize=8, color='b')
        plt.plot(x_rock_g, y_mn_g, "o", markersize=8, color='r')
        plt.plot(x_rock_a, y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Rock type', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        plt.axis([0, 5, 0, maxmn])
        
        ax = plt.subplot(3,2,4)
        plt.plot(x_rock_ff, y_mn_ff, "o", markersize=8, color='b')
        plt.plot(x_rock_ff_g, y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(x_rock_ff_a, y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Rock type', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.axis([0, 5, 0, maxmn])
        plt.title(selectitl, fontsize = label_size)
        
        
        # n = f(Rock_type) 
        #-------------------------- 
        ax = plt.subplot(3,2,5)
        plt.plot(x_rock, y_n, "o", markersize=8, color='b')
        plt.plot(x_rock_g, y_n_g, "o", markersize=8, color='r')
        plt.plot(x_rock_a, y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Rock type', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        plt.axis([0, 5, -60, maxn])
    
        
        ax = plt.subplot(3,2,6)
        plt.plot(x_rock_ff, y_n_ff, "o", markersize=8, color='b')
        plt.plot(x_rock_ff_g, y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(x_rock_ff_a, y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Rock type', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.axis([0, 5, 0, maxn])
        plt.title(selectitl, fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_ROCK.png') 
        
        
        # PRECIPITATION PLOTS
        #======================    
        
        # K = f(MAP) 
        #--------------------------  
        
        plt.figure(4, facecolor='white',figsize=(16,20))    
        ax = plt.subplot(3,2,1)
        plt.plot(x_precip, np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(x_precip_g, np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(x_precip_a, np.log10(y_K_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K', fontsize = label_size)
        #plt.axis([0, 3100, 0, maxK])
        plt.suptitle('MEAN ANNUAL PRECIPITATION',fontsize = label_size)
        
        ax = plt.subplot(3,2,2)
        plt.plot(x_precip_ff, np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(x_precip_ff_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(x_precip_ff_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        #plt.axis([0, 3100, 0, maxK])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend( ('all data', 'granite'), loc='upper right', numpoints = 1)
    
    
        # m/n = f(MAP) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        
        plt.plot(x_precip, y_mn, "o", markersize=8, color='b')
        plt.plot(x_precip_g, y_mn_g, "o", markersize=8, color='r')
        plt.plot(x_precip_a, y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        plt.axis([0, 3100, 0, maxmn])
    
        
        ax = plt.subplot(3,2,4)
        plt.plot(x_precip_ff, y_mn_ff, "o", markersize=8, color='b')
        plt.plot(x_precip_ff_g, y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(x_precip_ff_a, y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.axis([0, 3100, 0, maxmn])
        plt.title(selectitl, fontsize = label_size)
        
        # n = f(MAP) 
        #--------------------------    
        ax = plt.subplot(3,2,5)
        
        plt.plot(x_precip, y_n, "o", markersize=8, color='b')
        plt.plot(x_precip_g, y_n_g, "o", markersize=8, color='r')
        plt.plot(x_precip_a, y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Mean Annual Precipitation (mm/yr)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([0, 3100, -60, 82])
        
        ax = plt.subplot(3,2,6)
        plt.plot(x_precip_ff, y_n_ff, "o", markersize=8, color='b')
        plt.plot(x_precip_ff_g, y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(x_precip_ff_a, y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Mean Annual Precipitation (mm/yr)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.axis([0, 3100, 0, maxn])
        plt.title(selectitl, fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_MAP.png') 
    
    
    
        # ELEVATION PLOTS
        #======================    
        
        # K = f(ELEVATION) 
        #--------------------------  
        
        plt.figure(5, facecolor='white',figsize=(16,20))    
        ax = plt.subplot(3,2,1)
        plt.plot(x_eleva, np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(x_eleva_g, np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(x_eleva_a,np.log10(y_K_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K', fontsize = label_size)
        #plt.axis([0, 3100, 0, maxK])
        plt.suptitle('ELEVATION',fontsize = label_size)
        
        ax = plt.subplot(3,2,2)
        plt.plot(x_eleva_ff, np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(x_eleva_ff_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(x_eleva_ff_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        #plt.axis([0, 3100, 0, maxK])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend( ('all data', 'granite'), loc='upper right', numpoints = 1)
    
    
        # m/n = f(ELEVATION) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        
        plt.plot(x_eleva, y_mn, "o", markersize=8, color='b')
        plt.plot(x_eleva_g, y_mn_g, "o", markersize=8, color='r')
        plt.plot(x_eleva_a, y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        plt.axis([0, 3100, 0, maxmn])
    
        
        ax = plt.subplot(3,2,4)
        plt.plot(x_eleva_ff, y_mn_ff, "o", markersize=8, color='b')
        plt.plot(x_eleva_ff_g, y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(x_eleva_ff_a, y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.axis([0, 3100, 0, maxmn])
        plt.title(selectitl, fontsize = label_size)
        
        # n = f(ELEVATION) 
        #--------------------------    
        ax = plt.subplot(3,2,5)
        
        plt.plot(x_eleva, y_n, "o", markersize=8, color='b')
        plt.plot(x_eleva_g, y_n_g, "o", markersize=8, color='r')
        plt.plot(x_eleva_a, y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Elevation (m)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([0, 3100, -60, 82])
        
        ax = plt.subplot(3,2,6)
        plt.plot(x_eleva_ff, y_n_ff, "o", markersize=8, color='b')
        plt.plot(x_eleva_ff_g, y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(x_eleva_ff_a, y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Elevation (m)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.axis([0, 3100, 0, maxn])
        plt.title(selectitl, fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_ELEVATION.png') 
    
    
    
             
        # TEMPERATURE PLOTS
        #======================    
        
        # K = f(MAT) 
        #--------------------------  
        
        plt.figure(6, facecolor='white',figsize=(16,20))   
        
        ax = plt.subplot(3,2,1)
        plt.plot(x_temp, np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(x_temp_g, np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(x_temp_a, np.log10(y_K_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K', fontsize = label_size)
        #plt.axis([-6, 26, 0, maxK])
        plt.suptitle('MEAN ANNUAL TEMPERATURE',fontsize = label_size)
        
        ax = plt.subplot(3,2,2)
        plt.plot(x_temp_ff,np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(x_temp_ff_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(x_temp_ff_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        #plt.axis([-6, 26, 0, maxK])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend(('all data', 'granite'), loc='upper right', numpoints = 1)
    
        # m/n = f(MAT) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        plt.plot(x_temp, y_mn, "o", markersize=8, color='b')
        plt.plot(x_temp_g, y_mn_g, "o", markersize=8, color='r')
        plt.plot(x_temp_a, y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        plt.axis([-6, 26, 0, maxmn])
    
        
        ax = plt.subplot(3,2,4)
        plt.plot(x_temp_ff, y_mn_ff, "o", markersize=8, color='b')
        plt.plot(x_temp_ff_g, y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(x_temp_ff_a, y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.axis([-6, 26, 0, maxmn])
        plt.title(selectitl, fontsize = label_size)
        
        # n = f(MAT) 
        #--------------------------    
        ax = plt.subplot(3,2,5)
        plt.plot(x_temp, y_n, "o", markersize=8, color='b')
        plt.plot(x_temp_g, y_n_g, "o", markersize=8, color='r')
        plt.plot(x_temp_a, y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Mean Annual Temperature (C)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([-6, 26, -60, 82])
        
        ax = plt.subplot(3,2,6)
        plt.plot(x_temp_ff, y_n_ff, "o", markersize=8, color='b')
        plt.plot(x_temp_ff_g, y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(x_temp_ff_a, y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Mean Annual Temperature (C)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.axis([-6, 26, 0, maxn])
        plt.title(selectitl, fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_MAT.png')          
            
             
        # LATITUDE PLOTS
        #======================    
        
        # K = f(Lat) 
        #--------------------------  
        
        plt.figure(7, facecolor='white',figsize=(16,20))   
        
        ax = plt.subplot(3,2,1)
        plt.plot(x_lat, np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(x_lat_g, np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(x_lat_a, np.log10(y_K_a), "+", markersize=8, color='w')    
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K', fontsize = label_size)
        #plt.axis([-40, 60, 0, maxK])
        plt.suptitle('LATITUDE',fontsize = label_size)
        
        ax = plt.subplot(3,2,2)
        plt.plot(x_lat_ff, np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(x_lat_ff_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(x_lat_ff_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        #plt.axis([-40, 60, 0, maxK])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend(('all data', 'granite'), loc='upper left', numpoints = 1)
    
        # m/n = f(lat) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        plt.plot(x_lat, y_mn, "o", markersize=8, color='b')
        plt.plot(x_lat_g, y_mn_g, "o", markersize=8, color='r')
        plt.plot(x_lat_a, y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        plt.axis([-40, 60, 0, maxmn])
    
        
        ax = plt.subplot(3,2,4)
        plt.plot(x_lat_ff, y_mn_ff, "o", markersize=8, color='b')
        plt.plot(x_lat_ff_g, y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(x_lat_ff_a, y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.axis([-40, 60, 0, maxmn])
        plt.title(selectitl, fontsize = label_size)
        
        # n = f(lat) 
        #--------------------------    
        ax = plt.subplot(3,2,5)
        plt.plot(x_lat, y_n, "o", markersize=8, color='b')
        plt.plot(x_lat_g, y_n_g, "o", markersize=8, color='r')
        plt.plot(x_lat_a, y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Latitude', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([-40, 60, -60, 82])
        
        ax = plt.subplot(3,2,6)
        plt.plot(x_lat_ff, y_n_ff, "o", markersize=8, color='b')
        plt.plot(x_lat_ff_g, y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(x_lat_ff_a, y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Latitude', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.axis([-40, 60, 0, maxn])
        plt.title(selectitl, fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_LATITUDE.png') 
            
          
        # VEGETATION PLOTS
        #======================    
        
        # K = f(vegetation) 
        #--------------------------  
        
        plt.figure(8, facecolor='white',figsize=(16,20))   
        
        ax = plt.subplot(3,2,1)
        plt.plot(x_veg, np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(x_veg_g, np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(x_veg_a, np.log10(y_K_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K', fontsize = label_size)
        #plt.axis([0, 100, 0, maxK])
        plt.suptitle('% VEGETATION',fontsize = label_size)
        
        ax = plt.subplot(3,2,2)
        plt.plot(x_veg_ff, np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(x_veg_ff_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(x_veg_ff_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        #plt.axis([0, 100, 0, maxK])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend(('all data', 'granite'), loc='upper left', numpoints = 1)
    
        # m/n = f(vegetation) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        plt.plot(x_veg, y_mn, "o", markersize=8, color='b')
        plt.plot(x_veg_g, y_mn_g, "o", markersize=8, color='r')
        plt.plot(x_veg_a, y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        plt.axis([0, 100, 0, maxmn])
    
        
        ax = plt.subplot(3,2,4)
        plt.plot(x_veg_ff, y_mn_ff, "o", markersize=8, color='b')
        plt.plot(x_veg_ff_g, y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(x_veg_ff_a, y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.axis([0, 100, 0, maxmn])
        plt.title(selectitl, fontsize = label_size)
        
        # n = f(vegetation) 
        #--------------------------    
        ax = plt.subplot(3,2,5)
        plt.plot(x_veg, y_n, "o", markersize=8, color='b')
        plt.plot(x_veg_g, y_n_g, "o", markersize=8, color='r')
        plt.plot(x_veg_a, y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('% Vegetation', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([0, 100, -60, 82])
        
        ax = plt.subplot(3,2,6)
        plt.plot(x_veg_ff, y_n_ff, "o", markersize=8, color='b')
        plt.plot(x_veg_ff_g, y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(x_veg_ff_a, y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('% Vegetation', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.axis([0, 100, 0, maxn])
        plt.title(selectitl, fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_VEGETATION.png') 
            
                
        #      AREA PLOTS
        #======================    
        
        # K = f(area) 
        #--------------------------  
        
        plt.figure(9, facecolor='white',figsize=(16,20))   
        
        ax = plt.subplot(3,2,1)
        plt.plot(np.log10(x_area), np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(np.log10(x_area_g), np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(np.log10(x_area_a), np.log10(y_K_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K', fontsize = label_size)
        #plt.axis([minarea, maxarea, 0, maxK])
        plt.suptitle('AREA',fontsize = label_size)
        
        ax = plt.subplot(3,2,2)
        plt.plot(np.log10(x_area_ff), np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(np.log10(x_area_ff_g), np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(np.log10(x_area_ff_a), np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        #plt.axis([minarea, maxarea, 0, maxK])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend(('all data', 'granite'), loc='upper left', numpoints = 1)
    
        # m/n = f(area) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        plt.plot(np.log10(x_area), y_mn, "o", markersize=8, color='b')
        plt.plot(np.log10(x_area_g), y_mn_g, "o", markersize=8, color='r')
        plt.plot(np.log10(x_area_a), y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        plt.axis([minarea, maxarea, 0, maxmn])
    
        
        ax = plt.subplot(3,2,4)
        plt.plot(np.log10(x_area_ff), y_mn_ff, "o", markersize=8, color='b')
        plt.plot(np.log10(x_area_ff_g), y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(np.log10(x_area_ff_a), y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.axis([minarea, maxarea, 0, maxmn])
        plt.title(selectitl, fontsize = label_size)
        
        # n = f(area) 
        #--------------------------    
        ax = plt.subplot(3,2,5)
        plt.plot(np.log10(x_area), y_n, "o", markersize=8, color='b')
        plt.plot(np.log10(x_area_g), y_n_g, "o", markersize=8, color='r')
        plt.plot(np.log10(x_area_a), y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Area (m2)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([minarea, maxarea, -60, 82])
        
        ax = plt.subplot(3,2,6)
        plt.plot(np.log10(x_area_ff), y_n_ff, "o", markersize=8, color='b')
        plt.plot(np.log10(x_area_ff_g), y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(np.log10(x_area_ff_a), y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Area (m2)', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.axis([minarea, maxarea, 0, maxn])
        plt.title(selectitl, fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_AREA.png') 
                
                      
        #  MEAN_CHI_SLOPE PLOTS
        #======================    
        
        # K = f(steepness) 
        #--------------------------  
        
        plt.figure(10, facecolor='white',figsize=(16,20))   
        
        ax = plt.subplot(3,2,1)
        plt.plot(x_mchisl, np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(x_mchisl_g, np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(x_mchisl_a, np.log10(y_K_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K', fontsize = label_size)
        #plt.axis([0, 18, 0, maxK])
        plt.suptitle('MEAN CHI SLOPE',fontsize = label_size)
        
        ax = plt.subplot(3,2,2)
        plt.plot(x_mchisl_ff, np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(x_mchisl_ff_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(x_mchisl_ff_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        #plt.axis([0, 18, 0, maxK])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend(('all data', 'granite'), loc='upper right', numpoints = 1)
    
        # m/n = f(steepness) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        plt.plot(x_mchisl, y_mn, "o", markersize=8, color='b')
        plt.plot(x_mchisl_g, y_mn_g, "o", markersize=8, color='r')
        plt.plot(x_mchisl_a, y_mn_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        plt.axis([0, 18, 0, maxmn])
    
        
        ax = plt.subplot(3,2,4)
        plt.plot(x_mchisl_ff, y_mn_ff, "o", markersize=8, color='b')
        plt.plot(x_mchisl_ff_g, y_mn_ff_g, "o", markersize=8, color='r')
        plt.plot(x_mchisl_ff_a, y_mn_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('m/n', fontsize = axis_size-2)
        plt.axis([0, 18, 0, maxmn])
        plt.title(selectitl, fontsize = label_size)
        
        # n = f(steepness) 
        #--------------------------    
        ax = plt.subplot(3,2,5)
        plt.plot(x_mchisl, y_n, "o", markersize=8, color='b')
        plt.plot(x_mchisl_g, y_n_g, "o", markersize=8, color='r')
        plt.plot(x_mchisl_a, y_n_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Mean chi slope', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([0, 18, -60, 82])
        
        ax = plt.subplot(3,2,6)
        plt.plot(x_mchisl_ff, y_n_ff, "o", markersize=8, color='b')
        plt.plot(x_mchisl_ff_g, y_n_ff_g, "o", markersize=8, color='r')
        plt.plot(x_mchisl_ff_a, y_n_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Mean chi slope', fontsize = axis_size-2)
        plt.ylabel('n', fontsize = axis_size-2)
        plt.axis([0, 18, 0, maxn])
        plt.title(selectitl, fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_STEEPNESS.png')            
                
                
        #  LOG-LOG MEAN_CHI_SLOPE PLOTS
        #======================    
        
        # LOG K = f(LOG steepness) 
        #--------------------------  
        
        plt.figure(11, facecolor='white',figsize=(16,20))   
        
        ax = plt.subplot(3,2,1)
        plt.plot(np.log10(x_mchisl), np.log10(y_K), "o", markersize=8, color='b')
        plt.plot(np.log10(x_mchisl_g), np.log10(y_K_g), "o", markersize=8, color='r')
        plt.plot(np.log10(x_mchisl_a), np.log10(y_K_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        plt.title('All K (except highest)', fontsize = label_size)
        #plt.axis([0, 18, 0, 26])
        plt.suptitle('LOG-LOG MEAN CHI SLOPE',fontsize = label_size)
        
        ax = plt.subplot(3,2,2)
        plt.plot(np.log10(x_mchisl_ff), np.log10(y_K_ff), "o", markersize=8, color='b')
        plt.plot(np.log10(x_mchisl_ff_g), np.log10(y_K_ff_g), "o", markersize=8, color='r')
        plt.plot(np.log10(x_mchisl_ff_a), np.log10(y_K_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.ylabel('LOG K', fontsize = axis_size-2)
        #plt.axis([0, 18, 0, 26])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend(('all data', 'granite'), loc='lower left', numpoints = 1)
    
        # LOG m/n = f(LOG steepness) 
        #--------------------------    
        
        ax = plt.subplot(3,2,3)
        plt.plot(np.log10(x_mchisl), np.log10(y_mn), "o", markersize=8, color='b')
        plt.plot(np.log10(x_mchisl_g), np.log10(y_mn_g), "o", markersize=8, color='r')
        plt.plot(np.log10(x_mchisl_a), np.log10(y_mn_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('LOG m/n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([0, 18, 0, 0.6])
    
        
        ax = plt.subplot(3,2,4)
        plt.plot(np.log10(x_mchisl_ff), np.log10(y_mn_ff), "o", markersize=8, color='b')
        plt.plot(np.log10(x_mchisl_ff_g), np.log10(y_mn_ff_g), "o", markersize=8, color='r')
        plt.plot(np.log10(x_mchisl_ff_a), np.log10(y_mn_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        #plt.xlabel('Mean Annual Precipitation', fontsize = axis_size-2)
        plt.ylabel('LOG m/n', fontsize = axis_size-2)
        #plt.axis([0, 18, 0, 0.6])
        plt.title(selectitl, fontsize = label_size)
        
        # LOG n = f(LOG steepness) 
        #--------------------------    
        ax = plt.subplot(3,2,5)
        plt.plot(np.log10(x_mchisl), np.log10(y_n), "o", markersize=8, color='b')
        plt.plot(np.log10(x_mchisl_g), np.log10(y_n_g), "o", markersize=8, color='r')
        plt.plot(np.log10(x_mchisl_a), np.log10(y_n_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Mean chi slope', fontsize = axis_size-2)
        plt.ylabel('LOG n', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([0, 18, -60, 82])
        
        ax = plt.subplot(3,2,6)
        plt.plot(np.log10(x_mchisl_ff), np.log10(y_n_ff), "o", markersize=8, color='b')
        plt.plot(np.log10(x_mchisl_ff_g), np.log10(y_n_ff_g), "o", markersize=8, color='r')
        plt.plot(np.log10(x_mchisl_ff_a), np.log10(y_n_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Mean chi slope', fontsize = axis_size-2)
        plt.ylabel('LOG n', fontsize = axis_size-2)
        #plt.axis([0, 18, 0, 3.6])
        plt.title(selectitl, fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_LOG_STEEPNESS.png')
            
                
        #   mean chi slope = f(erosion rate)
        #====================================== 
        plt.figure(12, facecolor='white',figsize=(20,15))   
        
        ax = plt.subplot(2,2,1)
        plt.plot(x_erate, x_mchisl, "o", markersize=8, color='b')
        plt.plot(x_erate_g, x_mchisl_g, "o", markersize=8, color='r')
        plt.plot(x_erate_a, x_mchisl_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Erosion rate (mm/kyr)', fontsize = axis_size-2)
        plt.ylabel('Mean Chi Slope', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([0, 18, 0, 26])
           
        ax = plt.subplot(2,2,2)
        plt.plot(x_erate_ff, x_mchisl_ff, "o", markersize=8, color='b')
        plt.plot(x_erate_ff_g, x_mchisl_ff_g, "o", markersize=8, color='r')
        plt.plot(x_erate_ff_a, x_mchisl_ff_a, "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Erosion rate (mm/kyr)', fontsize = axis_size-2)
        plt.ylabel('Mean Chi Slope', fontsize = axis_size-2)
        #plt.axis([0, 18, 0, 26])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend(('all data', 'granite'), loc='upper right', numpoints = 1)
    
        
        ax = plt.subplot(2,2,3)
        plt.plot(x_erate_log, np.log10(x_mchisl), "o", markersize=8, color='b')
        plt.plot(x_erate_log_g, np.log10(x_mchisl_g), "o", markersize=8, color='r')
        plt.plot(x_erate_log_a, np.log10(x_mchisl_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
        plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        #plt.axis([0, 18, 0, 26])
           
        ax = plt.subplot(2,2,4)
        plt.plot(x_erate_ff_log, np.log10(x_mchisl_ff), "o", markersize=8, color='b')
        plt.plot(x_erate_ff_log_g, np.log10(x_mchisl_ff_g), "o", markersize=8, color='r')
        plt.plot(x_erate_ff_log_a, np.log10(x_mchisl_ff_a), "+", markersize=8, color='w')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
        plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
        #plt.axis([0, 18, 0, 26])
        plt.title(selectitl, fontsize = label_size)
        #plt.legend(('all data', 'granite'), loc='upper right', numpoints = 1)
        plt.suptitle('MEAN CHANNEL STEEPNESS = f(EROSION RATE)',fontsize = label_size)
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_STEEPNESS-EROSION.png')

    # end of bonus if loop
    #---------------------           

    #   mean chi slope = f(erosion rate) WITH CLIMATE COLORS
    #=============================================================    
    plt.figure(13, facecolor='white',figsize=(20,15))      
    
    ax = plt.subplot(2,2,1)
    plt.scatter(np.log10(x_erate_arid), np.log10(x_mchisl_arid), marker='o', s=50, alpha=0.6, c='y')
    plt.scatter(np.log10(x_erate_tropical), np.log10(x_mchisl_tropical), marker='o', s=50, alpha=0.6, c='r')
    plt.scatter(np.log10(x_erate_temperate), np.log10(x_mchisl_temperate), marker='o', s=50, alpha=0.6, c='g')
    plt.scatter(np.log10(x_erate_cold), np.log10(x_mchisl_cold), marker='o', s=50, alpha=0.6, c='b')
    plt.scatter(np.log10(x_erate_polar), np.log10(x_mchisl_polar), marker='o', s=50, alpha=0.6, c='c')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    plt.title('All data', fontsize = label_size)
    plt.legend(('arid', 'tropical', 'temperate', 'cold', 'polar'), loc='lower right', numpoints = 1)
    
    ax = plt.subplot(2,2,2)
    plt.scatter(np.log10(x_erate_arid_ff), np.log10(x_mchisl_arid_ff), marker='o', s=50, alpha=0.6, c='y')
    plt.scatter(np.log10(x_erate_tropical_ff), np.log10(x_mchisl_tropical_ff), marker='o', s=50, alpha=0.6, c='r')
    plt.scatter(np.log10(x_erate_temperate_ff), np.log10(x_mchisl_temperate_ff), marker='o', s=50, alpha=0.6, c='g')
    plt.scatter(np.log10(x_erate_cold_ff), np.log10(x_mchisl_cold_ff), marker='o', s=50, alpha=0.6, c='b')
    plt.scatter(np.log10(x_erate_polar_ff), np.log10(x_mchisl_polar_ff), marker='o', s=50, alpha=0.6, c='c')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    plt.title(selectitl, fontsize = label_size)
    plt.suptitle('MEAN CHANNEL STEEPNESS = f(EROSION RATE) - CLIMATE',fontsize = label_size)

    # PLOT OPTIONS for the two lower figures:
    choice = 3
    
    # 2 = uncertainties
    # 3 = color by zones       
    
    if choice==2:
        ax = plt.subplot(2,2,3)
        ax.errorbar(x_erate,x_mchisl, xerr=data['erate_sigma'], yerr=data['Std_chi_slope'], fmt='o')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.axis([0, 3500, 0, 20])
        plt.xlabel('Erosion rate (mm/kyr)', fontsize = axis_size-2)
        plt.ylabel('Mean Chi Slope', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        
        
        ax = plt.subplot(2,2,4)
        ax.errorbar(x_erate_ff,x_mchisl_ff, xerr=dataff['erate_sigma'], yerr=dataff['Std_chi_slope'], fmt='o')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('Erosion rate (mm/kyr)', fontsize = axis_size-2)
        plt.ylabel('Mean Chi Slope', fontsize = axis_size-2)
        plt.axis([0, 3500, 0, 20])
        plt.title(selectitl, fontsize = label_size)
            
    elif choice==3:
        ax = plt.subplot(2,2,3)
        plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['zone'], alpha=0.8, cmap=plt.cm.prism)
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
        plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
        plt.title('All data', fontsize = label_size)
        
        
        ax = plt.subplot(2,2,4)
        plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['zone'], alpha=0.8, cmap=plt.cm.prism)
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
        plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
        plt.title(selectitl, fontsize = label_size)        
    
    else:        
        print "Choose display options for the two lower plots"
        
           
    if safi == 1:
        plt.savefig(SaveDirectory+'fig_'+str(datach)+'_STEEPNESS-EROSION_climate.png')

    #   mean chi slope = f(erosion rate) WITH THIRD VARIABLE COLORS - 1  LOG
    #=============================================================
    plt.figure(14, facecolor='white',figsize=(16,20))   
        
    # PRECIPITATION    
    ax = plt.subplot(3,2,1)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['MAP'],cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.colorbar()
    plt.title('All data', fontsize = label_size)
    
    ax = plt.subplot(3,2,2)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['MAP'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.title(str(selectitl), fontsize = label_size)
    cb = plt.colorbar()
    cb.set_label('MAP (mm/yr)', rotation=90)    

    
    # TEMPERATURE
    ax = plt.subplot(3,2,3)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['MAT'],cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.colorbar()
    #plt.title('MAT - All data', fontsize = label_size)
    
    ax = plt.subplot(3,2,4)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['MAT'],cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.axis([0, 3500, 0, 20])
    #plt.title('MAT - '+str(selectitl), fontsize = label_size)
    cb = plt.colorbar()
    cb.set_label('MAT (C)', rotation=90)    
    
    
    # ELEVATION
    ax = plt.subplot(3,2,5)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['elevation'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    #plt.axis([0, 3500, 0, 20])
    #plt.title('Elevation - All data', fontsize = label_size)
    plt.colorbar()
    
    ax = plt.subplot(3,2,6)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['elevation'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    #plt.axis([0, 3500, 0, 20])
    #plt.title('Elevation - '+str(selectitl), fontsize = label_size)
    cb = plt.colorbar()
    cb.set_label('Elevation (m)', rotation=90)    
    
    
    plt.suptitle('LOG MEAN CHANNEL STEEPNESS = f(LOG EROSION RATE) - Third param color - 1',fontsize = label_size)
    if safi == 1:
        plt.savefig(SaveDirectory+'fig_'+str(datach)+'_STEEPNESS-EROS_third-param-color-log1.png')
    

    #   mean chi slope = f(erosion rate) WITH THIRD VARIABLE COLORS - 2 LOG
    #=============================================================
    plt.figure(15, facecolor='white',figsize=(16,20))   
    
    # VEGETATION   
    ax = plt.subplot(3,2,1)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['vegetation'],cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.title('All data', fontsize = label_size)
    plt.colorbar()
    
    ax = plt.subplot(3,2,2)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['vegetation'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.title(str(selectitl), fontsize = label_size)
    cb = plt.colorbar()
    cb.set_label('Vegetation (%)', rotation=90)     
    
    # SEISMICITY
    ax = plt.subplot(3,2,3)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['seismicity'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.title('seismicity - All data', fontsize = label_size)
    plt.colorbar()
    
    ax = plt.subplot(3,2,4)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['seismicity'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.title('seismicity - '+str(selectitl), fontsize = label_size)
    cb = plt.colorbar()
    cb.set_label('Seismicity-PGA', rotation=90) 
    
    
    # LATITUDE
    ax = plt.subplot(3,2,5)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['Latitude'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.title('Latitude - All data', fontsize = label_size)
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    plt.colorbar()
    
    ax = plt.subplot(3,2,6)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['Latitude'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.title('Latitude - '+str(selectitl), fontsize = label_size)
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    cb = plt.colorbar()    
    cb.set_label('Latitude (degree)', rotation=90) 
    
    plt.suptitle('LOG MEAN CHANNEL STEEPNESS = f(LOG EROSION RATE) - Third param color - 2',fontsize = label_size)
    if safi == 1:
        plt.savefig(SaveDirectory+'fig_'+str(datach)+'_STEEPNESS-EROS_third-param-color-log2.png')
    
    
    #   mean chi slope = f(erosion rate) WITH THIRD VARIABLE COLORS - 3 LOG
    #=============================================================
    plt.figure(16, facecolor='white',figsize=(16,20))   
    
    # M/N
    ax = plt.subplot(3,2,1)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['m_over_n'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.axis([0, 3500, 0, 20])
    plt.title('All data', fontsize = label_size)
    plt.colorbar()
    
    ax = plt.subplot(3,2,2)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['m_over_n'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.axis([0, 3500, 0, 20])
    plt.title(str(selectitl), fontsize = label_size)
    cb = plt.colorbar()
    cb.set_label('M/N', rotation=90)     
    
    # N
    ax = plt.subplot(3,2,3)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['n'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.axis([0, 3500, 0, 20])
    #plt.title('N - All data', fontsize = label_size)
    plt.colorbar()
    
    ax = plt.subplot(3,2,4)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['n'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.axis([0, 3500, 0, 20])
    #plt.title('N - '+str(selectitl), fontsize = label_size)
    cb = plt.colorbar()
    cb.set_label('N', rotation=90) 
    
    # K
    ax = plt.subplot(3,2,5)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['K'], cmap=my_cmap, alpha=0.5)    
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    #plt.axis([0, 3500, 0, 20])
    #plt.title('K - All data', fontsize = label_size)
    plt.colorbar()
    
    ax = plt.subplot(3,2,6)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=np.log10(dataff['K']), cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    #plt.axis([0, 3500, 0, 20])
    #plt.title('K - '+str(selectitl), fontsize = label_size)
    plt.clim(-16.6,-1)
    cb = plt.colorbar()
    cb.set_label('LOG K - Fixed range ('+str('%.1f' % np.min(np.log10(dataff['K'])))+' - '+str('%.1f' % np.max(np.log10(dataff['K'])))+')', rotation=90)
    #cb.set_label('K', rotation=90)
    if safi == 1:
        plt.savefig(SaveDirectory+'fig_'+str(datach)+'_STEEPNESS-EROS_third-param-color-log3.png')
    
    
    #   mean chi slope = f(erosion rate) WITH THIRD VARIABLE COLORS - 4 LOG
    #=============================================================
    plt.figure(17, facecolor='white',figsize=(16,20))   
    
    
   # AREA
    ax = plt.subplot(3,2,1)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['area']/1000000, cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.title('All data', fontsize = label_size)
    plt.colorbar()

    
    ax = plt.subplot(3,2,2)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['area']/1000000, cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.title(str(selectitl), fontsize = label_size)
    plt.clim(0,100)
    cb = plt.colorbar()
    cb.set_label('Area - Fixed range ('+str(np.min(dataff['area']/1000000))+' - '+str(np.max(dataff['area']/1000000))+' km2)', rotation=90)    
        

   # ELEVATION
    ax = plt.subplot(3,2,3)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['elevation'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.axis([0, 3500, 0, 20])
    #plt.title('Elevation - All data', fontsize = label_size)
    plt.colorbar()
    
    ax = plt.subplot(3,2,4)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['elevation'], cmap=my_cmap, alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.axis([0, 3500, 0, 20])
    #plt.title('Elevation - '+str(selectitl), fontsize = label_size)
    cb = plt.colorbar()
    cb.set_label('Elevation (m)', rotation=90) 
    
    # ROCK-TYPE
    ax = plt.subplot(3,2,5)
    plt.scatter(x_erate_log, np.log10(x_mchisl), marker='o', s=50, c=data['rock'], alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    plt.colorbar()
    #plt.title('Rock-Type - All data', fontsize = label_size)
    
    ax = plt.subplot(3,2,6)
    plt.scatter(x_erate_ff_log, np.log10(x_mchisl_ff), marker='o', s=50, c=dataff['rock'], alpha=0.5)
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size-2)
    plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size-2)
    #plt.axis([0, 3500, 0, 20])
    #plt.title('Rock-Type - '+str(selectitl), fontsize = label_size)
    cb = plt.colorbar()
    cb.set_label('Rock Type', rotation=90) 
    

    plt.suptitle('LOG MEAN CHANNEL STEEPNESS = f(LOG EROSION RATE) - Third param color - 4',fontsize = label_size)
    if safi == 1:
        plt.savefig(SaveDirectory+'fig_'+str(datach)+'_STEEPNESS-EROS_third-param-color-log4.png')
        
        
    
    # CLIMATE PLOTS
    #====================
    
    # K = f(climate) 
    #--------------------------    
    
    plt.figure(18, facecolor='white',figsize=(16,20))    
    
    ax = plt.subplot(3,2,1)
    plt.plot(x_clim, np.log10(y_K), "o", markersize=8, color='b')
    plt.plot(x_clim_g, np.log10(y_K_g), "o", markersize=8, color='r')   
    plt.plot(x_clim_a, np.log10(y_K_a), "+", markersize=8, color='w')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.ylabel('LOG K', fontsize = axis_size-2)
    plt.title('All K', fontsize = label_size)
    plt.axis([0, 6, 0, np.max(np.log10(y_K))-0.1])
    #plt.legend( ('all data', 'granite'), loc='upper left', numpoints = 1)
    plt.suptitle('1=Arid / 2=Tropical / 3=Temperate / 4=Cold / 5=Polar',fontsize = label_size)
    
    ax = plt.subplot(3,2,2)
    plt.plot(x_clim_ff, np.log10(y_K_ff), "o", markersize=8, color='b')
    plt.plot(x_clim_ff_g, np.log10(y_K_ff_g), "o", markersize=8, color='r')
    plt.plot(x_clim_ff_a, np.log10(y_K_ff_a), "+", markersize=8, color='w')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.ylabel('LOG K', fontsize = axis_size-2)
    plt.axis([0, 6, 0, np.max(np.log10(y_K))-0.1])
    plt.title(selectitl, fontsize = label_size)
    
    
    # m/n = f(climate) 
    #--------------------------    
       
    ax = plt.subplot(3,2,3)
    plt.plot(x_clim, y_mn, "o", markersize=8, color='b')
    plt.plot(x_clim_g, y_mn_g, "o", markersize=8, color='r')
    plt.plot(x_clim_a, y_mn_a, "+", markersize=8, color='w')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.xlabel('Rock type', fontsize = axis_size-2)
    plt.ylabel('m/n', fontsize = axis_size-2)
    plt.title('All data', fontsize = label_size)
    plt.axis([0, 6, 0, maxmn])
    
    ax = plt.subplot(3,2,4)
    plt.plot(x_clim_ff, y_mn_ff, "o", markersize=8, color='b')
    plt.plot(x_clim_ff_g, y_mn_ff_g, "o", markersize=8, color='r')
    plt.plot(x_clim_ff_a, y_mn_ff_a, "+", markersize=8, color='w')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    #plt.xlabel('Rock type', fontsize = axis_size-2)
    plt.ylabel('m/n', fontsize = axis_size-2)
    plt.axis([0, 6, 0, maxmn])
    plt.title(selectitl, fontsize = label_size)
    
    
    # n = f(Rock_type) 
    #-------------------------- 
    ax = plt.subplot(3,2,5)
    plt.plot(x_clim, y_n, "o", markersize=8, color='b')
    plt.plot(x_clim_g, y_n_g, "o", markersize=8, color='r')
    plt.plot(x_clim_a, y_n_a, "+", markersize=8, color='w')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('Climate type', fontsize = axis_size-2)
    plt.ylabel('n', fontsize = axis_size-2)
    plt.title('All data', fontsize = label_size)
    plt.axis([0, 6, -60, 84])

    
    ax = plt.subplot(3,2,6)
    plt.plot(x_clim_ff, y_n_ff, "o", markersize=8, color='b')
    plt.plot(x_clim_ff_g, y_n_ff_g, "o", markersize=8, color='r')
    plt.plot(x_clim_ff_a, y_n_ff_a, "+", markersize=8, color='w')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('Climate type', fontsize = axis_size-2)
    plt.ylabel('n', fontsize = axis_size-2)
    plt.axis([0, 6, 0, maxn])
    plt.title(selectitl, fontsize = label_size)
    if safi == 1:
        plt.savefig(SaveDirectory+'fig_'+str(datach)+'_CLIMATE.png') 
    

    #  PDF with CLIMATE
    #=============================================================
    if 0==1:    
        plt.figure(43, facecolor='white',figsize=(16,20))       
    
        # m/n
        xs = np.linspace(np.min(y_mn), np.max(y_mn), 100)
        ax = plt.subplot(3,2,1)
        density = gaussian_kde(y_mn)        
        density_arid = gaussian_kde(y_mn_arid)
        density_tropical = gaussian_kde(y_mn_tropical)
        density_temperate = gaussian_kde(y_mn_temperate)
        density_cold = gaussian_kde(y_mn_cold)
        density_polar = gaussian_kde(y_mn_polar)
        #density.covariance_factor = lambda : .25
        #density._compute_covariance()
        plt.plot(xs,density(xs), color='k',linewidth=2.0)
        plt.plot(xs,density_arid(xs), color='y')
        plt.plot(xs,density_tropical(xs), color='r')
        plt.plot(xs,density_temperate(xs), color='g')
        plt.plot(xs,density_cold(xs), color='b')
        plt.plot(xs,density_polar(xs), color='c')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('m / n', fontsize = axis_size-2)
        plt.ylabel('PDF', fontsize = axis_size-2)    
        
        ax = plt.subplot(3,2,2)
        xs = np.linspace(np.min(y_mn_ff), np.max(y_mn_ff), 100)
        density = gaussian_kde(y_mn_ff)        
        density_arid = gaussian_kde(y_mn_arid_ff)
        density_tropical = gaussian_kde(y_mn_tropical_ff)
        density_temperate = gaussian_kde(y_mn_temperate_ff)
        density_cold = gaussian_kde(y_mn_cold_ff)
        density_polar = gaussian_kde(y_mn_polar_ff)
        #density.covariance_factor = lambda : .25
        #density._compute_covariance()
        plt.plot(xs,density(xs), color='k',linewidth=2.0)
        plt.plot(xs,density_arid(xs), color='y')
        plt.plot(xs,density_tropical(xs), color='r')
        plt.plot(xs,density_temperate(xs), color='g')
        plt.plot(xs,density_cold(xs), color='b')
        plt.plot(xs,density_polar(xs), color='c')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('m / n - '+str(selectitl), fontsize = axis_size-2)
        #plt.ylabel('PDF', fontsize = axis_size-2)
        plt.suptitle('Probability Density Function of m/n, n and K', fontsize = label_size)
        
        # n
        xs = np.linspace(np.min(y_n), np.max(y_n), 100)
        ax = plt.subplot(3,2,3)
        density = gaussian_kde(y_n)        
        density_arid = gaussian_kde(y_n_arid)
        density_tropical = gaussian_kde(y_n_tropical)
        density_temperate = gaussian_kde(y_n_temperate)
        density_cold = gaussian_kde(y_n_cold)
        density_polar = gaussian_kde(y_n_polar)
        plt.plot(xs,density(xs), color='k',linewidth=2.0)
        plt.plot(xs,density_arid(xs), color='y')
        plt.plot(xs,density_tropical(xs), color='r')
        plt.plot(xs,density_temperate(xs), color='g')
        plt.plot(xs,density_cold(xs), color='b')
        plt.plot(xs,density_polar(xs), color='c')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('n', fontsize = axis_size-2)
        plt.ylabel('PDF', fontsize = axis_size-2)    
        #plt.axis([-50, 50, 0, 0.18])
    
        
        ax = plt.subplot(3,2,4)
        xs = np.linspace(np.min(y_n_ff), np.max(y_n_ff), 100)
        density = gaussian_kde(y_n_ff)        
        density_arid = gaussian_kde(y_n_arid_ff)
        density_tropical = gaussian_kde(y_n_tropical_ff)
        density_temperate = gaussian_kde(y_n_temperate_ff)
        density_cold = gaussian_kde(y_n_cold_ff)
        density_polar = gaussian_kde(y_n_polar_ff)
        plt.plot(xs,density(xs), color='k',linewidth=2.0)
        plt.plot(xs,density_arid(xs), color='y')
        plt.plot(xs,density_tropical(xs), color='r')
        plt.plot(xs,density_temperate(xs), color='g')
        plt.plot(xs,density_cold(xs), color='b')
        plt.plot(xs,density_polar(xs), color='c')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('n - '+str(selectitl), fontsize = axis_size-2)
        
        # K
        xs = np.linspace(np.min(y_K), np.max(y_K), 100)
        ax = plt.subplot(3,2,5)
        density = gaussian_kde(y_K)        
        density_arid = gaussian_kde(y_K_arid)
        density_tropical = gaussian_kde(y_K_tropical)
        density_temperate = gaussian_kde(y_K_temperate)
        density_cold = gaussian_kde(y_K_cold)
        density_polar = gaussian_kde(y_K_polar)
        plt.plot(xs,density(xs), color='k',linewidth=2.0)
        plt.plot(xs,density_arid(xs), color='y')
        plt.plot(xs,density_tropical(xs), color='r')
        plt.plot(xs,density_temperate(xs), color='g')
        plt.plot(xs,density_cold(xs), color='b')
        plt.plot(xs,density_polar(xs), color='c')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('K', fontsize = axis_size-2)
        plt.ylabel('PDF', fontsize = axis_size-2)    
        plt.legend(('all', 'arid', 'tropical', 'temperate', 'cold', 'polar'), loc='upper right', numpoints = 1)
        #plt.axis([0, 0.1, 0, 4])
    
        
        ax = plt.subplot(3,2,6)
        xs = np.linspace(np.min(y_K_ff), np.max(y_K_ff), 100)
        density = gaussian_kde(y_K_ff)        
        density_arid = gaussian_kde(y_K_arid_ff)
        density_tropical = gaussian_kde(y_K_tropical_ff)
        density_temperate = gaussian_kde(y_K_temperate_ff)
        density_cold = gaussian_kde(y_K_cold_ff)
        density_polar = gaussian_kde(y_K_polar_ff)
        plt.plot(xs,density(xs), color='k',linewidth=2.0)
        plt.plot(xs,density_arid(xs), color='y')
        plt.plot(xs,density_tropical(xs), color='r')
        plt.plot(xs,density_temperate(xs), color='g')
        plt.plot(xs,density_cold(xs), color='b')
        plt.plot(xs,density_polar(xs), color='c')
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('K - '+str(selectitl), fontsize = axis_size-2)
        plt.axis([0, 0.6, 0, 40])
    
        
        if safi == 1:
            plt.savefig(SaveDirectory+'fig_'+str(datach)+'_PDF_mnK_climate.png')
     
 
 
    #  LINEAR REGRESSIONS FOR CLIMATE, ROCK TYPE
    #=============================================================
    plt.figure(19, facecolor='white',figsize=(20,15))      
    ax = plt.subplot(1,2,1)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(x_erate),np.log10(x_mchisl))
    line = slope*np.log10(x_erate)+intercept
    plt.plot(np.log10(x_erate),line,'grey',lw=4)
    
    for cli in [1,2,3,4,5]:
        if cli == 1:
            x = np.log10(x_erate_arid)
            y = np.log10(x_mchisl_arid)
            colo = 'y'
        elif cli == 2:
            x = np.log10(x_erate_tropical)
            y = np.log10(x_mchisl_tropical)
            colo = 'r'
        elif cli == 3:
            x = np.log10(x_erate_temperate)
            y = np.log10(x_mchisl_temperate)
            colo = 'g'
        elif cli == 4:
            x = np.log10(x_erate_cold)
            y = np.log10(x_mchisl_cold)
            colo = 'b'            
        elif cli == 5:
            x = np.log10(x_erate_polar)
            y = np.log10(x_mchisl_polar)
            colo = 'c'

        plt.scatter(x,y, marker='o', s=50, alpha=0.6, c=colo)
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size)
        plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size)
        plt.title('All data', fontsize = label_size)
    
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*x+intercept
        plt.plot(x,line,colo,lw=3)
        plt.legend(('Global','arid', 'tropical', 'temperate', 'cold', 'polar'), loc='lower right', numpoints = 1)

    
    ax = plt.subplot(1,2,2)
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(x_erate_ff),np.log10(x_mchisl_ff))
    line = slope*np.log10(x_erate_ff)+intercept
    plt.plot(np.log10(x_erate_ff),line,'lightgrey',lw=4)    
    
    for cli in [1,2,3,4,5]:
        if cli == 1:
            x = np.log10(x_erate_arid_ff)
            y = np.log10(x_mchisl_arid_ff)
            colo = 'y'
        elif cli == 2:
            x = np.log10(x_erate_tropical_ff)
            y = np.log10(x_mchisl_tropical_ff)
            colo = 'r'
        elif cli == 3:
            x = np.log10(x_erate_temperate_ff)
            y = np.log10(x_mchisl_temperate_ff)
            colo = 'g'
        elif cli == 4:
            x = np.log10(x_erate_cold_ff)
            y = np.log10(x_mchisl_cold_ff)
            colo = 'b'            
        elif cli == 5:
            x = np.log10(x_erate_polar_ff)
            y = np.log10(x_mchisl_polar_ff)
            colo = 'c'         
    
        plt.scatter(x,y, marker='o', s=50, alpha=0.6, c=colo)
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Erosion rate (mm/kyr)', fontsize = axis_size)
        plt.ylabel('LOG Mean Chi Slope', fontsize = axis_size)
        plt.title(selectitl, fontsize = label_size)
    
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*x+intercept
        plt.plot(x,line,colo,lw=3)

    if safi == 1:
        plt.savefig(SaveDirectory+'fig_'+str(datach)+'_LineRegress_climate.png')
 
 
 
    #   Steepness = f(m/n) with climate colors
    #=============================================================
    plt.figure(20, facecolor='white',figsize=(16,10))   
    
    ax = plt.subplot(1,2,1)
    for cli in [1,2,3,4,5]:
        if cli == 1:
            y = y_mn_arid
            x = np.log10(x_mchisl_arid)
            colo = 'y'
        elif cli == 2:
            y = y_mn_tropical
            x = np.log10(x_mchisl_tropical)
            colo = 'r'
        elif cli == 3:
            y = y_mn_temperate
            x = np.log10(x_mchisl_temperate)
            colo = 'g'
        elif cli == 4:
            y = y_mn_cold
            x = np.log10(x_mchisl_cold)
            colo = 'b'            
        elif cli == 5:
            y = y_mn_polar
            x = np.log10(x_mchisl_polar)
            colo = 'c'

        plt.scatter(x,y, marker='o', s=50, alpha=0.6, c=colo)
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Steepness index', fontsize = axis_size)
        plt.ylabel('M/N', fontsize = axis_size)
        plt.title('All data', fontsize = label_size)
        plt.legend(('arid', 'tropical', 'temperate', 'cold', 'polar'), loc='lower right', numpoints = 1)

    ax = plt.subplot(1,2,2)
    for cli in [1,2,3,4,5]:
        if cli == 1:
            y = y_mn_arid_ff
            x = np.log10(x_mchisl_arid_ff)
            colo = 'y'
        elif cli == 2:
            y = y_mn_tropical_ff
            x = np.log10(x_mchisl_tropical_ff)
            colo = 'r'
        elif cli == 3:
            y = y_mn_temperate_ff
            x = np.log10(x_mchisl_temperate_ff)
            colo = 'g'
        elif cli == 4:
            y = y_mn_cold_ff
            x = np.log10(x_mchisl_cold_ff)
            colo = 'b'            
        elif cli == 5:
            y = y_mn_polar_ff
            x = np.log10(x_mchisl_polar_ff)
            colo = 'c'

        plt.scatter(x,y, marker='o', s=50, alpha=0.6, c=colo)
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('LOG Steepness index', fontsize = axis_size)
        plt.ylabel('M/N', fontsize = axis_size)
        plt.title('p<=0.1 data', fontsize = label_size)
        
    if safi == 1:
        plt.savefig(SaveDirectory+'fig_'+str(datach)+'_Steepness_movern.png')
        
        
    #   K, n, m/n = f(parameter) with climate colors (Fixed m/n only)
    #=================================================================
    plt.figure(21, facecolor='white',figsize=(16,20))   
    
    # MAP 
    ax = plt.subplot(2,2,1)
    for cli in [1,2,3,4,5]:
        if cli == 1:
            y = np.log10(y_K_arid_ff)
            x = x_precip_arid_ff
            colo = 'y'
        elif cli == 2:
            y = np.log10(y_K_tropical_ff)
            x = x_precip_tropical_ff
            colo = 'r'
        elif cli == 3:
            y = np.log10(y_K_temperate_ff)
            x = x_precip_temperate_ff
            colo = 'g'
        elif cli == 4:
            y = np.log10(y_K_cold_ff)
            x = x_precip_cold_ff
            colo = 'b'            
        elif cli == 5:
            y = np.log10(y_K_polar_ff)
            x = x_precip_polar_ff
            colo = 'c'

        plt.scatter(x,y, marker='o', s=50, alpha=0.6, c=colo)
        # linear regression for each climate        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*x+intercept
        plt.plot(x,line,colo,lw=3)            
        
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('MAP', fontsize = axis_size)
        plt.ylabel('log10 K', fontsize = axis_size)

    ax = plt.subplot(2,2,2)
    for cli in [1,2,3,4,5]:
        if cli == 1:
            y = y_n_arid_ff
            x = x_precip_arid_ff
            colo = 'y'
        elif cli == 2:
            y = y_n_tropical_ff
            x = x_precip_tropical_ff
            colo = 'r'
        elif cli == 3:
            y = y_n_temperate_ff
            x = x_precip_temperate_ff
            colo = 'g'
        elif cli == 4:
            y = y_n_cold_ff
            x = x_precip_cold_ff
            colo = 'b'            
        elif cli == 5:
            y = y_n_polar_ff
            x = x_precip_polar_ff
            colo = 'c'

        plt.scatter(x,y, marker='o', s=50, alpha=0.6, c=colo)
        # linear regression for each climate        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*x+intercept
        plt.plot(x,line,colo,lw=3)           
        
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('MAP', fontsize = axis_size)
        plt.ylabel('n', fontsize = axis_size)
        plt.legend(('Arid', 'Tropical', 'Temperate', 'Cold', 'Polar'), loc='lower right', numpoints = 1)


    # MAT 
    ax = plt.subplot(2,2,3)
    for cli in [1,2,3,4,5]:
        if cli == 1:
            y = np.log10(y_K_arid_ff)
            x = x_temp_arid_ff
            colo = 'y'
        elif cli == 2:
            y = np.log10(y_K_tropical_ff)
            x = x_temp_tropical_ff
            colo = 'r'
        elif cli == 3:
            y = np.log10(y_K_temperate_ff)
            x = x_temp_temperate_ff
            colo = 'g'
        elif cli == 4:
            y = np.log10(y_K_cold_ff)
            x = x_temp_cold_ff
            colo = 'b'            
        elif cli == 5:
            y = np.log10(y_K_polar_ff)
            x = x_temp_polar_ff
            colo = 'c'

        plt.scatter(x,y, marker='o', s=50, alpha=0.6, c=colo)
        # linear regression for each climate        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*x+intercept
        plt.plot(x,line,colo,lw=3)            
        
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('MAT', fontsize = axis_size)
        plt.ylabel('log10 K', fontsize = axis_size)

    ax = plt.subplot(2,2,4)
    for cli in [1,2,3,4,5]:
        if cli == 1:
            y = y_n_arid_ff
            x = x_temp_arid_ff
            colo = 'y'
        elif cli == 2:
            y = y_n_tropical_ff
            x = x_temp_tropical_ff
            colo = 'r'
        elif cli == 3:
            y = y_n_temperate_ff
            x = x_temp_temperate_ff
            colo = 'g'
        elif cli == 4:
            y = y_n_cold_ff
            x = x_temp_cold_ff
            colo = 'b'            
        elif cli == 5:
            y = y_n_polar_ff
            x = x_temp_polar_ff
            colo = 'c'

        plt.scatter(x,y, marker='o', s=50, alpha=0.6, c=colo)
        # linear regression for each climate        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
        line = slope*x+intercept
        plt.plot(x,line,colo,lw=3)           
        
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5)    
        plt.xlabel('MAT', fontsize = axis_size)
        plt.ylabel('n', fontsize = axis_size)

        plt.suptitle('Fixed m/n', fontsize = label_size)

    if safi == 1:
        plt.savefig(SaveDirectory+'fig_'+str(datach)+'_nK_precip_climate.png')        
        
        
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
       
       
    plt.show()
      

if __name__ == "__main__":
    make_plots()