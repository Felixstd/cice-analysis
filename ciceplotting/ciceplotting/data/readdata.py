import numpy as np
import xarray as xr
import re

def readdata(exp, datestr, var, datadir):
    '''
    Function used to open the .nc file from CICE

    :param exp: experiment that will be read 
    :param datestr: date open
    :param var: variable of the output file
    :param datadir: directory of the output file
    '''

    file = exp + '_' + var + '.' + datestr + '.nc'

    dataset_exp = xr.open_dataset(datadir+'/'+file, decode_times = False)

    return dataset_exp


def read_cicelog_dynamics(filename): 

    #---------------------------
    # Reading max speed 
    #---------------------------

    max_speed_arctic = []
    max_speed_antarctic = []
    max_conc = []
    uvel_point = []
    vvel_point= []
    strintx  = []
    strinty  = []
    strocnx  = []
    strocny  = []
    strairx  = []
    strairy  = []

    with open(filename, 'r') as f :
        for line in f.readlines():
            if 'max ice speed' in line:
                line_strip = line.strip()
                line_split = line_strip.split()
                
                max_speed_arctic.append(float(line_split[5]))
                max_speed_antarctic.append(float(line_split[6]))

            if 'max ice concentration' in line:
                line_strip = line.strip()
                line_split = line_strip.split()
                
                max_conc.append(float(line_split[3]))

            if 'velocity:' in line:
                line_strip = line.strip()
                line_split = line_strip.split()

                uvel_point.append(float(line_split[1]))
                vvel_point.append(float(line_split[-1]))

            if 'rheology at point' in line:
                line_strip = line.strip()
                line_split = line_strip.split()
                
                strintx.append(float(line_split[3]))
                strinty.append(float(line_split[-1]))

            if 'ice-ocean stresss at point:' in line:
                line_strip = line.strip()
                line_split = line_strip.split()
                
                strocnx.append(float(line_split[4]))
                strocny.append(float(line_split[-1]))

            if 'ice-atmosphere stress at point:' in line:
                line_strip = line.strip()
                line_split = line_strip.split()

                strairx.append(float(line_split[4]))
                strairy.append(float(line_split[-1]))



    max_speed_arctic = np.asarray(max_speed_arctic)
    max_speed_antarctic = np.asarray(max_speed_antarctic)
    max_conc = np.asarray(max_conc)

    return max_speed_arctic, max_speed_antarctic, max_conc, uvel_point, \
          vvel_point, strintx, strinty, strocnx, strocny, strairx, strairy


def read_cicelog(filename, solver, precond, monitor_nonlin, monitor_solver, monitor_precond):

    print('Reading cicelog')

    nonlin_value   = []
    progress_value = []
    solver_value   = []
    precond_value  = []
    its_precond    = []
    its_solver     = []
    breakdowns_it  = []

    with open(filename, "r") as f:
        previous_iter = None
        for line in f:

            if monitor_nonlin:
                if "nonlin_res_L2norm" in line:
                    m = re.search(
                        r"iter_nonlin=\s*(\d+)\s+nonlin_res_L2norm=\s*([0-9.D+-]+)",
                        line
                    )
                    if m:
                        it = int(m.group(1))
                        val = float(m.group(2).replace("D", "E"))
                        nonlin_value.append(val)

                # progress residual
                elif "progress_res_L2norm" in line:
                    m = re.search(
                        r"iter_nonlin=\s*(\d+)\s+progress_res_L2norm=\s*([0-9.D+-]+)",
                        line
                    )
                    if m:
                        it = int(m.group(1))
                        val = float(m.group(2).replace("D", "E"))
                        progress_value.append(val)

            if monitor_solver:
                if solver+"_L2norm" in line:

                    m = re.search(
                         rf"iter_{re.escape(solver)}=\s*(\d+)\s+{re.escape(solver)}_L2norm=\s*([0-9.D+-]+)",
                            line
                        )
                    if m:
                        it = int(m.group(1))
                        val = float(m.group(2).replace("D", "E"))
                        solver_value.append(val)
                        if it == 1 and previous_iter is not None:
                            its_solver.append(previous_iter)

                        previous_iter = it


                if solver == 'BiCGSTABEll':
                    m = re.search(
                                r"number_of_breakdowns\s*=\s*(\d+)", line
                    )
                    if m :
                        it = int(m.group(1))
                        breakdowns_it.append(it)

                        
            
            if monitor_precond:
                if precond+"_L2norm" in line:
                    m = re.search(
                         rf"iter_{re.escape(precond)}=\s*(\d+)\s+{re.escape(precond)}_L2norm=\s*([0-9.+-DEde]+)",
                            line
                        )
                    if m:
                        it = int(m.group(1))
                        val = float(m.group(2).replace("D", "E"))
                        precond_value.append(val)
                        if it == 0 and previous_iter is not None:
                            its_precond.append(previous_iter)

                        previous_iter = it
    
    return nonlin_value, progress_value, solver_value, its_solver, its_precond, precond_value, breakdowns_it








