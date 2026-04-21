import numpy as np
import xarray as xr
import re
from ciceplotting.utils import manip_arrays
from collections import defaultdict

def readdata(exp, datestr, var, datadir):
    '''
    Function used to open the .nc file from CICE

    :param exp: experiment that will be read 
    :param datestr: date open
    :param var: variable of the output file
    :param datadir: directory of the output file
    '''

    file = var + '.' + datestr + '.nc'

    dataset_exp = xr.open_dataset(datadir+'/'+file, decode_times = False)

    return dataset_exp


def read_cicelog_dynamics(filename): 

    #---------------------------
    # Reading max speed 
    #---------------------------


    # Map keywords to (list_key(s), column_indices)
    PATTERNS = {
        'total ice volume':                (('ice_volume_arctic', 'ice_volume_antarctic'),         (5,6)),
        'max ice speed    (m/s)':          (('max_speed_arctic',  'max_speed_antarctic'),          (5,6)),
        'max ice speed  high aice':        (('max_speed_arctic_ha',  'max_speed_antarctic_ha'),          (5,6)),
        'max ice volume':                  (('max_ice_volume_arctic', 'max_ice_volume_antarctic'), (5,6)),
        'max ice concentration':           (('max_conc',),                                          (3,)),
        'velocity:':                       (('uvel_point',  'vvel_point'),                        (1,-1)),
        'rheology at point':               (('strintx',     'strinty'),                           (3,-1)),
        'ice-ocean stresss at point:' :    (('strocnx',    'strocny'),                            (4,-1)),
        'ice-atmosphere stress at point:': (('strairx','strairy'),                                (4,-1)),
        'FGMRES, sol:':                    (('uvel_fgmres', 'vvel_fgmres'),                       (2,-1)),
    }

    data = defaultdict(list)

    with open(filename, 'r') as f:
        for line in f:                          # iterate directly — no .readlines()
            for keyword, (keys, cols) in PATTERNS.items():
                if keyword in line:
                    parts = line.split()        # split once per match
                    for key, col in zip(keys, cols):
                        data[key].append(float(parts[col]))
                    break     


    numpy_keys = {
        'max_speed_arctic', 'max_speed_antarctic',
        'ice_volume_arctic', 'ice_volume_antarctic',
        'max_ice_volume_arctic', 'max_ice_volume_antarctic',
        'max_conc',
    }
    results = {k: np.asarray(v) if k in numpy_keys else v for k, v in data.items()}

    return results


def read_cicelog(filename, solver, precond, monitor_nonlin, monitor_solver, 
                 monitor_precond, startdate = None, enddate = None, block_lines = False ):

    print('Reading cicelog')

    nonlin_value   = []
    progress_value = []
    solver_value   = []
    precond_value  = []
    its_precond    = []
    its_solver     = []
    breakdowns_it  = []
    solver_its_per_cycle = []
    fgmres_per_nonlin = []

    nonlin_cycles  = []
    current_nl_cycle = []
    solver_cycles  = []
    _current_cycles= []
    count_fgmres = 0

    with open(filename, "r") as f:

        lines = f.readlines()

    if block_lines:
        lines = find_block_cicelog(lines,startdate,enddate)
        previous_iter = 0
        previous_iter_nonlin = 0
        previous_iter_solver = 0
    else:
        previous_iter = None
        previous_iter_nonlin = 0
        previous_iter_solver = None
   
    for line in lines:

        if monitor_nonlin:
            if 'monitor_fgmres: iter_fgmres=   0' in line:
                count_fgmres+=1
            if "nonlin_res_L2norm" in line:
                m = re.search(
                    r"iter_nonlin=\s*(\d+)\s+nonlin_res_L2norm=\s*([0-9.D+-]+)",
                    line
                )
                if m:
                    it_nonlin = int(m.group(1))
                    val = float(m.group(2).replace("D", "E"))
                    nonlin_value.append(val)


                    if (it_nonlin == 0 and previous_iter_nonlin is not None):
                        # if block_lines:
                            
                        nonlin_cycles.append(current_nl_cycle)
                        fgmres_per_nonlin.append(count_fgmres)
                        current_nl_cycle = []
                        count_fgmres = 0

                    current_nl_cycle.append(val)
                    previous_iter_nonlin = it_nonlin

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
                    it_solver = int(m.group(1))
                    val = float(m.group(2).replace("D", "E"))
                    solver_value.append(val)
                    # print(it, previous_iter)
                    if it_solver == 0 and previous_iter_solver is not None:
                        its_solver.append(previous_iter)
                        solver_cycles.append(_current_cycles)
                        solver_its_per_cycle.append(previous_iter_solver)
                        _current_cycles = []

                    _current_cycles.append(val)

                    previous_iter_solver = it_solver


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

    pad_solver_cycles = manip_arrays.pad_array(solver_cycles)
    pad_nonlincycles = manip_arrays.pad_array(nonlin_cycles)
    
    return nonlin_value, progress_value, solver_value, its_solver, its_precond, precond_value, \
                breakdowns_it, pad_solver_cycles, solver_its_per_cycle, pad_nonlincycles,fgmres_per_nonlin


def find_block_cicelog(lines, startdate, enddate):

    start_block = 0
    end_block = 0

    for i, line in enumerate(lines):

        if re.search(rf"idate:\s+{startdate}\s+sec:\s+0", line):
            start_block = i
        if re.search(rf"idate:\s+{enddate}\s+sec:\s+0", line) and start_block is not None:
            end_block = i
            break

    block_lines = lines[start_block:end_block]

    return block_lines











