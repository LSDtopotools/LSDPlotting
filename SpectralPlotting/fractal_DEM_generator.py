# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 21:02:48 2014

@author: http://shortrecipes.blogspot.co.uk/
@author: DAV (General faffing with classes)
@author: SMM (The 'beta' method)

fractal_terrain_generation.py

Two methods for generating fractal terrain.

Using the main() function at the bottom, you can 
generate fractal landscapes of a given fractal dimension. They either plot
to the screen or you can save them as an ASCII DEM. You could also create a 
driver file to call the funcions, a la LSDTopoTools driver files.

Both these methods seem to produce very similar results. I suspect they are just
different implementations. (The Saupe algorithm is just under twice as fast)
Using the main() function at the bottom, you can generate fractal landscapes 
of a given fractal dimension. 
They either plot to the screen or you can save them as an ASCII DEM or TIFF

For the beta method, beta values in the 5-10 range will produce very smooth landscapes.
for the fractal dimension method, fd = 2-3 is supposedly closest to nature, but lower 
values will produce smoother terrain. 

The _truncate variations will fill the elevations below a certain elevation, to 
give the effect of a flat valley floor.

Requirements:
    Python 2.7
    SciPy
    NumPy
    # PIL only for saving as a tiff file
    
"""

from __future__ import division
from PIL import Image
from scipy import fftpack
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

import numpy as np
import scipy as scp

class FractalSurface(object):
    '''Generate isotropic fractal surface image using
    spectral synthesis method [1, p.]
    References:
    1. Yuval Fisher, Michael McGuire,
    The Science of Fractal Images, 1988
    '''
    
    def __init__(self,fd=1.5, N=2048):
        self.N=N
        self.H=1-(fd-2);
        self.X=np.zeros((self.N,self.N),complex)
        self.A=np.zeros((self.N,self.N),complex)
        self.img=Image.Image()
        
        self.beta=1.5
    
    def genSurface(self):
        '''Spectral synthesis method
            This is almost verbatim translated from Saupe 1987
            Algorithms for Random Fractals
        '''
        N=self.N; A=self.A
        powerr=-(self.H+1.0)/2.0
        
        for i in range(int(N/2)+1):
            for j in range(int(N/2)+1):
        
                phase=2*scp.pi*scp.rand()
                
                if i is not 0 or j is not 0:
                    rad=(i*i+j*j)**powerr*scp.random.normal()
                else:
                    rad=0.0
                
                self.A[i,j]=complex(rad*np.cos(phase),rad*np.sin(phase))
                
                if i is 0:
                    i0=0.0
                else:
                    i0=N-i
                if j is 0:
                    j0=0.0
                else:
                    j0=N-j
                
                self.A[i0,j0]=complex(rad*np.cos(phase),-rad*np.sin(phase))
                
                
        self.A.imag[N/2][0]=0.0
        self.A.imag[0,N/2]=0.0
        self.A.imag[N/2][N/2]=0.0
                
        for i in range(1,int(N/2)):
            for j in range(1,int(N/2)):
                phase=2*scp.pi*scp.rand()
                rad=(i*i+j*j)**powerr*scp.random.normal()
                self.A[i,N-j]=complex(rad*np.cos(phase),rad*np.sin(phase))
                self.A[N-i,j]=complex(rad*np.cos(phase),-rad*np.sin(phase))
                
        itemp=fftpack.ifft2(self.A)
        itemp=itemp-itemp.min()
        self.X=itemp 
        
    def genSurface_beta(self):
        # SMM method
        # this sets the size of the array. 
        N=self.N
        
        # get now the beta value (that is, the slope of the
        # 1D power spectrum in log-log space)
        beta = self.beta
    
        # first make a random array   
        randarray = np.random.rand(N,N)
       
        # initialize the array for the inverse fourier transform
        freq_scaled_real = np.zeros((N,N))
        freq_scaled_imaginary = np.zeros((N,N))
        
        # now get the FFT of the random surface
        F1 = fftpack.fft2(randarray)
      
        # get the frequency coordinate
        freq = np.fft.fftfreq(N)    
        
        #freq = np.fft.fftshift(freqs)
        radial_freq = np.zeros((N,N))
        scaling = np.zeros((N,N))
           
        for row in range (0,N):
            for col in range (0,N):
                radial_freq[row][col] = np.sqrt(freq[row]**2+freq[col]**2)
                
                if (radial_freq[row][col] == 0):
                    freq_scaled_real[row][col] = 0
                    freq_scaled_imaginary[row][col] = 0
                    scaling[row][col] = 0
                else:
                    freq_scaled_real[row][col] = F1.real[row][col]/(radial_freq[row][col]**beta)
                    freq_scaled_imaginary[row][col] = F1.imag[row][col]/(radial_freq[row][col]**beta)
                    scaling[row][col] = 1/(radial_freq[row][col]**beta)
        
        freq_scaled = freq_scaled_real + 1j*freq_scaled_imaginary
                          
        fractal_surf = np.fft.ifft2(freq_scaled)
        
        #real_fracsurf = fractal_surf.real
        
        self.X = fractal_surf
    
    def genTerrain(self):
        #Aa=abs(Aa)
        Aa = self.X
        self.terrain = Aa.real/Aa.real.max()*255.0  # could make this multiplier a variable
     
    # sets a flat valley floor at a given base elevation 
    def genTerrain_truncated(self, base_elev=100.0):
        Aa = self.X
        terrain1 = Aa.real/Aa.real.max()*255.0
        base_level_indices = terrain1 < base_elev
        
        terrain1[base_level_indices] = base_elev
        self.terrain = terrain1
   
    def show3DPlot(self):
        x, y = np.mgrid[0:self.N, 0:self.N]
        fig = plt.figure()
        ax = axes3d.Axes3D(fig)
        ax.view_init(40.,60.)
        ax.plot_surface(x, y, self.terrain, cstride=10,rstride=10)
        #plt.draw()
        plt.show()
    
    def genImage(self):
        self.img=Image.fromarray(scp.uint8(self.terrain))
        #img2=Image.fromstring("L",(N,N),uint8(terrain).tostring()) 
        #plt.imshow(terrain)
    
    def showImg(self): 
        self.img.show()
    
    def saveImg(self,fname="fs.tiff"):
        self.img.save(fname)
    
    def getFSimg(self):
        return self.img
        
    def saveDEM(self, fname="fractalsurf", ext=".asc", precision="%1.5f"):
        # Create the ASCII header information
        Ncols = str(self.N)
        Nrows = str(self.N)
        xllcorner = str(0.000)
        yllcorner = str(0.000)
        cellsize = str(10) 
        nodataval = str(-9999)
        
        # create the header for ESRI ASCII file (note the bug in the formatting)
        header = ("ncols " + Ncols + "\n" + "nrows " + Nrows + "\n" + "xllcorner " + xllcorner + "\n" + "yllcorner " + yllcorner + "\n" + "cellsize " + cellsize + "\n" + "nodata_value " + nodataval)
        # save DEM to file, note the abs() part to make the values positive in the DEM
        np.savetxt(fname+ext, self.terrain, fmt=precision, header=header)
    
def main():
    fs=FractalSurface()
    #fs.genSurface()
    fs.genSurface_beta()
    fs.genTerrain()
    #fs.genTerrain_truncated()
    fs.show3DPlot()
    #fs.saveImg()
    #fs.showImg()
    #fs.saveDEM()    # you can overwrite the defaults in many of these function calls

if __name__ == '__main__':
   main() 