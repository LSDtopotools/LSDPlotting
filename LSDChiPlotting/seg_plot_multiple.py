## seg_plot_multiple.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function creates a chi-elevation plot (see Perron and Royden, 2012; An 
## integral approach to bedrock river profile analysis), for river profiles
## stored in the *.Chi_tree file. The trunk channel is highlighted distinctly from
## the tributary channels.  The user needs to specify the FileName,
## OutputFigureName and OutputFIgureFormat in the code.
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## DTM 07/11/2012
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
##
## This function now creates chi plots best on the Chi_segment finding algorithm
## in the LSDRaster package. Each tributary is plotted as a different color
## identified by the colourbar of channel numbers. The mainstem is plotted as
## a thicker black line (channel no 0). The user can modify the script to plot 
## from different columns depending on the structure of the data file. (line 63 onwards)
##
## To do:
## At the moment the user must specify the number of header lines in the file
## at line 54ish (lines = f.readlines()[NUMBER OF HEADER LINES - 1])
## there will be a way to do this automatically
## difficult to identify channel number when there are more than about 10-15 channels
## perhaps add a label function to label each tributary?
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## DAV 2013-04-08
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.colors as colors
import matplotlib.cm as cmx

def make_plots():
    

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = 12

    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    # open file
    DataDirectory =  ''    
    FileName = 'francis136_AIC_best_fit_tree.chi_tree'
    OutputFigureName = 'seg_plot_test'
    OutputFigureFormat = 'png'
    f = open(DataDirectory + FileName,'r')  # open file
    lines = f.readlines()[95:]   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    channel_num = np.zeros(no_lines, dtype=np.int)     # channel number
    chi = np.zeros(no_lines)            # chi
    elev = np.zeros(no_lines)           # elevation
    best_elev = np.zeros(no_lines)  # best fit elevation
    
    for i in range (0,no_lines):
        line = lines[i].strip().split(" ")
        #print line
        channel_num[i] = int(float(line[0]))
        chi[i] = float(line[1])
        elev[i] = float(line[2])
        best_elev[i] = float(line[3])
   
    f.close()

    n_data = no_lines
    n_channel_segments = channel_num[n_data-1]+1
    segment_lengths = np.zeros(n_channel_segments, dtype=np.int)
    for i in range (0,n_data):
        segment_lengths[channel_num[i]] = segment_lengths[channel_num[i]] + 1   
        
    #########################
    #                       #
    #  MAKE SEGMENT-PLOTS   #
    #                       #
    #########################    
    
    plt.figure(1, facecolor='white')
    # Set up colourmap for plotting channel segments
    jet = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=1, vmax=n_channel_segments)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

#### A workaround to get a colourbar - DAV 8/11/2012 ########################
####=================================================########################
	
	# set the minimum and maximum values for the colourbar, 
    min, max = (0, n_channel_segments+1)
    step = 1
	
	# Using contourf to draw a plot for the colourbar
	# then get rid of the plot (but use it again later to get a colourbar)
    Z = [[0,0],[0,0]]
    levels = range(min,max+step,step)
    CB1 = plt.contourf(Z, levels, cmap=jet)
    plt.clf()    # clear the plot
	
##### back to making the actual plot... ######################################
		
    # loop through the data, extracting each profile segment in turn
    
    data_pointer = 0    # points to data element in chi and elev vectors
    for i in range (0,len(segment_lengths)):
        chi_seg = np.zeros(segment_lengths[i])
        elev_seg = np.zeros(segment_lengths[i])
        
        for j in range (0,segment_lengths[i]):
            chi_seg[j] = chi[data_pointer]
            elev_seg[j] = best_elev[data_pointer]
            data_pointer = data_pointer + 1

        if i == 0:
            # plot trunk stream in black, with thicker line 
            plt.plot(chi_seg, elev_seg, "k-", linewidth=2)
        else:
            # plot other stream segments plot
            colorVal = scalarMap.to_rgba(i) # this gets the distinct colour for this segment


            plt.plot(chi_seg, elev_seg, "b-", linewidth=0.5, color=colorVal)
 
    # Configure final plot
    plt.xlabel('$\chi$ / m')
    plt.ylabel('elevation / m')
	
    cbar = plt.colorbar(CB1,orientation='vertical')    # bring back the colourbar from the contour plot
    cbar.set_label('Channel Number')

    #plt.colorbar(jet,orientation='vertical')
    #plt.show()
    plt.savefig(OutputFigureName + '.' + OutputFigureFormat, format=OutputFigureFormat)
    
if __name__ == "__main__":
    make_plots()