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
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset


# VARIABLES
#data_dir = "/mnt/SCRATCH/Analyses/HydrogeomorphPaper/BOSCASTLE/Analysis/"
data_dir = "/run/media/dav/SHETLAND/Analyses/HydrogeomorphPaper/BOSCASTLE/Analysis/"
#data_dir="/mnt/WORK/Dev/PyToolsPhD/Radardata_tools"
input_raster2 = "elev.txt"
input_raster1 = "elevdiff.txt"
#input_raster2 = "rainfall_totals_boscastle_downscaled.asc"

# A text file with x, y scatter values, in case of future use
outpt_datafile_name = "elev_vs_erosion.txt"

timeseries = "boscastle_lumped_detachlim.dat"
wildcard_fname = "boscastle*.dat"

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
    
def plot_hydrograph(data_dir,timeseries, axes=None, ax_inset=None):   

    filename = data_dir + timeseries
    time_step, q_lisflood, q_topmodel, sed_tot = np.loadtxt(filename, usecols=(0,1,2,4), unpack=True)
    
    if axes==None:
        fig, ax = plt.subplots()
        
    axes.plot(time_step, q_lisflood)
    axes.set_xlim(450,600)

    if ax_inset==True:
      plot_inset(axes, time_step, q_lisflood, ax_inset)
    

    
def plot_ensemble_hydrograph(data_dir, wildcard_fname, inset=False):
    fig, ax = plt.subplots()
    
    if inset==True:
      ax_inset = zoomed_inset_axes(ax, 2, loc=1)
          # hide every other tick label
      for label in ax_inset.get_xticklabels()[::2]:
        label.set_visible(False)
    else:
      ax_inset=None

    # Loop through the files in a dir and plot them all on the same axes
    for f in glob.glob(data_dir + wildcard_fname):
        current_timeseries = os.path.basename(f)
        print current_timeseries
        plot_hydrograph(data_dir, current_timeseries, ax, ax_inset)
    
    # draw a bbox of the region of the inset axes in the parent axes and
    # connecting lines between the bbox and the inset axes area
    #mark_inset(ax, ax_inset, loc1=2, loc2=3, fc="none", ec="0.5")
            
def plot_inset(parent_axes, x_data, y_data, ax_inset):
    ax_inset.plot(x_data, y_data)
    ax_inset.set_xlim(470,500)
    ax_inset.set_ylim(100,160)

    
    
# Run the script 
#elev, total_precip = create_data_arrays(data_dir, input_raster2, input_raster1)
#plot_scatter_rasterdata(elev, total_precip)

#plot_hydrograph(data_dir,timeseries)

plot_ensemble_hydrograph(data_dir, wildcard_fname, inset=True)


























