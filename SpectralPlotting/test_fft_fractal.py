# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 13:18:50 2014

@author: smudd
"""

def test_fft_fractal():

    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    from matplotlib import rcParams
    import numpy as np
    
    from scipy import fftpack

    # this sets the size of the array. 
    array_power =10 
    array_size = 2**array_power
    
    # get now the beta value (that is, the slope of the
    # 1D power spectrum in log-log space)
    beta = 1.5
    
    print "array size is: " + str(array_size)
    
    # first make a random array   
    randarray = np.random.rand(array_size,array_size)
 
    plt.imshow(randarray)

    plt.show()
   
    # initialize the array for the inverse fourier transform
    freq_scaled_real = np.zeros((array_size,array_size))
    freq_scaled_imaginary = np.zeros((array_size,array_size))
        
    # print randarray
    
    # now get the FFT of the random surface
    F1 = fftpack.fft2(randarray)
    
    # get the FFT transformed data
    #F2 = fftpack.fftshift( F1 )  
    
  
    #plt.imshow(F2.real)

    #plt.show()


    #F2_backshift = np.fft.ifftshift(F2)
    #reconstruct = np.fft.ifft2(F2_backshift)
    
    #print "orig: "
    #print randarray
    
    #print "reconstruct: "
    #print reconstruct
    
    

    #plt.imshow(np.fft.ifft2(F2))
    #plt.show()

  
    # get the frequency coordinate
    freq = np.fft.fftfreq(array_size)    
    
    #freq = np.fft.fftshift(freqs)
    radial_freq = np.zeros((array_size,array_size))
    scaling = np.zeros((array_size,array_size))
    
    print "Frequency: " + str(freq)
       
    for row in range (0,array_size):
        for col in range (0,array_size):
            radial_freq[row][col] = np.sqrt(freq[row]**2+freq[col]**2)
            
            if (radial_freq[row][col] == 0):
                freq_scaled_real[row][col] = 0
                freq_scaled_imaginary[row][col] = 0
                scaling[row][col] = 0
            else:
                freq_scaled_real[row][col] = F1.real[row][col]/(radial_freq[row][col]**beta)
                freq_scaled_imaginary[row][col] = F1.imag[row][col]/(radial_freq[row][col]**beta)
                scaling[row][col] = 1/(radial_freq[row][col]**beta)
 
    #print "radial freq: "
    #print radial_freq
    
    #plt.imshow(freq_scaled_real)

    #plt.show()
    
    freq_scaled = freq_scaled_real + 1j*freq_scaled_imaginary
 
    #print "freq_scaled_real"
    #print freq_scaled_real
    
    #print "freq_scaled_imaginary"
    #print freq_scaled_imaginary
 
    #print "And freq_scaled: "
    #print freq_scaled

    #freq_scaled_backshift = np.fft.ifftshift(freq_scaled)
                      
    fractal_surf = np.fft.ifft2(freq_scaled)
    
    print "Factal surf is: "
    #print fractal_surf
    
    real_fracsurf = fractal_surf.real
        
    
    plt.imshow(real_fracsurf)

    plt.show()
            
            
    
            
    
test_fft_fractal()