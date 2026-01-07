import numpy as np
import xarray as xr 
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.cm as pltcm

from ciceplotting.utils.TimeUtilities import TimeUtility
from ciceplotting.data.readnamelist import namelist
from ciceplotting.data import readdata



import configparser
import cmocean as cm
import warnings
import os


plt.style.use('/home/fsd001/analysis/ciceplotting/ciceplotting/utils/science.mplstyle')


config_exp = configparser.ConfigParser()
config_exp.read('./namelist')


Parameters = namelist(configuration_exp  = config_exp['Experiment'], 
                      configuration_dyn  = config_exp['Dynamics'], 
                      configuration_num  = config_exp['Numerical'],
                      configuration_fig  = config_exp['Figures'], 
                      configuration_time = config_exp['Time'])


uvels_experiment = []

for exp in Parameters.exp:

    print('Reading Experiment: ', exp)

    # if not os.path.isdir(Parameters.figdir+str(exp)):
    #     os.mkdir(Parameters.figdir+str(exp))

    if Parameters.read_all:
        dataset_exp = readdata.readdata(exp, 
                                     Parameters.datestr, 
                                     Parameters.var, 
                                     Parameters.datadir)
        
        uvel = dataset_exp['uvel']
        uvels_experiment.append(uvel)



x = np.arange(300, 400)*Parameters.dx
plt.figure()
for i, uvel in enumerate(uvels_experiment):
    plt.plot(x, uvel[0, 200, 300:], label = Parameters.exp[i])
plt.legend()
plt.xlabel(r'$x$ (km)')
plt.ylabel(r'$u_{ice}$ (m/s)')
plt.savefig(Parameters.figdir+'/uvel_bgrid'+'.png')