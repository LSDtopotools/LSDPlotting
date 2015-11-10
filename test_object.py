# -*- coding: utf-8 -*-
"""
Created on Wed Nov 04 07:26:25 2015

@author: smudd
"""

import CRNResults as CRNR

def TestCRNObject():
    
    
    #FileName = "C://code//devel_projects//LSDPlotting//SanBernData//SanBern_Spawned_CRNResults.csv"
    FileName = "T://test_clone//topodata//CRNResults//SanBern_Spawned_CRNResults.csv"
    CRONUSFileName = "T://test_clone//topodata//CRNResults//SanBern_Spawned_CRONUS.csv"
    
    
    thisCRNData = CRNR.CRNResults(FileName)
    #thisCRNData.GetParameterNames(True)
    
    print "Erosion rates are: "    
    thisCRNData.GetErosionRates(True)
        
    print "Now I will translate to a shapefile"
    thisCRNData.TranslateToReducedShapefile(FileName)
    
    print "Now to geojson"
    thisCRNData.TranslateToReducedGeoJSON(FileName)
    
    print "Now getting CRONUS data"
    #thisCRNData.PlotERateErrorsGridSpec(CRONUSFileName)
    
    
    thisCRNData.PlotERateErrorsRefined(CRONUSFileName)
    
if __name__ == "__main__":
    TestCRNObject() 