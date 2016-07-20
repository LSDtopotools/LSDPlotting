# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 11:20:58 2014

@author: smudd
"""




def azimuthalAverage(image, center=None):

    import numpy as np

    """
    Calculate the azimuthally averaged radial profile.

    image - The 2D image
    center - The [x,y] pixel coordinates used as the center. The default is 
             None, which then uses the center of the image (including 
             fracitonal pixels).
    
    """
    # Calculate the indices from the image
    y, x = np.indices(image.shape)

    if not center:
        center = np.array([(x.max()-x.min())/2.0, (x.max()-x.min())/2.0])

    r = np.hypot(x - center[0], y - center[1])

    # Get sorted radii
    ind = np.argsort(r.flat)
    r_sorted = r.flat[ind]
    i_sorted = image.flat[ind]

    # Get the integer part of the radii (bin size = 1)
    r_int = r_sorted.astype(int)

    # Find all pixels that fall within each radial bin.
    deltar = r_int[1:] - r_int[:-1]  # Assumes all radii represented
    rind = np.where(deltar)[0]       # location of changed radius
    nr = rind[1:] - rind[:-1]        # number of radius bin
    
    # Cumulative sum to figure out sums for each radius bin
    csim = np.cumsum(i_sorted, dtype=float)
    tbin = csim[rind[1:]] - csim[rind[:-1]]

    radial_prof = tbin / nr

    return radial_prof


def read_headers(input_file):

    with open(input_file+'.hdr','r') as f:   
        return [float(h) if not h.isalpha() else h for h in [l.split()[1] for l in f.readlines()]]  #isdigit() does not catch floats      


def read_flt(input_file):

    if input_file.endswith('.flt') or input_file.endswith('.hdr'):
        input_file = input_file[:-4]    
    else:
        print 'Incorrect filename'
        return 0,0 #exits module gracefully
    
    headers = read_headers(input_file)
    
    #read the data as a 1D array and reshape it to the dimensions in the header
    raster_array = read_bin(input_file).reshape(headers[1], headers[0]) 
    raster_array = raster_array.reshape(headers[1], headers[0]) #rows, columns

    return raster_array, headers

def read_bin(filename):
    import sys
    import numpy as np

    with open(filename + '.flt', "rb") as f:
        raster_data = np.fromstring(f.read(), 'f')

    if sys.byteorder == 'big':
        raster_data = raster_data.byteswap()  #ensures data is little endian

    return raster_data

def test_fft_DS(DS_file):

    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    from matplotlib import rcParams
    import numpy as np
    
    DS_raster, DS_header = read_flt(DS_file)
    
    print "The size of your raster is:"
    print DS_raster.shape    
    
    #plt.imshow(DS_raster)

    #plt.show()
 
    from scipy import fftpack

    
    F1 = fftpack.fft2(DS_raster)
    
    print "The size of your fftarray is:"
    print F1.shape
    
    # get the shifted 
    F2 = fftpack.fftshift( F1 )
    
    # get the power
    psd2D = np.abs( F2 )**2
    
    # Calculate the azimuthally averaged 1D power spectrum
    psd1D = azimuthalAverage(psd2D)

    # Now plot up both
    plt.loglog( psd1D )
    plt.xlabel('Spatial Frequency')
    plt.ylabel('Power Spectrum')
    
    plt.show()

test_fft_DS('c:\\code\\topographic_analysis\\LSDRaster_local\\Data\\Rio_Torto\\rio_torto_DS.flt')    
    

