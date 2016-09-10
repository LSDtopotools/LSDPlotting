# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 12:08:22 2016

Erosion scatter plots

This script plots erosion amount against other metrics,
such as elevation and precipitation.

Actually, it can be used as a generic DEM vs DEM plotter: 
You just need to supply 2 input dems/raster data files of
the same dimension and resolution. It will plot each pixel 
as an x y scatter plot. Function for doing binned/window 
averages also under construction.

@author: dav
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# VARIABLES
data_dir = "/mnt/SCRATCH/Analyses/HydrogeomorphPaper/BOSCASTLE/Analysis/"
#data_dir="/mnt/WORK/Dev/PyToolsPhD/Radardata_tools"
input_raster2 = "elev.txt"
input_raster1 = "elevdiff.txt"
#input_raster2 = "rainfall_totals_boscastle_downscaled.asc"

# A text file with x, y scatter values, in case of future use
outpt_datafile_name = "elev_vs_erosion.txt"

timeseries = "boscastle_lumped_detachlim.dat"

# Plotting parameters
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['arial']
rcParams['font.size'] = 16


def create_data_arrays(data_dir, input_raster1, input_raster2):
    load_data1 = data_dir + "/" + input_raster1
    load_data2 = data_dir + "/" + input_raster2
    data_raster1 = np.loadtxt(load_data1, skiprows=6)
    data_raster2 = np.loadtxt(load_data2, skiprows=6)
    
    # get a 1D array from the raster data.
    return data_raster1.flatten(), data_raster2.flatten()
    
def plot_scatter_rasterdata(data_array1, data_array2):
    plt.scatter(data_array1, data_array2, marker="x")
    plt.xlim(0,300)
    #plt.ylim(0,1400)
    plt.xlabel("Elevation (m)")
    plt.ylabel("Elevation difference (mm)")
    plt.show()
    
def plot_hydrograph(data_dir,timeseries):
    filename = data_dir + timeseries
    time_step, q_topmodel, q_lisflood = np.loadtxt(filename, usecols=(0,1,2), unpack=True)
    
    plt.plot(time_step, q_lisflood)
    
    
# Run the script 
#elev, total_precip = create_data_arrays(data_dir, input_raster2, input_raster1)
#plot_scatter_rasterdata(elev, total_precip)

plot_hydrograph(data_dir,timeseries)




























