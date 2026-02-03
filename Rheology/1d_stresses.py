import numpy as np
import matplotlib.pyplot as plt

plt.style.use('/home/fsd001/cice-analysis/ciceplotting/ciceplotting/plotting/science.mplstyle')
e = 2
Pstar = 27.5e3
mu_b = 1.2
mu0 = 0.2
muinf = 0.8
delta_mu = muinf-mu0
dmean = 1000
rhoice = 900
psi_d = 1/2*((1+e**(-2))**(1/2)-1)
psi_c = 1/2*(-(1+e**(-2))**(1/2)-1)

def VP_rheology(dudx, dudx_c = 1e-8):
    
    sigma_11 = np.zeros_like(dudx)
    psi_d = 1/2*((1+e**(-2))**(1/2)-1)
    psi_c = 1/2*(-(1+e**(-2))**(1/2)-1)
    
    sigma_11[abs(dudx) < dudx_c] = (psi_d+psi_c)/2 + (psi_d - psi_c)/2*(dudx[abs(dudx) < dudx_c]/dudx_c)
    
    sigma_11[dudx > dudx_c] = psi_d
    sigma_11[dudx < -dudx_c] = psi_c
    
    
    return sigma_11

def GC_rheology(dudx, dudx_c = 1e-8):
    sigma_11 = np.zeros_like(dudx)
    
    I = dmean*abs(dudx)*np.sqrt(rhoice/Pstar)
    mu = mu0 + delta_mu/(1e-3/I+1)
    
    psi_d = ((mu/2 + mu_b)-1)
    psi_c = (-(mu/2 + mu_b)-1)
    
    sigma_11[abs(dudx) < dudx_c] = (psi_d[abs(dudx) < dudx_c]+psi_c[abs(dudx) < dudx_c])/2 + (psi_d[abs(dudx) < dudx_c] - psi_c[abs(dudx) < dudx_c])/2*(dudx[abs(dudx) < dudx_c]/dudx_c)
    
    sigma_11[dudx > dudx_c] = psi_d[dudx > dudx_c]
    sigma_11[dudx < -dudx_c] = psi_c[dudx < -dudx_c]
    
    return sigma_11
    

dudx = np.linspace(-1e-6, 1e-6, 1000000)

sigma_11_VP = VP_rheology(dudx)

sigma_11_GC = GC_rheology(dudx)

positions = [0, psi_c, psi_d]

# new labels
labels = ['0', r'', r'']



plt.figure(figsize= (4, 3))
ax = plt.axes()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.plot(dudx, sigma_11_VP, label = 'VP', color = 'r')
# plt.plot(dudx, sigma_11_GC, label = 'GC', color = 'b')
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.yticks(positions, labels, fontsize = 9)
ax.yaxis.set_label_coords(0.3,0.95)
# ax.spines['bottom'].set_position('center')
ax.fill_betweenx(
    [psi_c, abs(psi_c)-0.28],
    -1e-8, 1e-8,
    color='lightskyblue', alpha=0.3, 
    edgecolor = None
)
ax.fill_betweenx(
    [psi_c, abs(psi_c)-0.28],
    -1e-8, -1e-6,
    color='lightgreen', alpha=0.3, 
    edgecolor = None
)
ax.fill_betweenx(
    [psi_c, abs(psi_c)-0.28],
    1e-8, 1e-6,
    color='lightgreen', alpha=0.3, 
    edgecolor = None
)
ax.spines['left'].set_position('center')
ax.set_ylim(psi_c-0.1, abs(psi_c)-0.15)
plt.xscale('symlog', linthresh = 1e-8)
# plt.xscale('log')
plt.xlabel(r'$\frac{\partial{u}}{\partial{x}}$',fontsize=12)
plt.ylabel(r'Stress', rotation=0, fontsize=12, ha='left')
plt.savefig('sigma_11.png')