import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

#-------- info --------
exp='Bevp_NE_Ap8'
datestr='2005-02-01-00000'
filein=exp + '_iceh_inst.' + datestr + '.nc'
var='hi'
var_min=0.0
var_max=1.75
#cm='PuRd'
cm='jet'
#----------------------

fileout=exp + '_' + var + '_' + datestr + '.png'

ds=nc.Dataset(filein)
vartp=ds[var]
print(vartp.shape)
varplot=vartp[0,:,:]
print(varplot.shape)

plt.pcolor(varplot, cmap=cm, vmin=var_min, vmax=var_max)
plt.colorbar()
#plt.show()
plt.savefig(fileout)
