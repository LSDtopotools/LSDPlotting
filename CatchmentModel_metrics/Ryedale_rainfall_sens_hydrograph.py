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
import re  # regex
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

# This is a custom module
from label_lines import *


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


class CaesarTimeseriesPlot(object):

    def __init__(self, data_dir, fname, datametric):
        self.data_dir = data_dir
        self.fname = fname
        self.fig, self.ax = plt.subplots()

        self.ax_inset = None
        self.metric_name = datametric
        self.num_graphs = len(glob.glob(self.data_dir + self.fname))

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

    def plot_hydrograph(self, current_timeseries=None,
                        draw_inset=False, ax_inset=None):
        if current_timeseries is None:
            current_timeseries = self.fname

        line_label = self.make_line_label(current_timeseries)

        filename = self.data_dir + current_timeseries
        # get the time step array and the data metric
        # you want to plot against it.
        time_step, metric = self.get_datametric_array(filename, self.metric_name)
        hours = convert_timestep(time_step)

        # If we want to draw the inset,
        # and we haven't already got an inset axes
        # i.e. if you were using the multiple plot/ensemble plot,
        # this would already have been created.
        if (draw_inset is True and self.ax_inset is None):
            self.ax_inset = self.create_inset_axes()

        # plot the main axes data
        line, = self.ax.plot(hours, metric, linewidth=2)
        line.set_label(line_label)
        #labelLine(line, 45)

        # Tweak the xlimits to zone in on the relevnat bit of hydrograph
        self.ax.set_xlim(40, 50)

        # Now plot the inset data
        if self.ax_inset is not None:
            self.plot_inset(hours, metric)



    def plot_ensemble_hydrograph(self, draw_inset=False, labellines=False):

        cm = plt.get_cmap('winter')
        self.ax.set_color_cycle([cm(1.*i/self.num_graphs)
                                for i in range(self.num_graphs)])

        if draw_inset is True:
            self.ax_inset = self.create_inset_axes()
        else:
            self.ax_inset = None

        # Loop through the files in a dir and plot them all on the same axes
        for f in sorted(glob.glob(self.data_dir + self.fname)):
            current_timeseries = os.path.basename(f)
            print current_timeseries
            self.plot_hydrograph(current_timeseries, draw_inset)

        # for i in caesar_cube.dim(3) # loop through 3rd dims of array

        # draw a bbox of the region of the inset axes in the parent axes and
        # connecting lines between the bbox and the inset axes area
        # mark_inset(ax, ax_inset, loc1=2, loc2=3, fc="none", ec="0.5")
        self.set_labels()

        if labellines == True:
           self.add_line_labels()

    def set_labels(self):

        label_dic = {
          'q_lisflood': "water discharge ($m^3s^{-1}$)",
          'q_topmodel': "water (TOPMODEL) discharge ($m^3s^{-1}$)",
          'sed_tot': "sediment flux ($m^3$)"
        }

        self.ax.set_xlabel("simulation time (hours)")
        self.ax.set_ylabel(label_dic[self.metric_name])

    def make_line_label(self, fname):
        # Passing a list of delimiters to the re.split function
        part1 = re.split("[_.]", fname)[0]
        part2 = re.split("[_.]", fname)[1]
        part3 = re.split("[_.]", fname)[2]
        part4 = re.split("[_.]", fname)[3]

        part = part3 + ' ' + part4
        print part
        return part

    def add_line_labels(self):
        x_pos = [44.3, 45.8, 48, 52, 56, 60]
        labelLines(self.ax.get_lines(), zorder=2.5,
                   align=True, fontsize=10, xvals=x_pos)

    def save_figure(self, save_name="test.png"):
        self.fig.savefig(save_name, bbox_inches='tight')

    def create_inset_axes(self):
        ax_inset = zoomed_inset_axes(self.ax, 2, loc=1)

        cm = plt.get_cmap('winter')
        ax_inset.set_color_cycle([cm(1.*i/self.num_graphs)
                                 for i in range(self.num_graphs)])

        # hide every other tick label
        for label in ax_inset.get_xticklabels()[::4]:
            label.set_visible(False)

        return ax_inset

    def plot_inset(self, x_data, y_data):

        self.ax_inset.plot(x_data, y_data)
        self.ax_inset.set_xlim(39, 41)
        self.ax_inset.set_ylim(0, 100)

    def plot_legend(self):
        self.ax.legend(bbox_to_anchor=(1, 0.75),
               loc='center left', prop={'size': 11})

    def showfig(self):
        """
        Note: this will only work in GUI. If you are using an IPython
        console session, for example, just type CatchmentPlot.fig to re-draw
        the figure in the console.
        """
        self.fig.show()

    def plot_external_data(self, filename):
        """
        Plots external data, such as recorded discharge from
        a gauging station
        """
        x, y = np.loadtxt(filename, unpack=True, delimiter=',')
        hours = convert_timestep(x)
        line, = self.ax.plot(hours, y, '--k', linewidth=2)
        line.set_label("Measured")




# VARIABLES
data_dir = "/mnt/SCRATCH/Analyses/HydrogeomorphPaper/"
#data_dir = "/run/media/dav/SHETLAND/Analyses/HydrogeomorphPaper/BOSCASTLE/Analysis/"
#data_dir="/mnt/WORK/Dev/PyToolsPhD/Radardata_tools"
#data_dir = "/mnt/SCRATCH/Analyses/Topmodel_Sensitivity/Ryedale_storms_calibrate/"

input_raster2 = "elev.txt"
input_raster1 = "elevdiff.txt"
# input_raster2 = "rainfall_totals_boscastle_downscaled.asc"

# A text file with x, y scatter values, in case of future use
outpt_datafile_name = "elev_vs_erosion.txt"

fname = "boscastle_lumped_detachlim.dat"
wildcard_fname = "ryedale_*.dat"

external_file_data = "Ryedale72hours_measured.csv"


# Run the script
# elev, total_precip = create_data_arrays(data_dir, input_raster2, input_raster1)
# plot_scatter_rasterdata(elev, total_precip)

#plot_hydrograph(data_dir, fname, "q_lisflood", draw_inset=True)


# OOP way
BosHydroS = CaesarTimeseriesPlot(data_dir, "ryedale*.dat", "q_lisflood")
BosHydroS.plot_ensemble_hydrograph(draw_inset=False, labellines=False)
#BosHydroS.plot_external_data(data_dir + external_file_data)
BosHydroS.plot_legend()
BosHydroS.save_figure("Ryedale_rainfall_sens_hydrograph.svg")

# ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])






















