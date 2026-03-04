
"""
CICE-Analysis

This package is used to analyse the outputs of the CICE sea ice model. 
The different functions are located in ciceplotting. It contains
three repositories:

- data: everything that as to do with reading data and namelist. 
- plotting: functions to plot and create figures.
- utils: utilities such as time management. 

Felix St-Denis (09/01/2026)

"""

import numpy as np
import xarray as xr 
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.cm as pltcm

from ciceplotting.utils.TimeUtilities import TimeUtility
from ciceplotting.data.readnamelist import namelist
from ciceplotting.data import readdata
from ciceplotting.plotting import plot_cice
from collections import defaultdict


import configparser
import cmocean as cmo
import warnings
import os


#configuration of  the style of figures
plt.style.use('/home/fsd001/cice-analysis/ciceplotting/ciceplotting/plotting/science.mplstyle')


config_exp = configparser.ConfigParser(interpolation=None)
config_exp.read('./namelist')

#reading namelist
Parameters = namelist(configuration_exp  = config_exp['Experiment'], 
                      configuration_dyn  = config_exp['Dynamics'], 
                      configuration_num  = config_exp['Numerical'],
                      configuration_fig  = config_exp['Figures'], 
                      configuration_time = config_exp['Time'])

Dates_Config = TimeUtility(configuration_time = config_exp['Time'])
dates_list = TimeUtility.setup_time(Dates_Config)

print(dates_list)
uvels_experiments = []
h_experiments = []

data_experiments = defaultdict(dict)

if not os.path.isdir(Parameters.figdir+Parameters.case):
    os.mkdir(Parameters.figdir+Parameters.case)

#going through all experiments
for exp in Parameters.exp:

    print('Experiment: ', exp)

    if not os.path.isdir(Parameters.figdir+'Experiments/'+str(exp)):
        os.mkdir(Parameters.figdir+'Experiments/'+str(exp))

    #reading data 
    if Parameters.read_all:
        print('Reading Data')

        max_speed_arctic, max_speed_antarctic = readdata.read_cicelog_dynamics(Parameters.datadir+'/cice.runlog.'+Parameters.case)


        for datestr in dates_list:
            print('Reading Date: ', datestr)
            dataset_exp = readdata.readdata(exp, 
                                        datestr, 
                                        Parameters.var, 
                                        Parameters.datadir)
            
            data_experiments[exp][datestr] = dataset_exp


print('Plotting Figures')

if Parameters.Global:

    datestr = '2005-11'

    # plot_cice.plot_global(data_experiments, 
    #                     'Cgrid', 
    #                     datestr, 
    #                     'vvel', 
    #                     Parameters,
    #                     r'$v_{ice}$ (m/s)', 
    #                     'C-grid',
    #                     'vvel_cgrid'+'_'+datestr)
    
    plot_cice.plot_global(data_experiments, 
                        Parameters.exp[0], 
                        datestr, 
                        'vvel', 
                        Parameters,
                        r'$v_{ice}$ (m/s)', 
                        'Thermo IMEX',
                        Parameters.exp[0]+'_vvel'+'_'+datestr)
    

    plot_cice.plot_maxspeed(max_speed_arctic, max_speed_antarctic, 
                            Parameters.figdir+Parameters.case+"/", Parameters.exp[0]+'max_speed.png')

if Parameters.imex:

    plot_cice.plot_1d(data_experiments, 
                    exp, 
                    datestr,
                    Parameters, 
                    'hi',
                    r'$x$ (km)',
                    r'$h$ (m)', 
                    'Rothrock',
                    'h_imex.png', 
                    IMEX = True)

    #making a figure with multiple experiments
    print('Plotting Figures')
    x = np.arange(300, 400)*Parameters.dx

    labels = ['Default', 'IMEXSerial', 'IMEXParallel']
    #thickness
    print('Plotting Thicknesses')
    plt.figure()
    for i, h in enumerate(h_experiments):
        plt.plot(x, h[0, 200, 300:], label = Parameters.exp[i])
    plt.legend()
    plt.xlabel(r'$x$ (km)')
    plt.ylabel(r'$h$ (m)')
    plt.savefig(Parameters.figdir+'/'+Parameters.case+'/h_IMEX'+'.png')




    print('Plotting Velocities')
    # velocity
    plt.figure()
    for i, uvel in enumerate(uvels_experiments):
        plt.plot(x, uvel[0, 200, 300:], label = Parameters.exp[i])
    plt.legend()
    plt.xlabel(r'$x$ (km)')
    plt.ylabel(r'$u_{ice}$ (m/s)')
    plt.savefig(Parameters.figdir+'/'+Parameters.case+'/uvel_IMEX'+'.png')


    h_diff = h_experiments[0] - h_experiments[1]

    plt.figure()
    plt.plot(x, h_diff[0, 200, 300:])
    plt.legend()
    plt.xlabel(r'$x$ (km)')
    plt.ylabel(r'$\Delta h$ (m)')
    plt.savefig(Parameters.figdir+'/'+Parameters.case+'/diffh_IMEX'+'.png')
