import numpy as np

import matplotlib.pyplot as plt 
import cmocean as cmo
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.cm as pltcm
from matplotlib.lines import Line2D


import matplotlib.path as mpath
from matplotlib.gridspec import GridSpec
import cartopy.crs as ccrs
import cartopy.feature as cfeature

import re

colors_list1 = mpl.color_sequences['Dark2']

dt_to_color = {
                1:'k', 
                5:   colors_list1[1], 
                20:  colors_list1[2],
                40:  colors_list1[3],
                60:  colors_list1[4], 
                120: colors_list1[5],
                180: colors_list1[6]
                }

def extract_number(label):
    match = re.search(r'B(\d+)', label)
    return int(match.group(1)) if match else None


def plot_global(data_experiments,
                exp, 
                datestr, 
                var, 
                Parameters,
                var_label, 
                title,
                figname):

    ds = data_experiments[exp][datestr]
    ds = ds.where(ds.tmask == 1)

    var_plot = ds[var][:]

    ni, nj = np.shape(var_plot)[1:]
    data = np.zeros((ni, nj),dtype=np.float32)
    data[:,:] = var_plot[0]

    data[data > 100.0 ] = np.nan

    tlon = ds['TLON'][:, :].to_numpy()
    tlat = ds['TLAT'][:, :].to_numpy()


    # Convert lon/lat to regular numpy arrays (remove masks)
    tlon = np.asarray(tlon)
    tlat = np.asarray(tlat)

    # Replace non-finite values
    # maybe this is not the best way, but works for now 
    tlon[~np.isfinite(tlon)] = 1e10
    tlat[~np.isfinite(tlat)] = 1e10

    # make circular boundary for polar stereographic circular plots
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)

    # define the colormap
    if var == 'aice':
        cmap = cmo.cm.ice
        vmax = 1
        vmin = 0

    if var == 'hi':
        cmap = cmo.cm.dense 
        vmax = 5
        vmin = 0
    
    if ('uvel' in var or 'vvel' in var) : 
        cmap = cmo.cm.balance
        vmax = 0.8
        vmin = -0.8

    # set up the figure with a North Polar Stereographic projection
    fig = plt.figure(figsize=(12,20), constrained_layout = True)
    ax = fig.add_subplot(1,2,1, projection=ccrs.NorthPolarStereo())
    ax.set_boundary(circle, transform=ax.transAxes)
    # ax.set_extent([0, 360, 55, 90], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND,zorder=100,edgecolor='k')

    # sets the latitude / longitude boundaries of the plot
    ax.set_extent([0.005, 360, 90, 55], crs=ccrs.PlateCarree())

    #Plot the first timeslice of aice
    this=ax.pcolormesh(tlon,
                       tlat,
                       data,
                       cmap=cmap,
                       vmax=vmax,
                       vmin=vmin,
                       transform=ccrs.PlateCarree(), shading = 'auto')
    
    ax2 = fig.add_subplot(1,2,2, projection=ccrs.SouthPolarStereo())

    ax2.set_boundary(circle, transform=ax2.transAxes)
    # ax.set_extent([0, 360, 55, 90], crs=ccrs.PlateCarree())
    ax2.add_feature(cfeature.LAND,zorder=100,edgecolor='k')

    # sets the latitude / longitude boundaries of the plot
    ax2.set_extent([0.005, 360, -90, -55], ccrs.PlateCarree())

    #Plot the first timeslice of aice
    aice2=ax2.pcolormesh(tlon,
                       tlat,
                       data,
                       cmap=cmap,
                       vmax=vmax,
                       vmin=vmin,
                       transform=ccrs.PlateCarree(), shading = 'auto')
    
    cbar = fig.colorbar(aice2,
                 ax = [ax, ax2], 
                 shrink = 0.3,
                 orientation='vertical')
    cbar.set_label(label = var_label, size = 14)
    fig.suptitle(title, x = 0.45, y = 0.65, size = 14)

    plt.savefig(Parameters.figdir+'/'+Parameters.case+'/'+figname)
    # plt.savefig(figdir+figname)
    
def plot_maxspeed(experiments, data_experiments,
                  datestr, 
                  figdir    , figname):
    

    handles = [
        Line2D(
            [0], [0],
            label='Arctic',
            color='royalblue'
        ), 
        Line2D(
            [0], [0],
            label='Antarctic',
            color='darkred'
        )]
    
    fig, (ax1,ax2) = plt.subplots(1,2, figsize = (8,4))
    handles = []
    for i, exp in enumerate(experiments):
        max_arctic = data_experiments[exp][datestr]['max_arctic']
        max_antarctic = data_experiments[exp][datestr]['max_antarc']


        p1 = ax1.plot(max_arctic)

        ax2.plot(max_antarctic, label = 'Antarctic')

        if exp == 'N50F20P10':
            label = 'Zhang'

        elif exp == "N50F20P10LIN2":
            label = 'Tremblay'

        else:
            label = exp


        handles.append(Line2D(
            [0], [0],
            label=label,
            color=p1[0].get_color()
        ))

    # ax2.set_yscale('log')
    fig.legend(handles = handles, bbox_to_anchor = (1.1,0.9))
    fig.supxlabel('Picard Iteration')
    ax1.set_ylabel('Maximum Ice Speed (m/s)')
    ax1.set_title('Arctic')
    ax2.set_title('Antarctic')
    plt.savefig(figdir+'maxicespeed_exp.png')


def plot_solver(Parameters, experiments, 
                data_experiments,
                datestr, 
                figdir, 
                startdate = None, enddate = None):
    

    colors = ['royalblue', 'darkred', 'forestgreen', 'darkviolet', 'k']
    fig, ((ax1,ax2), (ax3,ax4)) = plt.subplots(2,2, figsize = (10,10))
    
    fig2, ax5 = plt.subplots(1, 1)
    fig3, ax6 = plt.subplots(1,1)

    fig4, ax7 = plt.subplots(1,1)

    fig5, ax8 = plt.subplots(1,1)
    
    handles = []
    for i, exp in enumerate(experiments):

        nonlin_norm = data_experiments[exp][datestr]['picardnorm']
        solver_norm = data_experiments[exp][datestr]['solvernorm']
        precond_norm = data_experiments[exp][datestr]['precondnorm']
        max_arctic = data_experiments[exp][datestr]['max_arctic']
        max_antarctic = data_experiments[exp][datestr]['max_antarc']
        solver_its_cycles = data_experiments[exp][datestr]['solverItsperCycles']
        nonlin_cycles     = data_experiments[exp][datestr]['non_cycles']
        solver_cycles     = data_experiments[exp][datestr]['solvercycles']


        print(np.shape(solver_cycles), np.shape(nonlin_cycles))
        p1 = ax1.plot(np.arange(len(nonlin_norm)), nonlin_norm, color = colors[i])

        ax2.plot(solver_norm, color=p1[0].get_color())
        ax3.plot(max_arctic, color=p1[0].get_color())
        ax3.plot(max_antarctic, color=p1[0].get_color(),linestyle = '--')
        ax4.plot(precond_norm, color=p1[0].get_color())

        ax5.plot(solver_its_cycles, color = colors[i])

        ax6.plot(nonlin_cycles[-1, :], color=colors[i])

        ax7.plot(solver_cycles[-4, :], color = colors[i], linestyle = '--')
        ax7.plot(solver_cycles[-3, :], color = colors[i])

        for ax in [ax3, ax8]:
            ax.plot(max_arctic, color=p1[0].get_color())
            ax.plot(max_antarctic, color=p1[0].get_color(),linestyle = '--')

        handles.append(Line2D(
            [0], [0],
            label=Parameters.labels[i],
            color=p1[0].get_color()
        ))

    axs_scale = [ax1, ax2, ax4, ax6, ax7]
    for ax in axs_scale:
        ax.set_yscale('log')
    # ax1.set_yscale('log')
    fig.legend(handles = handles, bbox_to_anchor = (1.1,0.9))
    ax1.set_ylabel('L2norm')
    ax1.set_xlabel('Picard Iteration')
    ax2.set_xlabel('FGMRES Iteration')
    ax4.set_ylabel('L2norm')
    ax4.set_xlabel('Precond Iteration')
    ax3.set_xlabel('Picard Iteration')
    ax3.set_ylabel('Max Ice Speed (m/s)')

    fig.savefig(figdir+'precond_exps/comp_solver.png')

    if (startdate is not None):
        ax5.set_title(startdate+' to '+enddate)
    ax5.set_xlabel('Picard Iteration')
    ax5.set_ylabel('FGMRES Iteration')
    fig2.legend(handles = handles, bbox_to_anchor = (1.25,0.9))
    fig2.savefig(figdir+'precond_exps/its_solver.png')

    ax6.set_xlabel('Picard Iteration')
    ax6.set_ylabel('L2norm')

    if (startdate is not None):
        ax6.set_title(startdate+' to '+enddate+' Hour: 23')
    fig3.legend(handles = handles, bbox_to_anchor = (1.25,0.9))
    fig3.savefig(figdir+'precond_exps/nonlin_solver.png')

    ax7.set_xlabel('FGMRES Iteration')
    ax7.set_ylabel('L2norm')

    if (startdate is not None):
        ax7.set_title(startdate+' to '+enddate+' Hour: 23')
    fig4.legend(handles = handles, bbox_to_anchor = (1.25,0.9))
    fig4.savefig(figdir+'precond_exps/fgmres_norm.png')

    ax8.set_xlabel('Picard Iteration')
    ax8.set_ylabel('Max ice speed (m/s)')

    fig5.legend(handles = handles, bbox_to_anchor = (1.4,0.9))
    fig5.savefig(figdir+'precond_exps/maxvel_picard.png')

#------------------------------------------------------------
def plot_1d(data_exps , experiments      , 
            datestr   , Parameters,
            var_label ,
            xlabel    , ylabel    , 
            title     , figname   , 
            IMEX = False):
    '''
    Docstring for plot_1d
    
    All of the data should be for the same case, hence should have the same shapes.

    :param data_exps: Description
    :param label_exps: Description
    :param var: Description
    :param dx: Description
    :param xlabel: Description
    :param ylabel: Description
    :param figdir: Description
    :param case: Description
    :param figname: Description


    '''
    dx = Parameters.dx


    shape = np.shape(data_exps[experiments[0]][datestr][var_label])
    shape_x = shape[2]
    shape_y = shape[1]

    nx = shape_x//2
    ny = shape_y//2

    X = np.arange(0, shape_x, 1)*dx
    Y = np.arange(0, shape_y, 1)*dx

    plt.figure(1)
    for i, exp in enumerate(experiments):
        
        var = data_exps[exp][datestr][var_label]
        plt.plot(X[:], var[0,ny, :], label = Parameters.exp[i], color = colors_list1[i])
    
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(Parameters.figdir+'/'+Parameters.case+'/'+figname)

    dt_handles = {1:Line2D([0], [0], color='k', linestyle='-', label='1 min'), 
               5:Line2D([0], [0], color=colors_list1[1], linestyle='-', label='5 min'), 
               20:Line2D([0], [0], color=colors_list1[2], linestyle='-', label='20 min'), 
               40:Line2D([0], [0], color=colors_list1[3], linestyle='-', label='40 min'),
               60:Line2D([0], [0], color=colors_list1[4], linestyle='-', label='60 min'), 
               120:Line2D([0], [0], color=colors_list1[5], linestyle='-', label='120 min'), 
               180:Line2D([0], [0], color=colors_list1[6], linestyle='-', label='180 min')
    }


    if IMEX:
        fig = plt.figure(2, figsize = (5, 4))
        ax = plt.axes()
        handles = []
        seen_dt = set()
        scheme_handles = [
            Line2D([0], [0], color='k', linestyle='-',  label='SIT'),
            Line2D([0], [0], color='k', linestyle='--', label='IMEX'),
        ]
        for i, data_exp in enumerate(data_exps):
            exp = Parameters.exp[i]
            var = data_exp[var_label]
            dt = extract_number(exp)

            if exp.startswith('imex'):
                linestyle = '--'
            else:
                linestyle = '-'

            color = dt_to_color.get(dt)

            if dt not in seen_dt:
                handle = dt_handles.get(dt)
                handles.append(handle)
                seen_dt.add(dt)

            plt.plot(X[-100:], var[0,200, -100:], 
                    linestyle = linestyle, 
                    color = color)

        
        handles = handles + scheme_handles

        fig.legend(handles, [h.get_label() for h in handles],
                loc='outside upper right', frameon=False, bbox_to_anchor = (1.2, 0.9))

        plt.title(title)
        plt.legend()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        ax.set_aspect('auto')
        plt.savefig(Parameters.figdir+'/'+Parameters.case+'/'+figname)
        











