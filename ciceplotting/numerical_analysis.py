import re
import os 
import numpy as np
import xarray as xr 
import cmocean as cm
import matplotlib.pyplot as plt

from ciceplotting.data import readdata
from ciceplotting.utils import arguments 
from ciceplotting.plotting import plot_cice
from collections import defaultdict


plt.style.use('/home/fsd001/cice-analysis/ciceplotting/ciceplotting/plotting/science.mplstyle')


def main():

    datadir = '/home/fsd001/data/ppp5/cice/runs/GlobalCG/history/'
    dir = '/home/fsd001/data/ppp5/cice/runs/GlobalCG/'
    figdir = '/home/fsd001/cice-analysis/Figures/Numerics/'

    datelist = ['2005-01-01-03600']

    args = arguments.parse_args()
    exps = args.exp[1:].split(',')
    velocity_plot = int(args.vel)
    grid = args.grid
    num = int(args.num)
    res = int(args.res)
    solvers = args.solver[1:].split(',')
    monit_precond = int(args.precond)
    preconds = args.precondname[1:].split(',')
    case = args.case[1:]


    if case == 'gx1':
        data_experiments = defaultdict(dict)


    if os.path.isdir(figdir+case):
        print('Case exists')
    else:
        os.mkdir(figdir+case)
    
    figdir = figdir+case+'/'

    
    num_solvers = {}

    for i, exp in enumerate(exps):

        print('Analysing Exp:', i, exp)
        solver = solvers[i]
        precond = preconds[i]
        fileE = dir+'residualE_'+exp
        fileN = dir+'residualN_'+exp
        filedata = datadir+exp+'_iceh_inst.2005-01-01-03600.nc'
        cicelog = dir+'cice.runlog.'+exp

        print('Reading Data')
        if num:
            nonlin_value, progress_value, solver_value, its_solver, its_precond, precond_value, breakdown_its = readdata.read_cicelog(cicelog, 
                                                                                           solver, 
                                                                                           precond, 
                                                                                           True, 
                                                                                           True, 
                                                                                           monit_precond)
            dict_exp = {'nonlin'  : nonlin_value, 
                        'progress': progress_value, 
                        'solver'  : solver_value,
                        'its_solver': its_solver,
                        'precond': precond_value, 
                        'its_precond': its_precond, 
                        'breakdown' : breakdown_its
                        }
            
            num_solvers[exp] = dict_exp

        if case == 'gx1':

            dataset_exp = readdata.readdata(exp, 
                                        datelist[0], 
                                        'iceh_inst', 
                                        datadir)

            data_experiments[exp][datelist[0]] = dataset_exp


        if res:

            dataE = np.loadtxt(fileE)
            dataN = np.loadtxt(fileN)

            res_E = np.reshape(dataE, (52,52))
            res_N = np.reshape(dataN, (52, 52))

            res_E = res_E[1:51, 1:51]
            res_N = res_N[1:51, 1:51]
            
        if velocity_plot:
            dataset_exp = xr.open_dataset(filedata, decode_times = False)

            if grid == 'B':
                uvel = dataset_exp['uvel'][0]
                vvel = dataset_exp['vvel'][0]

            elif grid == 'C':
                uvel = dataset_exp['uvelE'][0]
                vvel = dataset_exp['vvelN'][0]

        #---------------------------------------------------
        # FIGURES 
        #---------------------------------------------------


        #----- Figure 1 ------#
        # #----- Showing the residual spatially and norms -----#
        if num:
            if res:
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
                plt.savefig(figdir+'res_'+solver+'.png')

            #------- Figure 2 -------#
            #This shows the L2norm for fgmres and nonlin

            fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout = True, figsize = (10, 5))

            if solver == 'fgmres':
                ax1.set_title('FMGRES')
                

            if solver == 'CG':
                ax1.set_title('Conjugate-Gradients')

            if solver == 'BiCGSTAB':
                ax1.set_title('BiCGSTAB')

            ax1.plot(solver_value)
            ax1.set_yscale('log')

            ax2.plot(nonlin_value)
            ax2.set_title('Nonlinear')
            ax2.set_yscale('log')
            fig.supylabel('L2norm')
            fig.supxlabel('Iterations')
            
            plt.savefig(figdir+'conv_'+solver+'.png')
            plt.close()

            if solver == 'BiCGSTABEll': 
                num_iterations = np.arange(0, len(nonlin_value))
                plt.figure()

                pc = plt.scatter(num_iterations[:-1], nonlin_value[:-1], c = dict_exp['breakdown'][:-1], cmap = 'plasma')
                plt.colorbar(pc, label = 'Number of Breakdowns')
                plt.yscale('log')
                plt.xlabel('Iterations')
                plt.ylabel('Nonlinear L2norm')
                # plt.scatter(np.arange(len(dict_exp['breakdown'])), dict_exp['breakdown'])
                plt.savefig(figdir+'num_breakdowns.png')

            if monit_precond:

                iterations_solver = dict_exp['its_precond']
                mean_its = np.mean(iterations_solver)
                fig = plt.figure()

                if precond == 'CG':
                    plt.title('Conjugate-Gradients')

                plt.xlabel('Iterations')
                plt.ylabel('Count')
                plt.hist(iterations_solver, bins = 20, color = 'royalblue')
                plt.axvline(mean_its, color = 'gray', linestyle = '--', zorder = 0)
                plt.savefig(figdir+'hist_itsprecond.png')



                fig, (ax1, ax2, ax3) = plt.subplots(1, 3, constrained_layout = True, figsize = (10, 5))

                if solver == 'fgmres':
                    ax1.set_title('FMGRES')
                    fig.supylabel('L2norm')

                if solver == 'CG':
                    ax1.set_title('Conjugate-Gradients')
                    ax1.set_ylabel(r'$r^Tr$')
                    ax2.set_ylabel('L2norm')

                if precond == 'CG':
                    ax3.set_title('Conjugate-Gradients')
                    ax3.set_ylabel(r'$r^Tr$')

                elif precond == 'pgmres':
                    ax3.set_title('PGMRES')

                ax1.plot(solver_value)
                ax1.set_yscale('log')

                ax2.plot(nonlin_value)
                ax2.set_title('Nonlinear')
                ax2.set_yscale('log')

                ax3.plot(precond_value)
                ax3.set_yscale('log')


                fig.supxlabel('Iterations')
                
                plt.savefig(figdir+'conv_'+solver+'_'+precond+'.png')



        if velocity_plot:
            maxmin = 1e-2
            cmap = cm.cm.balance 

            fig, (ax1, ax2) = plt.subplots(1, 2, 
                                        constrained_layout = True, 
                                        figsize = (10, 5))

            ax1.pcolor(uvel, 
                    vmin = -maxmin, vmax = maxmin, 
                    cmap = cmap)
            ax1.set_title(r'$u_{ice}$')

            pc = ax2.pcolor(vvel, 
                            vmin = -maxmin, vmax = maxmin, 
                            cmap = cmap)
            ax2.set_title(r'$v_{ice}$')
            fig.colorbar(pc, ax = [ax1, ax2])
            
            plt.savefig(figdir+'vel.png')


        

#--------- Comparaisons between experiments ------------#
    if case == 'gx1':
        print('hrtr')
        for solver in solvers:
            plot_cice.plot_global(data_experiments,
                    exp, 
                    datelist[0], 
                    'uvelE', 
                    [],
                    r"u_E (m/s)", 
                    '',
                    'uvelE_'+solver, 
                    figdir, 
                    case)

    fig1, ax1 = plt.subplots()
    colors = ['royalblue', 'forestgreen', 'maroon', 'darkorange']
    for i, exp in enumerate(exps):
        solver = solvers[i]

        ax1.plot(num_solvers[exp]['nonlin'], label = solver, color = colors[i])

    ax1.set_yscale('log')
    ax1.set_xlabel('Nonlinear Iterations')
    ax1.set_ylabel('L2norm')
    fig1.legend(loc = 'upper right', bbox_to_anchor = (1.3, 0.9))
    fig1.savefig(figdir+'comp_conv.png')

    fig1, ax1 = plt.subplots()
    for i, exp in enumerate(exps):
        solver = solvers[i]

        ax1.plot(num_solvers[exp]['solver'], label = solver, color = colors[i])

    ax1.set_yscale('log')
    ax1.set_xscale('log')
    ax1.set_xlabel('Solver Iterations')
    ax1.set_ylabel('L2norm')
    fig1.legend(loc = 'upper right', bbox_to_anchor = (1.3, 0.9))
    fig1.savefig(figdir+'comp_conv_solv.png')


    solver_values = np.array([num_solvers[k]['nonlin'] for k in exps])

    diff_solvers = np.diff(solver_values)[0]

    fig1, ax1 = plt.subplots()

    ax1.plot(diff_solvers)

    ax1.set_yscale('symlog', linthresh = 1e-8)
    # ax1.set_xscale('log')
    ax1.set_xlabel('Solver Iterations')
    ax1.set_ylabel(r'$r_{B} - r_{G}$ ')
    fig1.legend(loc = 'upper right', bbox_to_anchor = (1.3, 0.9))
    fig1.savefig(figdir+'diff_conv_solv.png')

    fig2, ax2 = plt.subplots()
    colors = ['royalblue', 'forestgreen']
    for i, exp in enumerate(exps):
        solver = solvers[i]

        iterations_solver = num_solvers[exp]['its_solver']
        mean_its = np.mean(iterations_solver)

        ax2.hist(iterations_solver, color = colors[i], bins = 20, label = solver, alpha = 0.7)
        ax2.axvline(mean_its, color = colors[i], linestyle = '--', zorder = 1)

    ax2.set_ylabel('Counts')
    ax2.set_xlabel("Iterations")
    ax2.legend(loc = 'best')#, bbox_to_anchor = (1.25, 0.9))
    fig2.savefig(figdir+'hist_its_solver.png')

if __name__ == '__main__':
    main()