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
from matplotlib.patches import Rectangle

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

# This is a custom module

from label_lines.label_lines import *


# Plotting parameters
def init_plotting():
    plt.rcParams['figure.figsize'] = (8, 8)
    plt.rcParams['font.size'] = 17
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['axes.labelsize'] = 1.2*plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 1.2*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['savefig.dpi'] = 2*plt.rcParams['savefig.dpi']
    plt.rcParams['xtick.major.size'] = 3
    plt.rcParams['xtick.minor.size'] = 3
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['ytick.major.size'] = 3
    plt.rcParams['ytick.minor.size'] = 3
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.width'] = 1
    plt.rcParams['legend.frameon'] = True
    plt.rcParams['legend.loc'] = 'center left'
    plt.rcParams['axes.linewidth'] = 1
    plt.rcParams['xtick.minor.visible'] = True
    plt.rcParams['ytick.minor.visible'] = True
    plt.rcParams['lines.linewidth'] = 1.5


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
        line, = self.ax.plot(hours, metric)
        line.set_label(line_label)
        #labelLine(line, 45)

        # Tweak the xlimits to zone in on the relevnat bit of hydrograph
        self.ax.set_xlim(39, 65)

        # Now plot the inset data
        if self.ax_inset is not None:
            self.plot_inset(hours, metric)



    def plot_ensemble_hydrograph(self, draw_inset=False):

        cm = plt.get_cmap('winter')
        self.ax.set_color_cycle([cm(1.*i/self.num_graphs) for i in range(self.num_graphs)])

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

        x_pos = [44.3, 45.8, 48, 52, 56, 60]
        labelLines(self.ax.get_lines(), zorder=2.5, align=True, fontsize=10, xvals=x_pos)

    def set_labels(self):

        label_dic = {
          'q_lisflood': "water discharge ($m^3s^{-1}$)",
          'q_topmodel': "water (TOPMODEL) discharge ($m^3s^{-1}$)",
          'sed_tot': "sediment flux ($m^3$)"
        }

        self.ax.set_xlabel("simulation time (hours)")
        self.ax.set_ylabel(label_dic[self.metric_name])

    def make_line_label(self, fname):
        part = fname.split('_')[0]
        # part = "m = " + part
        print part
        return part

    def save_figure(self, save_name="test.png"):
        self.fig.savefig(save_name, bbox_inches='tight')

    def create_inset_axes(self):
        ax_inset = zoomed_inset_axes(self.ax, 2, loc=1)

        cm = plt.get_cmap('gist_rainbow')
        ax_inset.set_color_cycle([cm(1.*i/self.num_graphs)
                                 for i in range(self.num_graphs)])

        # hide every other tick label
        for label in ax_inset.get_xticklabels()[::2]:
            label.set_visible(False)

        return ax_inset

    def plot_inset(self, x_data, y_data):

        self.ax_inset.plot(x_data, y_data)
        self.ax_inset.set_xlim(39, 42)
        self.ax_inset.set_ylim(90, 160)

    def plot_legend(self):
        extra = Rectangle((0, 0), 1, 1,
                          fc="w",
                          fill=False,
                          edgecolor='none',
                          linewidth=0)

        handles, labels = self.ax.get_legend_handles_labels()
        handles.insert(0,extra)
        labels.insert(0, "Modelled discharge \n$m$ value:")

        self.ax.legend(handles, labels,
                       #bbox_to_anchor=(0.75, 0.75),
                       loc='top right')

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
        line.set_label("Measured discharge")




# VARIABLES
#data_dir = "/mnt/SCRATCH/Analyses/HydrogeomorphPaper/"
# data_dir = "/run/media/dav/SHETLAND/Analyses/HydrogeomorphPaper/BOSCASTLE/Analysis/"
# data_dir="/mnt/WORK/Dev/PyToolsPhD/Radardata_tools"
data_dir = "/mnt/SCRATCH/Analyses/Topmodel_Sensitivity/Ryedale_storms_calibrate/"

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

init_plotting()
# OOP way
BosHydro = CaesarTimeseriesPlot(data_dir, "*.dat", "q_lisflood")
BosHydro.plot_ensemble_hydrograph(draw_inset=False)
BosHydro.plot_external_data(data_dir + external_file_data)
BosHydro.plot_legend()
#BosHydro.save_figure("Ryedale_M_sens_hydro.svg")

# ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])






















