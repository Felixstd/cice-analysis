import numpy as np 
import matplotlib.pyplot as plt


datadir = '/home/fsd001/data/ppp5/cice/runs/CGCidealDebug/'


Auv = np.loadtxt(datadir+'AuE_vN')
Avu = np.loadtxt(datadir+'AvN_uE')

Auv = np.reshape(Auv, (52,52))
Avu = np.reshape(Avu, (52, 52))

# Auv = Auv[1:51, 1:51]
# Avu = Avu[1

plt.figure()
pc = plt.pcolormesh(Auv - Avu)
plt.colorbar(pc)
plt.savefig('matrix.png', dpi = 500)