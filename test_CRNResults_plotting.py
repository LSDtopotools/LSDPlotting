# -*- coding: utf-8 -*-
"""
Created on Tue Nov 03 17:12:17 2015

@author: smudd
"""

import CRNResults_plotting as CRNRP


# A test of the results plotting
def Test_CRNRP():
    
    DataDirectory = "T://test_clone//topodata//CRNResults//"  
    #DataDirectory = "/home/smudd/SMMDataStore/Git_projects/LSDPlotting/"
    
    # get some data
    prefixes, CRNResults =  CRNRP.GatherCRNResults(DataDirectory) 
    
    print "Erosion rates are: "
    print CRNResults[0]['erate_g_percm2_peryr']
    

if __name__ == "__main__":
    #fit_weibull_from_file(sys.argv[1]) 
    Test_CRNRP() 