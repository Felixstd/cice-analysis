import numpy as np
import xarray as xr

def readdata(exp, datestr, var, datadir):

    file = exp + '_' + var + '.' + datestr + '.nc'

    dataset_exp = xr.open_dataset(datadir+'/'+file, decode_times = False)
    #print(xr.open_dataset('/home/fsd001/analysis/ciceplotting/B15mink1_480_iceh_inst.2005-01-02-00000.nc', decode_times = False))

    return dataset_exp

