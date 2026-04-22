
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
import matplotlib.ticker as ticker

from ciceplotting.utils.TimeUtilities import TimeUtility
from ciceplotting.data.readnamelist import namelist
from ciceplotting.data import readdata
from ciceplotting.plotting import plot_cice
from collections import defaultdict
from argparse import ArgumentParser


import configparser
import cmocean as cmo
import warnings
import os


#configuration of  the style of figures
plt.style.use('/home/fsd001/cice-analysis/ciceplotting/ciceplotting/plotting/science.mplstyle')

parser = ArgumentParser(prog='CICE-Analysis',
                    description='Program used to analyse CICE outputs')
parser.add_argument('-c', "--case", dest = 'case', 
                            help = 'case name for fig dir')
args = parser.parse_args()
case_arg = args.case

config_exp = configparser.ConfigParser(interpolation=None)

if case_arg == 'gx':
    config_exp.read('./namelist')

elif case_arg == 'ideal':
    config_exp.read('./namelist_ideal')


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
for i, exp in enumerate(Parameters.exp):

    print('Experiment: ', exp)

    precond = Parameters.preconds[i]

    #reading data 
    if Parameters.read_all:
        print('Reading Data')

        if Parameters.Global:

            results = readdata.read_cicelog_dynamics(Parameters.datadir+'/cice.runlog.'+exp)
            data_experiments[exp] = results
            
            (nonlin_value, progress_value, solver_value, its_solver, its_precond, 
             precond_value, breakdowns_it, solver_cycles, solver_its_cycles, nonlin_cycles, solver_pernonlin) = \
                readdata.read_cicelog(Parameters.datadir+'/cice.runlog.'+exp, 'fgmres', precond, 1, 1, 0)
            

        for datestr in dates_list:
            print('Reading Date: ', datestr)
            dataset_exp = readdata.readdata(exp, 
                                        datestr, 
                                        Parameters.var, 
                                        Parameters.datadir+'/'+exp+'/')    
            
            data_experiments[exp][datestr] = dataset_exp

            if Parameters.Global:
                data_experiments[exp][datestr]['picardnorm'] = nonlin_value
                data_experiments[exp][datestr]['solvernorm'] = solver_value
                data_experiments[exp][datestr]['precondnorm'] = precond_value
                data_experiments[exp][datestr]['solvercycles'] = (
                                                                    ('fgmres_cycle', 'solver_iter'),   # explicit dim names
                                                                    solver_cycles
                                                                )
                data_experiments[exp][datestr]['solverItsperCycles'] = solver_its_cycles
                data_experiments[exp][datestr]['non_cycles'] = (
                                                                    ('timestep', 'PicardIter'),   # explicit dim names
                                                                    nonlin_cycles
                                                                )
                data_experiments[exp][datestr]['solveritspernonlin'] = solver_pernonlin

print('Plotting Figures')

if Parameters.Global:

    date = '2006-01'
    var = 'hi'

    for exp in Parameters.exp:
            print(date, exp)
            plot_cice.plot_global(data_experiments, 
                        exp, 
                        date, 
                        var, 
                        Parameters,
                        r'Ice Thickness (m)', 
                        r'$\Delta t$ = 4hr',
                        exp+'_'+var+'_'+date)

    plot_cice.plot_timeseries(data_experiments, Parameters,
                              Parameters.figdir+Parameters.case+"/", 
                              str(Parameters.dt))
    
    plot_cice.plot_timeseries_pres(data_experiments, Parameters,
                              Parameters.figdir+Parameters.case+"/", 
                              str(Parameters.dt))
    
    # plot_cice.plot_solver(Parameters, Parameters.exp, 
    #                       data_experiments,
    #                       datestr, 
    #                       Parameters.figdir+Parameters.case+"/")

    plot_cice.plot_difference_global(Parameters, data_experiments, 
                                     date, 'hi',
                                     Parameters.figdir)


if Parameters.imex:

    # if Parameters.case == 'IMEX_ideal':
    plot_cice.plot_1d(data_experiments, 
                        Parameters.exp, 
                        Parameters.startdate,
                        Parameters, 
                        'uvel',
                        '',
                        r'$x$ (km)',
                        r'$u$ (m/s)', 
                        island = True)
    
    plot_cice.plot_1d_presentation(data_experiments, 
                        Parameters.exp, 
                        Parameters.startdate,
                        Parameters, 
                        'hi',
                        '',
                        r'$x$ (km)',
                        'Thickness\n(m)', 
                        island = True)
    
    if (Parameters.case == 'IMEX_lshape' or Parameters.case == 'INSTAhpcLISLAND'):
        for exp in Parameters.exp:
            if 'IMEX' in exp:
                plot_cice.plot_rect(data_experiments , exp, 
                                    Parameters.startdate   , Parameters,
                                    'hi' ,
                                    IMEX = True)
            else:
                plot_cice.plot_rect(data_experiments , exp, 
                                    Parameters.startdate, Parameters,
                                    'hi' ,
                                    IMEX = False)
            
    #making a figure with multiple experiments
    # print('Plotting Figures')
    # x = np.arange(300, 400)*Parameters.dx

    # labels = ['Default', 'IMEXSerial', 'IMEXParallel']
    # #thickness
    # print('Plotting Thicknesses')
    # plt.figure()
    # for i, h in enumerate(h_experiments):
    #     plt.plot(x, h[0, 200, 300:], label = Parameters.exp[i])
    # plt.legend()
    # plt.xlabel(r'$x$ (km)')
    # plt.ylabel(r'$h$ (m)')
    # plt.savefig(Parameters.figdir+'/'+Parameters.case+'/h_IMEX'+'.png')




    # print('Plotting Velocities')
    # # velocity
    # plt.figure()
    # for i, uvel in enumerate(uvels_experiments):
    #     plt.plot(x, uvel[0, 200, 300:], label = Parameters.exp[i])
    # plt.legend()
    # plt.xlabel(r'$x$ (km)')
    # plt.ylabel(r'$u_{ice}$ (m/s)')
    # plt.savefig(Parameters.figdir+'/'+Parameters.case+'/uvel_IMEX'+'.png')


    # h_diff = h_experiments[0] - h_experiments[1]

    # plt.figure()
    # plt.plot(x, h_diff[0, 200, 300:])
    # plt.legend()
    # plt.xlabel(r'$x$ (km)')
    # plt.ylabel(r'$\Delta h$ (m)')
    # plt.savefig(Parameters.figdir+'/'+Parameters.case+'/diffh_IMEX'+'.png')

        # time_solvers = np.array([129.27,57.14,30.23,16.87])
    # plt.figure()
    # plt.bar(Parameters.exp, time_solvers)
    # plt.ylabel('Time (s)')
    # plt.xticks(rotation = 45)
    # plt.savefig(Parameters.figdir+Parameters.case+"/timeslver.png")

    
    # fig = plt.figure()
    # plt.plot(uvel_max[:10], label = 'u')
    # plt.plot(vvel_max[:10], label = 'v')
    # fig.legend(bbox_to_anchor=(1.2,0.9))
    # plt.grid()
    # plt.xlabel('Picard Iteration')
    # plt.ylabel('Velocity (m/s)')
    # # plt.title('Velocity at i = 2, j = 2')
    # plt.savefig(Parameters.figdir+Parameters.case+"/"+Parameters.exp[0]+"_maxvel.png")

    # fig = plt.figure()
    # plt.plot(uvel_fgmres, label = 'u')
    # plt.plot(vvel_fgmres, label = 'v')
    # fig.legend(bbox_to_anchor=(1.2,0.9))
    # plt.grid()
    # plt.xlabel('FGMRES Iteration')
    # plt.ylabel('Velocity (m/s)')
    # # plt.title('Velocity at i = 2, j = 2')
    # plt.savefig(Parameters.figdir+Parameters.case+"/"+Parameters.exp[0]+"_FMGRESmaxvel.png")

    # fig = plt.figure()
    # plt.plot(strintx, label = 'strintx')
    # plt.plot(strinty, label = 'strinty')
    # fig.legend(bbox_to_anchor = (1.2,0.9))
    # plt.xlabel('Picard Iteration')
    # plt.grid()
    # plt.ylabel(r'$div(\sigma)$ (Nm$^{-1}$s$^{-2}$)')
    # plt.title('Rheology at i = 2, j = 2')
    # plt.savefig(Parameters.figdir+Parameters.case+"/"+Parameters.exp[0]+"_rheology.png")

    # fig = plt.figure()
    # plt.plot(strocnx, label = 'strocnx', color = 'royalblue')
    # plt.plot(strocny, label = 'strocny', color = 'darkgreen')
    # plt.yscale('symlog', linthresh = 1e-10)
    # ticks = [-1e-2, -1e-4, -1e-6, -1e-8, 0, 1e-8, 1e-6, 1e-4]
    # plt.gca().set_yticks(ticks)
    # plt.grid()
    # # plt.gca().yaxis.set_major_locator(ticker.LogLocator(base=10, numticks=6))
    # # plt.gca().yaxis.set_major_formatter(ticker.LogFormatterSciNotation())
    # plt.axhline(strairx[0], color = 'royalblue', alpha = 0.5)
    # plt.axhline(strairy[0], color = 'darkgreen', alpha = 0.5)
    # fig.legend(bbox_to_anchor = (1.2,0.9))
    # plt.xlabel('Picard Iteration')
    # plt.ylabel(r'Ice-ocean Stress (Nm$^{-2}$)')
    # plt.title('Ocean at i = 2, j = 2')
    # plt.savefig(Parameters.figdir+Parameters.case+"/"+Parameters.exp[0]+"_oceanstress.png")
