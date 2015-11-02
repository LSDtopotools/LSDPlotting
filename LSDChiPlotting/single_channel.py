##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## This function creates a chi-elevation plot (see Perron and Royden, 2012; An 
## integral approach to bedrock river profile analysis), for river profiles
## stored in the *.tree file. 
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## DTM 07/11/2012
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

## Addition DAV 11/11/12
## This script, based on the original chi_plot.py script, plots single
## channels from the *.tree file. At the command line, use the option [-w] followed by the number 
## of the channel to be plotted. The main trunk channel is 0. i.e: ./python single.py -w 34 would
## plot channel no 34.


#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.colors as colors
import matplotlib.cm as cmx

from optparse import OptionParser

	
def make_plots():
    
	#################################
	#								                #
	#	   SET COMMAND LINE OPTIONS	  #
	#		    AND DEFAULTS			      #
	#								                #
	#################################

    usage = "usage: %prog [-o (option switch) argument (string)]"
    parser = OptionParser(usage=usage)
    parser.set_defaults(inputfile="ChannelTree.tree", outputfile="plot", filetype="png")
    #parser.add_option("-i", "--inputfile", type="string", dest="inputfile", help="set the input filename.extension")
    parser.add_option("-o", "--outputfile", type="string", dest="outputfile", help="set the output file name")
    parser.add_option("-f", "--filetype", type="string", dest="filetype", help="set the file type, e.g. png")
    parser.add_option("-s", "--show", action="store_true", dest="showgraph", default=False, help="show the graph, instead of saving a file")
    parser.add_option("-w", "--single", type="int", dest="channel_no", default="0", help="creates a plot of an indivdual channel's elevation against chi. 0 is the main trunk channel.")
    parser.add_option("-n", "--startnode", type="string", dest="start_node", default="none", help="enter the junction index for the starting node of the channel, this should be the same as the ChannelTree.tree file number")
    parser.add_option("-d", "--demname", type="string", dest="demname", default="default", help="the DEM name of the ChannelTree file to be read in")
	
    (options, args) = parser.parse_args()
	
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
    #FileName = options.inputfile
    FileName = options.start_node + '_' + options.demname + '_ChannelTree.tree'     # open the relevant ChannelTree file
    OutputFigureName = options.demname + '_' + options.start_node + '_chi_plot_mainstem'
    OutputFigureFormat = options.filetype
#     try:
#       with open(DataDirectory + FileName,'r') as f: pass
#     except IOError as e:
#       print 'File IO error - did you enter the correct file name?'  # open file

# ^above didn't work DAV 5/2/13
    
    f = open(DataDirectory + FileName,'r')
    lines = f.readlines()   # read in the data
    no_lines = len(lines)   # get the number of lines (=number of data)

    # data variables
    channel_id = np.zeros(no_lines, dtype=np.int)     # ID number for channel segment
    node = np.zeros(no_lines, dtype=np.int)           # node number
    row = np.zeros(no_lines, dtype=np.int)            # row
    col = np.zeros(no_lines, dtype=np.int)            # column
    flow_dist = np.zeros(no_lines)      # flow distance
    chi = np.zeros(no_lines)            # chi
    elev = np.zeros(no_lines)           # elevation
    drainage_area = np.zeros(no_lines)  # drainage area
    
    for i in range (0,no_lines):
        line = lines[i].strip().split(" ")
        #print line
        channel_id[i] = int(float(line[0]))
        node[i] = int(float(line[1]))
        row[i] = int(float(line[2]))
        col[i] = int(float(line[3]))
        flow_dist[i] = float(line[4])
        chi[i] = float(line[5])
        elev[i] = float(line[6])
        drainage_area[i] = float(line[7])
   
    f.close() 
  	
	  #########################
    #                       #
    #   PLOTTING SINGLE		  #
    #		CHANNELS		        #
    #                       #
    #########################
	
	# get all the values when for a particular channel number (options.channel_no)
    # single_channel = [i for i in channel_id if i == options.channel_no]
	
    # print single_channel
    # number_points = len(single_channel)
    # print number_points
	
	#  for plotting a single channel, we want to use only the rows that have the same channel number
	# convert the chi line into an array
    chi_array = np.array(chi)
	# convert the channel_id line into an array
    channel_array = np.array(channel_id)
	# take out the chi values for the corresponding channel number
    short_chi_array = chi_array[channel_array==options.channel_no]
    # print short_chi_array 
	
	
	# convert the flow_dist line into an array
    fdist_array = np.array(flow_dist)
	# take out the flow_dist values for the corresponding channel number
    short_fdist_array = fdist_array[channel_array==options.channel_no]
    # print short_fdist_array	
	
	# convert the elevation line into an array
    elev_array = np.array(elev)
	# take out the elev values for the corresponding channel number
    short_elev_array = elev_array[channel_array==options.channel_no]
    # print short_elev_array		

    n_data = no_lines
    n_channel_segments = channel_id[n_data-1]+1
    segment_lengths = np.zeros(n_channel_segments, dtype=np.int)
	
    plt.figure(4, facecolor='white')
		
    plt.plot(short_chi_array, short_elev_array)
		
    # Configure final plot
    plt.xlabel('$\chi$ / m')
    plt.ylabel('elevation / m')
		
    if options.showgraph == True:
	    plt.show()
    else:
        plt.savefig(OutputFigureName + '_' + "channel_no" + str(options.channel_no) + '.' + OutputFigureFormat, format=OutputFigureFormat)
			        
if __name__ == "__main__":
    make_plots()