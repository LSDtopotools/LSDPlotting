# -*- coding: utf-8 -*-
# This code is used to fit a 3 exponential production model for 10Be. 
# It is used to cast the new COSMOCALC production calculations in a format 
# Compatible with the CAERN model
"""
Created on Fri Jan 29 10:56:52 2016

@author: smudd
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit # Import the curve fitting module
import os
import LSDOSystemTools as LSDOst

# this function calculates the root mean square error
def RMSE(data,prediction):
    sum_err = 0
    n = len(data)
    residual = []
    for d,p in zip(data,prediction):
        sum_err = (p-d)*(p-d)
        residual.append(p-d)
    resid = np.asarray(residual)
    sq_resid = np.power(resid,2)
    
    #print "The square residuals are: "
    print sq_resid    
    RMSE = np.sqrt(sum_err/n)
    return RMSE


def ReadProdData(prod_fname):
  #See if the parameter files exist
  if os.access(prod_fname,os.F_OK):
    this_file = open(prod_fname, 'r')
    lines = this_file.readlines()
            
    EffDepth = []
    TotalProd = []
    SpallationProd = [] 
    MuonProd = [] 
    
    # get rid of the first two lines
    lines.pop(0)
    lines.pop(0)
        
    # now get the data into the dict
    for line in lines:
      this_line = LSDOst.RemoveEscapeCharacters(line)
      split_line = this_line.split(',')
 
      EffDepth.append(float(split_line[0]))
      TotalProd.append(float(split_line[1]))
      SpallationProd.append(float(split_line[2]))
      MuonProd.append(float(split_line[3])) 
      
    return EffDepth,TotalProd,SpallationProd,MuonProd  

# This returns a production curve in atms/g/yr 
def ThreeExpProdCurve(eff_depths,F1,Gamma1,F2,Gamma2):

    # These numbers have been extracted from Shasta's production curve    
    P_HLSL = 4.075213
    F0 = 0.98374
    Gamma0 = 160.0

    production = []    
    for depth in eff_depths:
        this_prod = P_HLSL*(F0*np.exp(-depth/Gamma0)+F1*np.exp(-depth/Gamma1)+F2*np.exp(-depth/Gamma2))
        production.append(this_prod)
        
    return np.asarray(production)

def ProductionCurveFit(filename):

    # first, load the file
    EffDepth,TotalProd,SpallationProd,MuonProd = ReadProdData(filename)
    ED2 =  np.asarray(EffDepth)
    TP2 =  np.asarray(TotalProd)
    
    
    #reduce the data a bit
    #ED = EffDepth[0::100]  
    #TP = TotalProd[0::100]
    
    #print ED
    #print TP
    
    #ED2 = np.asarray(ED)
    #TP2 = np.asarray(TP)
    
    #print EffDepth
    #print TotalProd
    
    # Test some values
    F1 = 0.0027
    Gamma1 = 1500
    F2 = 0.0086
    Gamma2 = 4320    

    # new initial guess    
    initial_guess = [F1,Gamma1,F2,Gamma2]
    
    print "The initial guesses are: "
    print initial_guess

    #Yo = ThreeExpProdCurve(EffDepth,F1,Gamma1,F2,Gamma2)
        
    #print Yo

    # now fit the erosion data to a double gaussian
    #popt_bl, pcov_bl = curve_fit(ThreeExpProdCurve,EffDepth,TotalProd,initial_guess)
    #popt_dg, pcov_dg = curve_fit(sd.double_gaussian, depth, erate)   
    popt_bl, pcov_bl = curve_fit(ThreeExpProdCurve,ED2,TP2,initial_guess)
   
    # get the fitted pdf
    print "The fitted components are: "
    print "F1: " + str(popt_bl[0])
    print "Gamma1: " + str(popt_bl[1])
    print "F2: " + str(popt_bl[2])
    print "Gamma2: " + str(popt_bl[3])    
    ProdPrediction = ThreeExpProdCurve(EffDepth,popt_bl[0],popt_bl[1],popt_bl[2],popt_bl[3])        
        
    RMSE_val =  RMSE(TotalProd,ProdPrediction)
    print "The RMSE is: " + str(RMSE_val)
    
    PlotProFit(EffDepth,TotalProd,ProdPrediction)        
    
    return EffDepth,TotalProd,popt_bl,ProdPrediction,RMSE_val



# This function plots the results from the fitting
def PlotProFit(EffDepth,TotalProd,ProdPrediction):      

    ## PLOT THE GRAPH
    plt.figure(figsize=(12,6))
    
    # The first subplot is the data, and the truncated data
    ax1=plt.subplot(111)
    ax1.plot(TotalProd,EffDepth,'ro',label='data')    
    ax1.plot(ProdPrediction,EffDepth,'ko',label='fit data')  
    ax1.invert_yaxis()
    plt.xlabel('Data and fit, in Production rate atoms/g/yr')
    plt.ylabel('Effective depth, g/cm^2')
    ax1.legend(loc='lower right')

    
    #plot_fname = "Fit_plot_bl.png"
    #plt.savefig(plot_fname, format='png')
    #plt.clf()
    plt.show()

    
if __name__ == "__main__":

    filename = 'T:\\Git_projects\\LSDPlotting\\CRONUSScalcProd.csv'    
    ProductionCurveFit(filename)
    #plot_SWE_effD_fit(elevations,SWE_in_effDepth,popt_bl,SWE_bl_fit,RMSE_val)