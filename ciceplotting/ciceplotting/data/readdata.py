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

def read_cicelog(filename, solver, precond, monitor_nonlin, monitor_solver, monitor_precond):

    print('Reading cicelog')

    nonlin_value   = []
    progress_value = []
    solver_value   = []
    precond_value  = []
    its_precond    = []

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

                        # print(it)
            
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
    
    return nonlin_value, progress_value, solver_value, its_precond, precond_value








