## Analysis_categorical_boxplots.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## Script displaying the data contained in the compil-data-MAH.csv 
## table in the form of boxplots for the global dataset and categorical subsets 
## (litholohy, climate, tectonics). The user needs to specify the filter for the data 
## (all data, p<0.1 data or fixed m/n=0.45) 
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
## Marie-Alice Harel - 2014
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#import modules
import numpy as np, matplotlib.pyplot as plt
from matplotlib import rcParams
#from scipy import stats
#import csv
import pandas
from scipy.stats import gaussian_kde
from numpy import arange
#import matplotlib.gridspec as gridspec


def make_plots():
    
    label_size = 30
    axis_size = 40

    # Set up fonts for plots
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['arial']
    rcParams['font.size'] = label_size
    
    #************** USER'S CHOICE********************************#
    
    # Dataset: 
        #   all data    = 0
        #   p<=1        = 1
        #   fixed m/n   = 2 
    datach = 2
        
    # Save figures as png (1 to save, otherwise 0):
    safi = 1
    
    # Display log10 K instead of K
    log10K = 1
    
    #***********************************************************#    
    
    #########################
    #                       #
    #   READ IN THE DATA    #
    #                       #
    #########################

    # Load the data into a DataFrame
    if datach == 2:
        data = pandas.read_csv('fixed_movern_trustworthy.csv')
    else:
        data = pandas.read_csv('compil-data-MAH.csv')

    data.info()
    dataff = data[(data.zone > 0.1)].copy()
    
    if datach == 0:
        datatitle = 'ALL DATA'
        fileref = 'ALL_DATA'
    elif datach == 1:
        datatitle = 'p<=0.1 DATA'
        fileref = 'TRUST_DATA'
    elif datach == 2:
        datatitle = 'FIXED m/n'
        fileref = 'FIXED_MN'
        
    #########################
    #                       #
    #      MAKE PLOTS       #
    #                       #
    #########################    
    # List all the zones
    #--------------------
    lengzonall = len(dataff)
    all_list = []
    all_movern = []
    p_movern = []
    for zoo in range(1,lengzonall-1):
        if dataff.zone[zoo]-dataff.zone[zoo+1] != 0:
           all_list.append(int(dataff.zone[zoo]))   
           all_movern.append(dataff.m_over_n[zoo])
           if dataff.p_loglog_linregress[zoo] <= 0.1 :
               p_movern.append(dataff.m_over_n[zoo])
    all_list.append(int(dataff.zone[lengzonall-1]))    
    print "All zones : " +str(all_list)
   
    # Trustworthy zones using a threshold on p
    #-------------------------------------------
    datap = dataff[(dataff.p_loglog_linregress <= 0.1)] 
    datap = datap.reset_index(drop=True)
    lengzon = len(datap)
    trust_list = []

    for zo in range(1,lengzon-1):
        if datap.zone[zo]-datap.zone[zo+1] != 0:
           trust_list.append(int(datap.zone[zo]))   
           
    trust_list.append(int(datap.zone[lengzon-1]))    
    print "Zones for which p<=0.1 are : " +str(trust_list)

    #----------
    print "Total number of zones : " +str(len(all_list))
    print "Number of trustworthy zones : " +str(len(trust_list))


    # SD ERROR LOG-LOG LINEREGRESS & co for zone numbers
    #===============================================  
    yplotmax = 2
    xmaxaxis = np.max(len(all_list))
  
    plt.figure(1, facecolor='white',figsize=(20,20))  
    ax = plt.subplot(2,2,1)
    yplotmax = np.max(dataff['Std_error_loglog_linregress'])
    for zz in all_list:
        datatempzone = dataff[(dataff.zone == zz)]
        ymaxz = np.min(datatempzone['Std_error_loglog_linregress'])
        if zz in trust_list:
            plt.axvline(x=zz, ymin=0, ymax=ymaxz/yplotmax, color='r')
        else:
            plt.axvline(x=zz, ymin=0, ymax=ymaxz/yplotmax, color='b')
    plt.plot(dataff['zone'], dataff['Std_error_loglog_linregress'], "o", markersize=8, color='b')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('zone number', fontsize = axis_size-2)
    plt.ylabel('Std_error_loglog_linregress', fontsize = axis_size-2)
    plt.axis([0, xmaxaxis, 0, yplotmax])

    ax = plt.subplot(2,2,2)
    yplotmax = np.max(dataff['R_loglog_linregress']*dataff['R_loglog_linregress'])
    for zz in all_list:
        datatempzone = dataff[(dataff.zone == zz)]
        ymaxz = np.min(datatempzone['R_loglog_linregress']*datatempzone['R_loglog_linregress'])
        if zz in trust_list:
            plt.axvline(x=zz, ymin=0, ymax=ymaxz/yplotmax, color='r')
        else:
            plt.axvline(x=zz, ymin=0, ymax=ymaxz/yplotmax, color='g')
    plt.plot(dataff['zone'], dataff['R_loglog_linregress']*dataff['R_loglog_linregress'], "o", markersize=8, color='g')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('zone number', fontsize = axis_size-2)
    plt.ylabel('R2_loglog_linregress', fontsize = axis_size-2)
    plt.axis([0, xmaxaxis, 0, yplotmax])
    
    ax = plt.subplot(2,2,3)
    yplotmax = np.max(dataff['Std_m_over_n'])
    for zz in all_list:
        datatempzone = dataff[(dataff.zone == zz)]
        ymaxz = np.min(datatempzone['Std_m_over_n'])
        if zz in trust_list:
            plt.axvline(x=zz, ymin=0, ymax=ymaxz/yplotmax, color='r')
        else:
            plt.axvline(x=zz, ymin=0, ymax=ymaxz/yplotmax, color='k')
    plt.plot(dataff['zone'], dataff['Std_m_over_n'], "o", markersize=8, color='k')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('zone number', fontsize = axis_size-2)
    plt.ylabel('Std_m_over_n', fontsize = axis_size-2)
    plt.axis([0, xmaxaxis, 0, yplotmax])
    
    ax = plt.subplot(2,2,4)
    yplotmax = np.max(dataff['p_loglog_linregress'])
    for zz in all_list:
        datatempzone = dataff[(dataff.zone == zz)]
        ymaxz = np.min(datatempzone['p_loglog_linregress'])
        if zz in trust_list:
            plt.axvline(x=zz, ymin=0, ymax=ymaxz/yplotmax, color='r')
        else:
            plt.axvline(x=zz, ymin=0, ymax=ymaxz/yplotmax, color='c')
    plt.axhline(y=0.1,xmin=0,xmax=180,color='y')
    plt.plot(dataff['zone'], dataff['p_loglog_linregress'], "o", markersize=8, color='c')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('zone number', fontsize = axis_size-2)
    plt.ylabel('p_loglog_linregress', fontsize = axis_size-2)
    plt.axis([0, xmaxaxis, 0, yplotmax])    
    
    plt.suptitle('Zones for which p<= 0.1 (trustworthy): '+str(trust_list),fontsize = label_size)
    
    if safi == 1:
        plt.savefig('t:\\Topo_Data\\post-traitement\\fig_trustworthy-selection.png') 


    # m/n, n and K for zone numbers, with error
    #===============================================  
    datapp = dataff[(dataff.p_loglog_linregress > 0.1)] 
    datapp = datapp.reset_index(drop=True)        
    
    plt.figure(2, facecolor='white',figsize=(10,8))  
    ax = plt.subplot(1,1,1)

    plt.plot(datapp['zone'], datapp['m_over_n'], "o", markersize=8, color='b')
    ax.errorbar(datapp['zone'], datapp['m_over_n'], yerr=datapp['Std_m_over_n'],fmt='x')
    plt.plot(datap['zone'], datap['m_over_n'], "o", markersize=8, color='r')
    ax.errorbar(datap['zone'], datap['m_over_n'], yerr=datap['Std_m_over_n'], ecolor='r',fmt=' ')
    ax.spines['top'].set_linewidth(2.5)
    ax.spines['left'].set_linewidth(2.5)
    ax.spines['right'].set_linewidth(2.5)
    ax.spines['bottom'].set_linewidth(2.5) 
    ax.tick_params(axis='both', width=2.5)    
    plt.xlabel('zone number', fontsize = axis_size-2)
    plt.ylabel('m/n', fontsize = axis_size-2)
    plt.axis([0, xmaxaxis, 0, np.max(dataff['m_over_n'])+0.2])
    plt.axhline(y=np.mean(all_movern),xmin=0,xmax=65,color='r')
    plt.axhline(y=np.mean(p_movern),xmin=0,xmax=65,color='b')
    plt.title('m/n values and error for each zone (trustworthy in red)',fontsize = label_size)

    if safi == 1:
       plt.savefig('t:\\Topo_Data\\post-traitement\\fig_trustworthy-display.png') 


    # GENERAL STATISTICS ON M/N, N and K
    #**********************************************************************************************************

    # FOR TRUSTWORHTY :    
    if datach == 1:
        databox = datap.copy() 
    else:
        databox = dataff.copy()
            
    data_r1 = databox[(databox.rock == 1)] 
    data_r2 = databox[(databox.rock == 2)] 
    data_r3 = databox[(databox.rock == 3)] 
    data_r4 = databox[(databox.rock == 4)] 

    data_c1 = databox[(databox.clim == 1)] 
    data_c2 = databox[(databox.clim == 2)] 
    data_c3 = databox[(databox.clim == 3)] 
    data_c4 = databox[(databox.clim == 4)]  
    data_c5 = databox[(databox.clim == 5)] 
    
    data_s0 = databox[(databox.activity == 0)] 
    data_s1 = databox[(databox.activity == 1)] 
    
    #labels_rocks = ['Igneous', 'Sedimentary','Metamorphic', 'Mixed']
    #labels_clim = ['ARID', 'TROP.', 'TEMP.', 'COLD', 'POLAR']
    #labels_seismicity = ['Inactive','Active']

    # Stats on subgroups (number of zones and points) :
    #--------------------------------------------------
    
    # Define function--------
    def nb_pts_zones(datasub):   
        datasub = datasub.reset_index(drop=True)   
        lengzon = len(datasub)
        zone_list = []
        for zoo in range(1,lengzon-1):
            if datasub.zone[zoo]-datasub.zone[zoo+1] != 0:
               zone_list.append(int(datasub.zone[zoo]))   
        zone_list.append(int(datasub.zone[lengzon-1]))  
        return len(zone_list), lengzon
              
    # Apply function to rocks, climates and seismic activity ------------
    nb_glo = nb_pts_zones(databox.copy()) 
    
    nb_r1 = nb_pts_zones(data_r1.copy())   # resu = [nb_zones, nb_pts]
    nb_r2 = nb_pts_zones(data_r2.copy())
    nb_r3 = nb_pts_zones(data_r3.copy())
    nb_r4 = nb_pts_zones(data_r4.copy())

    nb_c1 = nb_pts_zones(data_c1.copy())
    nb_c2 = nb_pts_zones(data_c2.copy())    
    nb_c3 = nb_pts_zones(data_c3.copy())
    nb_c4 = nb_pts_zones(data_c4.copy())
    nb_c5 = nb_pts_zones(data_c5.copy())
    
    nb_s0 = nb_pts_zones(data_s0.copy())
    nb_s1 = nb_pts_zones(data_s1.copy())

    
        # Boxplots for M/N, N and K
        #============================
    if 1==1:
        
        fig = plt.figure(3, facecolor='white',figsize=(35,30))
        subpl = 0
        
        for parrow in [1,2,3]:   # ROWS
            if parrow == 1:
                if datach ==2:
                    param = 'erate'
                    paramsh = 'Erosion rate'
                    rowst = 0
                    print 'Tracing boxplots for erosion ...'
                else:
                    param = 'm_over_n'
                    paramsh = 'm/n'
                    rowst = 0
                    print 'Tracing boxplots for m/n ...'
            elif parrow==2:
                param = 'n'
                paramsh = param
                rowst = 2
                print 'Tracing boxplots for n ...'
            elif parrow==3:
                param = 'K'
                if log10K==1:
                    paramsh = 'Log10 K'
                else:
                    paramsh = param
                rowst = 4
                print 'Tracing boxplots for K ...'
                
            for parcol in [0,1,2,3]:  # COLUMNS
                subpl = subpl+1
                if parcol ==0 : # ALL DATA
                    n_cat = 1
                    if (parrow==3 and log10K ==1):
                        datamod = np.log10(databox[param])
                    else:
                        datamod = databox[param]
                    mean_datamod = np.mean(datamod)                    
                    ax = plt.subplot2grid((6,12),(rowst,0),rowspan=2, colspan=1)
                    lab = '\n GLOBAL \n Zones = '+str(nb_glo[0])+'\n Pts = '+str(nb_glo[1])
                    if parrow==1:
                        plt.title(' Global', fontsize = axis_size)
                if parcol ==1 :  # ROCKS
                    n_cat = 4
                    if (parrow==3 and log10K ==1):
                        datamod= [np.log10(data_r1[param]), np.log10(data_r2[param]), np.log10(data_r3[param]), np.log10(data_r4[param])]
                        mean_datamod = [np.mean(np.log10(data_r1[param])), np.mean(np.log10(data_r2[param])), np.mean(np.log10(data_r3[param])), np.mean(np.log10(data_r4[param]))]
                    else:
                        datamod= [data_r1[param] , data_r2[param], data_r3[param], data_r4[param]]
                        mean_datamod = [np.mean(data_r1[param]) , np.mean(data_r2[param]), np.mean(data_r3[param]), np.mean(data_r4[param])]
                    ax = plt.subplot2grid((6,12), (rowst,1), rowspan=2 ,colspan=4)   
                    lab = ['\n IGNE. \n'+str(nb_r1[0])+'\n'+str(nb_r1[1]), '\n SEDIM.\n'+str(nb_r2[0])+'\n'+str(nb_r2[1]),'\nMETA. \n'+str(nb_r3[0])+'\n'+str(nb_r3[1]), '\nMIX.\n'+str(nb_r4[0])+'\n'+str(nb_r4[1])]
                    if parrow==1:
                        plt.title('Rock Type', fontsize = axis_size)
                elif parcol==2:   # CLIMATE
                    n_cat = 5
                    if (parrow==3 and log10K ==1):
                        datamod= [np.log10(data_c1[param]), np.log10(data_c2[param]), np.log10(data_c3[param]), np.log10(data_c4[param]), np.log10(data_c5[param])]
                        mean_datamod = [np.mean(np.log10(data_c1[param])), np.mean(np.log10(data_c2[param])), np.mean(np.log10(data_c3[param])), np.mean(np.log10(data_c4[param])), np.mean(np.log10(data_c5[param]))]                      
                    else:
                        datamod= [data_c1[param] , data_c2[param], data_c3[param], data_c4[param], data_c5[param]]
                        mean_datamod = [np.mean(data_c1[param]) , np.mean(data_c2[param]), np.mean(data_c3[param]), np.mean(data_c4[param]), np.mean(data_c5[param])]                      
                    ax = plt.subplot2grid((6,12), (rowst,5), rowspan=2, colspan=5)            
                    lab = ['\n ARID \n'+str(nb_c1[0])+'\n'+str(nb_c1[1]), '\n TROP. \n'+str(nb_c2[0])+'\n'+str(nb_c2[1]), '\n TEMP.\n'+str(nb_c3[0])+'\n'+str(nb_c3[1]), '\n COLD \n'+str(nb_c4[0])+'\n'+str(nb_c4[1]), '\n POLAR\n'+str(nb_c5[0])+'\n'+str(nb_c5[1])]
                    if parrow==1:
                        plt.title('Climate Zone', fontsize = axis_size)
                elif parcol==3:   # SEISMICITY
                    n_cat = 2
                    if (parrow==3 and log10K ==1):
                        datamod= [np.log10(data_s0[param]), np.log10(data_s1[param])]
                        mean_datamod = [np.mean(np.log10(data_s0[param])), np.mean(np.log10(data_s1[param]))]
                    else:
                        datamod= [data_s0[param] , data_s1[param]]
                        mean_datamod = [np.mean(data_s0[param]) , np.mean(data_s1[param])]
                    ax = plt.subplot2grid((6,12), (rowst,10), rowspan=2, colspan=2)            
                    lab = ['\n INACT.\n'+str(nb_s0[0])+'\n'+str(nb_s0[1]),'\n ACT.\n'+str(nb_s1[0])+'\n'+str(nb_s1[1])]
                    if parrow==1:
                        plt.title('Tectonics', fontsize = axis_size)

                if (parrow==3 and log10K ==1):
                    plt.axhline(y=np.mean(np.log10(databox[param])),xmin=0,xmax=n_cat,color=(1, 0, 0, 0.5),lw=4)  # Add a mean param lines
                else:
                    plt.axhline(y=np.mean(databox[param]),xmin=0,xmax=n_cat,color=(1, 0, 0, 0.5),lw=4)  # Add a mean param lines
                pos = range(n_cat)          
                fig.subplots_adjust(wspace=0.8, hspace=0.2)
                ax.spines['left'].set_linewidth(2.5)
                ax.spines['bottom'].set_linewidth(2.5) 
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.yaxis.set_ticks_position('left')
                ax.xaxis.set_ticks_position('bottom')
                ax.tick_params(axis='both', width=2.5)  
                 
                if subpl in [1,5,9]:
                    plt.ylabel(paramsh, fontsize =axis_size+10)  # add y-labels
                else:
                    ax.set_yticklabels([])
                                    
                if parrow == 3:
                    plt.xticks(pos, lab,fontsize=axis_size) # add x-labels
                    if parcol ==0:
                        plt.figtext(0.105, 0.032, lab, fontsize=axis_size) # add x labels for global plot
                else:
                    ax.set_xticklabels([])

                # Create Violin Plot :
                w=0.5
                if parcol ==0:
                    k = gaussian_kde(datamod) #calculates the kernel density
                    m = k.dataset.min() #lower bound of violin
                    M = k.dataset.max() #upper bound of violin
                    x = arange(m,M,(M-m)/100.) # support for violin
                    v = k.evaluate(x) #violin profile (density curve)
                    v = v/v.max()*w #scaling the violin to the available space
                    ax.fill_betweenx(x,0,v,facecolor='lightgrey',alpha=0.3)
                    ax.fill_betweenx(x,0,-v,facecolor='lightgrey',alpha=0.3)
                    ax.boxplot(datamod,notch=1,positions=pos,vert=1,bootstrap=10000)
                else:
                    for d,p in zip(datamod,pos):
                        k = gaussian_kde(d) #calculates the kernel density
                        m = k.dataset.min() #lower bound of violin
                        M = k.dataset.max() #upper bound of violin
                        x = arange(m,M,(M-m)/100.) # support for violin
                        v = k.evaluate(x) #violin profile (density curve)
                        v = v/v.max()*w #scaling the violin to the available space
                        ax.fill_betweenx(x,p,v+p,facecolor='lightgrey',alpha=0.3)
                        ax.fill_betweenx(x,p,-v+p,facecolor='lightgrey',alpha=0.3)
                        ax.boxplot(datamod,notch=1,positions=pos,vert=1,bootstrap=10000)    
                plt.scatter(pos, mean_datamod, s=90, c='r')
                
                if parrow == 2:
                    plt.axhline(y=1,xmin=0,xmax=n_cat,color='Grey')  # Add a n=1 line
                    plt.figtext(0.095, 0.47, 'n=1',color = 'Grey', fontsize=axis_size-5) # add x labels for global plot
                    if datach == 0:
                        ax.set_ylim([-1,6])   # re-scale n axis

#                if parrow == 3:
#                    #if datach == 0:
#                     #   ax.set_ylim([-0.5e30,1e30])   # re-scale K axis
#                    #elif datach ==1:
#                      #  ax.set_ylim([-0.1,1])
#                    if datach ==2:
#                        ax.set_ylim([0,2.5e-6])
#                        
                               
        plt.suptitle(datatitle,fontsize = label_size+10)  
    
        if safi == 1:
            plt.savefig('t:\\Topo_Data\\post-traitement\\boxplots_mnK_'+fileref+'.png')  
            
            
            
            
            
    # GENERAL STATISTICS ON EROSION AND STEEPNESS INDEX
    #**********************************************************************************************************

  # Ajouter MAT, AREA and VEGETATION ?
    
        # Boxplots for EROSION and STEEPNESS
        #====================================
    if 1==1:
        
        fig = plt.figure(4, facecolor='white',figsize=(35,30))
        subpl = 0
        
        for parrow in [1,2,3]:   # ROWS
            if parrow == 1:
                param = 'erate'
                paramsh = 'Erosion rate (mm/kyr)'
                rowst = 0
                print 'Tracing boxplots for Erosion rate ...'
            elif parrow==2:
                param = 'Mean_chi_slope'
                paramsh = 'Steepness (chi-slope)'
                rowst = 2
                print 'Tracing boxplots for steepness ...'
            elif parrow==3:
                param = 'MAP'
                paramsh = param
                rowst = 4
                print 'Tracing boxplots for MAP ...'
                
            for parcol in [0,1,2,3]:  # COLUMNS
                subpl = subpl+1
                if parcol ==0 : # ALL DATA
                    n_cat = 1
                    datamod = dataff[param]
                    mean_datamod = np.mean(datamod)                    
                    ax = plt.subplot2grid((6,12),(rowst,0),rowspan=2, colspan=1)
                    lab = '\n GLOBAL \n Zones = '+str(nb_glo[0])+'\n Pts = '+str(nb_glo[1])
                    if parrow==1:
                        plt.title(' Global', fontsize = axis_size)
                if parcol ==1 :  # ROCKS
                    n_cat = 4
                    datamod= [data_r1[param] , data_r2[param], data_r3[param], data_r4[param]]
                    mean_datamod = [np.mean(data_r1[param]) , np.mean(data_r2[param]), np.mean(data_r3[param]), np.mean(data_r4[param])]
                    ax = plt.subplot2grid((6,12), (rowst,1), rowspan=2 ,colspan=4)   
                    lab = ['\n IGNE. \n'+str(nb_r1[0])+'\n'+str(nb_r1[1]), '\n SEDIM.\n'+str(nb_r2[0])+'\n'+str(nb_r2[1]),'\nMETA. \n'+str(nb_r3[0])+'\n'+str(nb_r3[1]), '\nMIX.\n'+str(nb_r4[0])+'\n'+str(nb_r4[1])]
                    if parrow==1:
                        plt.title('Rock Type', fontsize = axis_size)
                elif parcol==2:   # CLIMATE
                    n_cat = 5
                    datamod= [data_c1[param] , data_c2[param], data_c3[param], data_c4[param], data_c5[param]]
                    mean_datamod = [np.mean(data_c1[param]) , np.mean(data_c2[param]), np.mean(data_c3[param]), np.mean(data_c4[param]), np.mean(data_c5[param])]                      
                    ax = plt.subplot2grid((6,12), (rowst,5), rowspan=2, colspan=5)            
                    lab = ['\n ARID \n'+str(nb_c1[0])+'\n'+str(nb_c1[1]), '\n TROP. \n'+str(nb_c2[0])+'\n'+str(nb_c2[1]), '\n TEMP.\n'+str(nb_c3[0])+'\n'+str(nb_c3[1]), '\n COLD \n'+str(nb_c4[0])+'\n'+str(nb_c4[1]), '\n POLAR\n'+str(nb_c5[0])+'\n'+str(nb_c5[1])]
                    if parrow==1:
                        plt.title('Climate Zone', fontsize = axis_size)
                elif parcol==3:   # SEISMICITY
                    n_cat = 2
                    datamod= [data_s0[param] , data_s1[param]]
                    mean_datamod = [np.mean(data_s0[param]) , np.mean(data_s1[param])]
                    ax = plt.subplot2grid((6,12), (rowst,10), rowspan=2, colspan=2)            
                    lab = ['\n INACT.\n'+str(nb_s0[0])+'\n'+str(nb_s0[1]),'\n ACT.\n'+str(nb_s1[0])+'\n'+str(nb_s1[1])]
                    if parrow==1:
                        plt.title('Tectonics', fontsize = axis_size)

                plt.axhline(y=np.mean(dataff[param]),xmin=0,xmax=n_cat,color=(1, 0, 0, 0.5),lw=4)  # Add a mean param lines
                pos = range(n_cat)          
                fig.subplots_adjust(wspace=0.8, hspace=0.2)
                ax.spines['left'].set_linewidth(2.5)
                ax.spines['bottom'].set_linewidth(2.5) 
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.yaxis.set_ticks_position('left')
                ax.xaxis.set_ticks_position('bottom')
                ax.tick_params(axis='both', width=2.5)  
                 
                if subpl in [1,5,9]:
                    plt.ylabel(paramsh, fontsize =axis_size+20)  # add y-labels
                else:
                    ax.set_yticklabels([])
                                    
                if parrow == 3:
                    plt.xticks(pos, lab,fontsize=axis_size) # add x-labels
                    if parcol ==0:
                        plt.figtext(0.105, 0.032, lab, fontsize=axis_size) # add x labels for global plot
                else:
                    ax.set_xticklabels([])       
                    
                # Create Violin Plot :
                w=0.5
                if parcol ==0:
                    k = gaussian_kde(datamod) #calculates the kernel density
                    m = k.dataset.min() #lower bound of violin
                    M = k.dataset.max() #upper bound of violin
                    x = arange(m,M,(M-m)/100.) # support for violin
                    v = k.evaluate(x) #violin profile (density curve)
                    v = v/v.max()*w #scaling the violin to the available space
                    ax.fill_betweenx(x,0,v,facecolor='lightgrey',alpha=0.3)
                    ax.fill_betweenx(x,0,-v,facecolor='lightgrey',alpha=0.3)
                    ax.boxplot(datamod,notch=1,positions=pos,vert=1,bootstrap=10000)
                else:
                    for d,p in zip(datamod,pos):
                        k = gaussian_kde(d) #calculates the kernel density
                        m = k.dataset.min() #lower bound of violin
                        M = k.dataset.max() #upper bound of violin
                        x = arange(m,M,(M-m)/100.) # support for violin
                        v = k.evaluate(x) #violin profile (density curve)
                        v = v/v.max()*w #scaling the violin to the available space
                        ax.fill_betweenx(x,p,v+p,facecolor='lightgrey',alpha=0.3)
                        ax.fill_betweenx(x,p,-v+p,facecolor='lightgrey',alpha=0.3)
                        ax.boxplot(datamod,notch=1,positions=pos,vert=1,bootstrap=10000)    
                plt.scatter(pos, mean_datamod, s=90, c='r')
                       
                if parrow == 1:
                    ax.set_ylim([0,2000])   # re-scale erosion axis                              
                elif parrow == 2:
                    if datach == 2 :
                        ax.set_ylim([0,20])    # re-scale steepness axis                        
                    else:
                        ax.set_ylim([0,80])    # re-scale steepness axis
            
        plt.suptitle(datatitle,fontsize = label_size+10)  
    
        if safi == 1:
            plt.savefig('t:\\Topo_Data\\post-traitement\\boxplots_erosion_'+fileref+'.png')  
            
            
    # GENERAL STATISTICS ON MAT, AREA and VEGETATION
    #**********************************************************************************************************
    
        # Boxplots for MAT, AREA and vegetation
        #====================================
    if 1==1:
        
        fig = plt.figure(5, facecolor='white',figsize=(35,30))
        subpl = 0
        
        for parrow in [1,2,3]:   # ROWS
            if parrow == 1:
                param = 'MAT'
                paramsh = 'MAT'
                rowst = 0
                print 'Tracing boxplots for MAT ...'
            elif parrow==2:
                param = 'area'
                paramsh = 'Area (m2)'
                rowst = 2
                print 'Tracing boxplots for area ...'
            elif parrow==3:
                param = 'vegetation'
                paramsh = param
                rowst = 4
                print 'Tracing boxplots for vegetation ...'
                
            for parcol in [0,1,2,3]:  # COLUMNS
                subpl = subpl+1
                if parcol ==0 : # ALL DATA
                    n_cat = 1
                    datamod = dataff[param]
                    mean_datamod = np.mean(datamod)                    
                    ax = plt.subplot2grid((6,12),(rowst,0),rowspan=2, colspan=1)
                    lab = '\n GLOBAL \n Zones = '+str(nb_glo[0])+'\n Pts = '+str(nb_glo[1])
                    if parrow==1:
                        plt.title(' Global', fontsize = axis_size)
                if parcol ==1 :  # ROCKS
                    n_cat = 4
                    datamod= [data_r1[param] , data_r2[param], data_r3[param], data_r4[param]]
                    mean_datamod = [np.mean(data_r1[param]) , np.mean(data_r2[param]), np.mean(data_r3[param]), np.mean(data_r4[param])]
                    ax = plt.subplot2grid((6,12), (rowst,1), rowspan=2 ,colspan=4)   
                    lab = ['\n IGNE. \n'+str(nb_r1[0])+'\n'+str(nb_r1[1]), '\n SEDIM.\n'+str(nb_r2[0])+'\n'+str(nb_r2[1]),'\nMETA. \n'+str(nb_r3[0])+'\n'+str(nb_r3[1]), '\nMIX.\n'+str(nb_r4[0])+'\n'+str(nb_r4[1])]
                    if parrow==1:
                        plt.title('Rock Type', fontsize = axis_size)
                elif parcol==2:   # CLIMATE
                    n_cat = 5
                    datamod= [data_c1[param] , data_c2[param], data_c3[param], data_c4[param], data_c5[param]]
                    mean_datamod = [np.mean(data_c1[param]) , np.mean(data_c2[param]), np.mean(data_c3[param]), np.mean(data_c4[param]), np.mean(data_c5[param])]                      
                    ax = plt.subplot2grid((6,12), (rowst,5), rowspan=2, colspan=5)            
                    lab = ['\n ARID \n'+str(nb_c1[0])+'\n'+str(nb_c1[1]), '\n TROP. \n'+str(nb_c2[0])+'\n'+str(nb_c2[1]), '\n TEMP.\n'+str(nb_c3[0])+'\n'+str(nb_c3[1]), '\n COLD \n'+str(nb_c4[0])+'\n'+str(nb_c4[1]), '\n POLAR\n'+str(nb_c5[0])+'\n'+str(nb_c5[1])]
                    if parrow==1:
                        plt.title('Climate Zone', fontsize = axis_size)
                elif parcol==3:   # SEISMICITY
                    n_cat = 2
                    datamod= [data_s0[param] , data_s1[param]]
                    mean_datamod = [np.mean(data_s0[param]) , np.mean(data_s1[param])]
                    ax = plt.subplot2grid((6,12), (rowst,10), rowspan=2, colspan=2)            
                    lab = ['\n INACT.\n'+str(nb_s0[0])+'\n'+str(nb_s0[1]),'\n ACT.\n'+str(nb_s1[0])+'\n'+str(nb_s1[1])]
                    if parrow==1:
                        plt.title('Tectonics', fontsize = axis_size)

                plt.axhline(y=np.mean(dataff[param]),xmin=0,xmax=n_cat,color=(1, 0, 0, 0.5),lw=4)  # Add a mean param lines
                pos = range(n_cat)          
                fig.subplots_adjust(wspace=0.8, hspace=0.2)
                ax.spines['left'].set_linewidth(2.5)
                ax.spines['bottom'].set_linewidth(2.5) 
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.yaxis.set_ticks_position('left')
                ax.xaxis.set_ticks_position('bottom')
                ax.tick_params(axis='both', width=2.5)  
                 
                if subpl in [1,5,9]:
                    plt.ylabel(paramsh, fontsize =axis_size+20)  # add y-labels
                else:
                    ax.set_yticklabels([])
                                    
                if parrow == 3:
                    plt.xticks(pos, lab,fontsize=axis_size) # add x-labels
                    if parcol ==0:
                        plt.figtext(0.105, 0.032, lab, fontsize=axis_size) # add x labels for global plot
                else:
                    ax.set_xticklabels([])           
                    
                # Create Violin Plot :
                w=0.5
                if parcol ==0:
                    k = gaussian_kde(datamod) #calculates the kernel density
                    m = k.dataset.min() #lower bound of violin
                    M = k.dataset.max() #upper bound of violin
                    x = arange(m,M,(M-m)/100.) # support for violin
                    v = k.evaluate(x) #violin profile (density curve)
                    v = v/v.max()*w #scaling the violin to the available space
                    ax.fill_betweenx(x,0,v,facecolor='lightgrey',alpha=0.3)
                    ax.fill_betweenx(x,0,-v,facecolor='lightgrey',alpha=0.3)
                    ax.boxplot(datamod,notch=1,positions=pos,vert=1,bootstrap=10000)
                else:
                    for d,p in zip(datamod,pos):
                        k = gaussian_kde(d) #calculates the kernel density
                        m = k.dataset.min() #lower bound of violin
                        M = k.dataset.max() #upper bound of violin
                        x = arange(m,M,(M-m)/100.) # support for violin
                        v = k.evaluate(x) #violin profile (density curve)
                        v = v/v.max()*w #scaling the violin to the available space
                        ax.fill_betweenx(x,p,v+p,facecolor='lightgrey',alpha=0.3)
                        ax.fill_betweenx(x,p,-v+p,facecolor='lightgrey',alpha=0.3)
                        ax.boxplot(datamod,notch=1,positions=pos,vert=1,bootstrap=10000)    
                plt.scatter(pos, mean_datamod, s=90, c='r')
                       
                if parrow == 2:
                    ax.set_ylim([0,3e9])    # re-scale area axis

        plt.suptitle(datatitle,fontsize = label_size+10)  
    
        if safi == 1:
            plt.savefig('t:\\Topo_Data\\post-traitement\\boxplots_param_'+fileref+'.png')  
                        
            
            
            
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    print 'Done.'
    plt.show()
      

if __name__ == "__main__":
    make_plots()