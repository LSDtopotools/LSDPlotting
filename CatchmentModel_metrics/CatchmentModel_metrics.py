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
    plt.xlim(0, 300)
    # plt.ylim(0,1400)
    plt.xlabel("Elevation (m)")
    plt.ylabel("Elevation difference (mm)")
    plt.show()


def convert_timestep(time_step):
    minutes = time_step*5
    hours = minutes/60
    return hours


class CatchmentPlot(object):

    def __init__(self, data_dir, fname):
        self.data_dir = data_dir
        self.fname = fname

    """
    Extracts the relevant data column from the timeseries file.
    """
    def get_datametric_array(self, filename, data_name):
        time_step, q_lisflood, \
            q_topmodel, sed_tot = np.loadtxt(filename,
                                             usecols=(0, 1, 2, 4), unpack=True)

        # Create a dictionary to store the keys/arrays
        # You can add to this later without having to modify
        # the plot_hydrography function
        dic = {'q_lisflood': q_lisflood,
               'q_topmodel': q_topmodel,
               'sed_tot': sed_tot
               }
        return time_step, dic[data_name]

    def plot_hydrograph(self, metric_name, current_timeseries=None, axes=None,
                        draw_inset=False, ax_inset=None):
        if current_timeseries is None:
            current_timeseries = self.fname
        filename = self.data_dir + current_timeseries
        # get the time step array and the data metric
        # you want to plot against it.
        time_step, metric = self.get_datametric_array(filename, metric_name)
        hours = convert_timestep(time_step)
        # We check this so the function can be called
        # within the plot_ensemble_hydrograph
        # function, without having to duplicate axes creation every iteration.
        if axes is None:
            fig, axes = plt.subplots()

        # If we want to draw the inset,
        # and we haven't already got an inset axes
        # i.e. if you were using the multiple plot/ensemble plot,
        # this would already have been created.
        if (draw_inset is True and ax_inset is None):
            ax_inset = self.create_inset_axes(axes)

        # plot the main axes data
        line, = axes.plot(hours, metric)
        line.set_label(fname)
        axes.legend(bbox_to_anchor=(1, 0.5),
                    loc='center left', prop={'size': 12})

        # Tweak the xlimits to zone in on the relevnat bit of hydrograph
        axes.set_xlim(35, 54)

        # Now plot the inset data
        if ax_inset is not None:
            self.plot_inset(axes, hours, metric, ax_inset)

    def plot_ensemble_hydrograph(self,
                                 metric_name, draw_inset=False):
        fig, ax = plt.subplots()

        if draw_inset is True:
            ax_inset = self.create_inset_axes(ax)
        else:
            ax_inset = None

        # Loop through the files in a dir and plot them all on the same axes
        for f in glob.glob(self.data_dir + self.fname):
            current_timeseries = os.path.basename(f)
            print current_timeseries
            self.plot_hydrograph(metric_name, current_timeseries,
                                 ax, draw_inset, ax_inset)

        # draw a bbox of the region of the inset axes in the parent axes and
        # connecting lines between the bbox and the inset axes area
        # mark_inset(ax, ax_inset, loc1=2, loc2=3, fc="none", ec="0.5")
        self.set_labels(ax, metric_name)
        self.save_figure(fig)

    def set_labels(self, ax, metric_name):

        label_dic = {
          'q_lisflood': "water discharge ($m^3s^{-1}$)",
          'q_topmodel': "water (TOPMODEL) discharge ($m^3s^{-1}$)",
          'sed_tot': "sediment flux ($m^3$)"
        }

        ax.set_xlabel("simulation time (hours)")
        ax.set_ylabel(label_dic[metric_name])

    def save_figure(self, fig):
        fig.savefig("test.svg", bbox_inches='tight')

    def create_inset_axes(self, ax):
        ax_inset = zoomed_inset_axes(ax, 2, loc=1)
        # hide every other tick label
        for label in ax_inset.get_xticklabels()[::2]:
            label.set_visible(False)

        return ax_inset

    def plot_inset(self, parent_axes, x_data, y_data, ax_inset):
        ax_inset.plot(x_data, y_data)
        ax_inset.set_xlim(39, 42)
        ax_inset.set_ylim(90, 160)



# VARIABLES
data_dir = "/mnt/SCRATCH/Analyses/HydrogeomorphPaper/BOSCASTLE/Analysis/"
# data_dir = "/run/media/dav/SHETLAND/Analyses/HydrogeomorphPaper/BOSCASTLE/Analysis/"
# data_dir="/mnt/WORK/Dev/PyToolsPhD/Radardata_tools"
input_raster2 = "elev.txt"
input_raster1 = "elevdiff.txt"
# input_raster2 = "rainfall_totals_boscastle_downscaled.asc"

# A text file with x, y scatter values, in case of future use
outpt_datafile_name = "elev_vs_erosion.txt"

fname = "boscastle_lumped_detachlim.dat"
wildcard_fname = "ryedale*.dat"


# Run the script
# elev, total_precip = create_data_arrays(data_dir, input_raster2, input_raster1)
# plot_scatter_rasterdata(elev, total_precip)

#plot_hydrograph(data_dir, fname, "q_lisflood", draw_inset=True)

# OOP way
BoscastleHydro = CatchmentPlot(data_dir, "boscastle_*")
BoscastleHydro.plot_ensemble_hydrograph("q_lisflood", draw_inset=True)


























