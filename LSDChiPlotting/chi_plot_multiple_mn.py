## chi_plot_multiple_mn.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function creates a chi-elevation plot (see Perron and Royden, 2012; An 
## integral approach to bedrock river profile analysis), for river profiles
## stored in the *.tree file. The trunk channel is highlighted distinctly from
## the tributary channels.  The user needs to specify the FileName,
## OutputFigureName and OutputFIgureFormat in the code.
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## DTM 07/11/2012
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## 
##
## This modified script now creates multiple plots for all channel tree files contained
## within the directory. Place all the *.tree files to be plotted in the same 
## directory with the python script and run from there.
## Change the data variables (l.68) to plot different paramaters
##
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## DAV 06/08/2013
## SMM 13/08/2013: Plots to powerpoint sized slides, also prints to files
##                  that store the m/n ratio and the basin number


#import modules
import numpy as np, matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
#import re

from glob import glob
from matplotlib import rcParams


#==============================================================================
# numbers = re.compile(r'(\d+)')               
# def numericalSort(value):                    
#     parts = numbers.split(value)             
#     parts[1::2] = map(int, parts[1::2])      
#     return parts
# This function enables numerical sorting of files
#==============================================================================

def make_plots():
    
    #DataDirectory =  'm:\\topographic_tools\\LSDRaster_chi_package\\PA\\'        
    #DataDirectory =  'c:\\code\\topographic_analysis\\LSDRaster_chi_package\\PA\\'
    #DataDirectory =  'c:\\code\\topographic_analysis\\LSDRaster_chi_package\\Child_runs\\'
    DataDirectory =  'c:\\code\\topographic_analysis\\LSDRaster_chi_package\\Test_data\\'
    
    # set sizes for fonts. These sizes are designed to be visible on a powerpoint
    # slide (10 inches x 7.5 inches) and at the same time be legible if this
    # slide is shrunk to 1 column width (85mm)
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

    for fname in glob(DataDirectory+"*fullProfileMC_forced*.tree"): # assigns a number to each iteration (i.e. for every .tree file in the directory)
        #print idx, fname 
        
        print fname
        split_fname = fname.split('\\')
        no_tree_levs = len(split_fname) 
        this_fname = split_fname[no_tree_levs-1]
        print "fname: "+fname+" and this fname: "+this_fname
        
        fname_prefix = this_fname.split('_fullProfileMC_')[0]
        print "fname prefix: " + fname_prefix
       
       # open file
        f = open(fname,'r')
        lines = f.readlines()[0:]   # read in the data           
        no_lines = len(lines)-1   # get the number of lines (=number of data)
        movn_value = this_fname.split('_')[4]    #get the value of m/n used 
        basin_name = this_fname.split('_')[5]
        basin_name = basin_name.split('.')[0]
    
        # get the A_0 and m/n values
        line = lines[0].strip().split(" ")
        A_0 = float(line[0]) 
        m_over_n = float(line[1]) 

        # set the name of the output figure
        OutputFigureName = DataDirectory+fname_prefix+'_' + movn_value+'_'+basin_name
        OutputFigureFormat = 'png'
        print OutputFigureName
    
        # data variables
        channel_id = np.zeros(no_lines, dtype=np.int)     # ID number for channel segment
    
        chi = np.zeros(no_lines)            # chi
        elev = np.zeros(no_lines)           # elevation
        fitted_elevation_mean = np.zeros(no_lines) #fitted elevation
    
        for i in range (0,no_lines):
            line = lines[i+1].strip().split(" ")
            #print line
            channel_id[i] = int(float(line[0]))
            chi[i] = float(line[7])
            elev[i] = float(line[8])
            fitted_elevation_mean[i] = float(line[20])       
        f.close()
  
        # get the segments  
        n_data = no_lines
        n_channel_segments = channel_id[n_data-1]+1
        segment_lengths = np.zeros(n_channel_segments, dtype=np.int)
        for i in range (0,n_data):
            segment_lengths[channel_id[i]] = segment_lengths[channel_id[i]] + 1   
 
        # SET UP COLOURMAPS
        jet = plt.get_cmap('jet')
    
        # channel ID
        Channel_ID_MIN = np.min(channel_id)
        Channel_ID_MAX = np.max(channel_id)
        cNorm_channel_ID  = colors.Normalize(vmin=Channel_ID_MIN, vmax=Channel_ID_MAX)  # the max number of channel segs is the 'top' colour
        scalarMap_channel_ID = cmx.ScalarMappable(norm=cNorm_channel_ID, cmap=jet)
           
        #########################
        #                       #
        #   MAKE CHI-PLOTS      #
        #                       #
        #########################    
        
        # set the size to that of a powerpoint slide
        plt.figure(1, facecolor='white',figsize=(10,7.5))
        ax = plt.subplot(1,1,1)
        # Set up colourmap for plotting channel segments
        jet = plt.get_cmap('jet')
        cNorm  = colors.Normalize(vmin=1, vmax=n_channel_segments)
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    
        
        # loop through the data, extracting each profile segment in turn   
        # this plots the data in chi-elevation space
        data_pointer = 0    # points to data element in chi and elev vectors
        for i in range (0,len(segment_lengths)):
            chi_seg = np.zeros(segment_lengths[i])
            elev_seg = np.zeros(segment_lengths[i])
            
            for j in range (0,segment_lengths[i]):
                chi_seg[j] = chi[data_pointer]
                elev_seg[j] = elev[data_pointer]
                data_pointer = data_pointer + 1
    
            if i == 0:
                # plot trunk stream in black, with thicker line 
                plt.plot(chi_seg, elev_seg, "k-", linewidth=4, alpha = 0.3)
            else:
                # plot other stream segments plot
                colorVal = scalarMap_channel_ID.to_rgba(i) # this gets the distinct colour for this segment
                plt.plot(chi_seg, elev_seg, "-", linewidth=4, color=colorVal, alpha = 0.3)
     
        # now loop again plotting the fitted segments    
        data_pointer = 0    # points to data element in chi and elev vectors
        for i in range (0,len(segment_lengths)):
            chi_seg = np.zeros(segment_lengths[i])
            elev_seg = np.zeros(segment_lengths[i])
            
            for j in range (0,segment_lengths[i]):
                chi_seg[j] = chi[data_pointer]
                elev_seg[j] = fitted_elevation_mean[data_pointer]
                data_pointer = data_pointer + 1
    
            if i == 0:
                # plot trunk stream in black, with thicker line 
                plt.plot(chi_seg, elev_seg, "k", linewidth=3, dashes=(10,2))
            else:
                # plot other stream segments plot
                colorVal = scalarMap_channel_ID.to_rgba(i) # this gets the distinct colour for this segment
                ax.plot(chi_seg, elev_seg, linewidth=3, color=colorVal, dashes=(10,2)) 
       
        # Configure final plot
        plt.xlabel('$\chi$ (m)', fontsize= axis_size)
        plt.ylabel('Elevation (m)', fontsize =axis_size)
        plt.title('$A_0$: '+str(A_0)+' m$^2$, and $m/n$: '+str(m_over_n), fontsize = label_size)  
 
        ax.spines['top'].set_linewidth(2.5)
        ax.spines['left'].set_linewidth(2.5)
        ax.spines['right'].set_linewidth(2.5)
        ax.spines['bottom'].set_linewidth(2.5) 
        ax.tick_params(axis='both', width=2.5) 
   
        plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
        plt.clf()
    
if __name__ == "__main__":
    make_plots()