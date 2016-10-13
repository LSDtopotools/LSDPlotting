# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 10:50:27 2016

Catchment Model plotter

This tool is to plot the output from the Catchment Model
as a series of rasters and overlays of different data,
e.g. Hillshade overlaid by erosion/deposition amounts, or water depth
or d50 size, etc.

@author: dav
"""

import LSDPlottingTools as lsdplt
import LSDPlottingTools.LSDMap_GDALIO as mapio # fun trivia: this is Welsh for 'mapping'.
import numpy as np


"""Plots a hillshade overlain with the erossion or deposition amount"""

folder = "/mnt/DATA/DATA/VIRTUALBOX_SHARED/HydrogeomorphPaper/BOSCASTLE/PaperSimulations/Radar1km/TransLim/"
laptop_folder = ""

filename = "boscastle5m_bedrock_fill.asc"
drapename = "waterdepth2400.txt"

# Create the drape array from one of the Catchment model output rasters
drape_array = mapio.ReadRasterArrayBlocks(folder + drapename)
# Optional: A lot of the output rasters contain very small values for certain 
# things like water depth or elevation difference, so you can mask this below:
low_values_index = drape_array < 0.005
drape_array[low_values_index] = np.nan

# Alternatively you can just pass the name of a secondary drape raster instead
# of an array below: The function takes either a string or a ready-extracted array.
lsdplt.DrapedOverHillshade(folder + filename, drape_array, clim_val=(0,400), \
drape_cmap='Blues', colorbarlabel='Elevation in meters'\
,ShowColorbar=True, ShowDrapeColorbar=True, drape_cbarlabel = "Water depth (m)")
