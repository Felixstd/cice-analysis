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
    #print(xr.open_dataset('/home/fsd001/analysis/ciceplotting/B15mink1_480_iceh_inst.2005-01-02-00000.nc', decode_times = False))

    return dataset_exp

def read_cicelog(filename, monitor_nonlin, monitor_fgmres):

    if monitor_nonlin:

        nonlin_value = []
        progress_value = []

    if monitor_fgmres : 
        fgmres_value = []

    with open(filename, "r") as f:
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

            if monitor_fgmres:
                if "fgmres_L2norm" in line:
                    m = re.search(
                        r"iter_fgmres=\s*(\d+)\s+fgmres_L2norm=\s*([0-9.D+-]+)",
                        line
                    )
                    if m:
                        it = int(m.group(1))
                        val = float(m.group(2).replace("D", "E"))
                        fgmres_value.append(val)

    if monitor_nonlin and monitor_fgmres:
        return nonlin_value, progress_value, fgmres_value

    else:
        return nonlin_value, progress_value






