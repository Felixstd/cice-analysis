import re
import numpy as np
import xarray as xr 
import matplotlib.pyplot as plt

from ciceplotting.data import readdata
from ciceplotting.utils import arguments 


plt.style.use('/home/fsd001/cice-analysis/ciceplotting/ciceplotting/plotting/science.mplstyle')
datadir = '/home/fsd001/data/ppp5/cice/runs/implicitCrheoIdeal/history/'
dir = '/home/fsd001/data/ppp5/cice/runs/implicitCrheoIdealdebug/'
figdir = '/home/fsd001/cice-analysis/Figures/Numerics/'

def main():

    args = arguments.parse_args()
    exp = args.exp

    fileE = dir+'residualE_'+exp
    fileN = dir+'residualN_'+exp

    cicelog = dir+'cice.runlog.'+exp


    nonlin_value, progress_value, fgmres_value = readdata.read_cicelog(cicelog, True, True)


    dataE = np.loadtxt(fileE)
    dataN = np.loadtxt(fileN)

    res_E = np.reshape(dataE, (52,52))
    res_N = np.reshape(dataN, (52, 52))

    res_E = res_E[1:51, 1:51]
    res_N = res_N[1:51, 1:51]


    #---------------------------------------------------
    # FIGURES 
    #---------------------------------------------------


    #----- Figure 1 ------#
    #----- Showing the residual spatially and norms -----#
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, 
                                                constrained_layout = True, 
                                                figsize = (10, 6))
    ax1.pcolor(res_E, 
            vmin = -1e-10, 
            vmax = 1e-10)
    ax1.set_title('fpresxE')

    pc = ax2.pcolor(res_N, 
                    vmin = -1e-10, 
                    vmax = 1e-10)
    fig.colorbar(pc, 
                ax = [ax1, ax2], 
                pad = 0.01)
    ax2.set_title('fpresyN')

    ax3.plot(nonlin_value)
    ax3.set_yscale('log')
    ax3.set_title('Nonlin_res_L2norm')

    ax4.plot(progress_value)
    ax4.set_yscale('log')
    ax4.set_title('progress_res_L2norm')
    plt.savefig(figdir+'res.png')

    #------- Figure 2 -------#
    #This shows the L2norm for fgmres and nonlin

    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout = True, figsize = (10, 5))
    ax1.plot(fgmres_value)
    ax1.set_xlabel('its FGMRES')

    ax1.set_yscale('log')

    ax2.plot(nonlin_value)
    ax2.set_xlabel('nonlin its')

    ax2.set_yscale('log')
    fig.supylabel('L2norm')
    plt.savefig(figdir+'conv.png')

if __name__ == '__main__':
    main()