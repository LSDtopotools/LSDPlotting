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


"""Plots a hillshade overlain with the erossion or deposition amount"""

folder = "/mnt/DATA/DATA/VIRTUALBOX_SHARED/HydrogeomorphPaper/BOSCASTLE/PaperSimulations/Lumped/TransportLim/"
laptop_folder = ""

filename = "boscastle5m_bedrock_fill.asc"
drapename = "elevdiff4320.txt"

lsdplt.DrapedOverHillshade(folder + filename, folder + drapename, clim_val=(2,6), drape_cmap='jet')
