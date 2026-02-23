#%%
import numpy as np
import matplotlib.pyplot as plt
import time 
import warnings

from scipy.sparse.linalg import gmres


warnings.filterwarnings("ignore", category=DeprecationWarning)

plt.style.use('/home/fsd001/cice-analysis/ciceplotting/ciceplotting/plotting/science.mplstyle')

#%%

def quad(x, A, b, c):

    return (0.5*x.T*A*x - b.T*x + c)


def steepest_descent(A, b, x, imax = 100, eps = 1e-4):

    print('Solving Ax = b with Steepest-Descent')
    start = time.perf_counter()
    r = b - A*x
    delta = r.T*r
    delta_0 = delta
    tol = eps**2*delta_0

    error_its = []

    for i in range(0, imax):

        print('its, error: ', i, delta[0,0])
        error_its.append(delta[0, 0])


        if delta < tol:
            break

        q = A*r
        alpha = float(delta/(r.T*q))
        x = x + alpha*r

        if (i%50 == 0):
            r = b-A*x
        else:
            r = r-alpha*q
        
        delta = r.T*r
    
    end = time.perf_counter()



    return x, error_its, end-start

def conjugate_gradients(A, b, x, imax = 100, eps = 1e-4):

    print('Solving Ax = b with Conjugate-Gradients')
    start = time.perf_counter()

    r = b - A*x
    d = r
    delta_n = r.T*r
    delta_0 = delta_n
    tol = eps**2*delta_0
    error_its = []


    for i in range(0, imax):

        print('its, error: ', i, delta_n[0,0])
        error_its.append(delta_n[0, 0])

        if delta_n < tol:
            break

        q = A*d
        alpha = float(delta_n/(d.T*q))
        print(d.T*q)
        x = x+alpha*d

        if (i%50 == 0):
            r = b-A*x
        else:
            r = r-alpha*q
        
        delta_o = delta_n
        delta_n = r.T*r
        beta = float(delta_n/delta_o)
        print(beta)
        d = r+beta*d

        print(np.linalg.norm(r), delta_n)
    
    end = time.perf_counter()

    return x, error_its, end-start



def BCG(A, b, x, imax = 100, eps = 1e-4):

    r = b - A*x
    r_0_prime = r 
    print(r, r_0_prime)
    p = r
    delta_n = r.T*r
    tol = eps**2*delta_n
    error_its = []
    r_p1 = r

    for i in range(0, imax):
        
        delta_n = r.T*r

        print('its, error: ', i, delta_n[0,0])
        error_its.append(delta_n[0, 0])

        if delta_n < tol:
            break
        print((r.T*r_0_prime))
        alpha = float((r.T*r_0_prime)/((A*p).T*r_0_prime))

        s = r - alpha*A*p

        As = A*s
        omega = float(((As).T*s)/((As.T*As)))
        x = x + alpha*p+omega*s
        r_p1 = s - omega*As
        beta = float((alpha/omega)*(r_p1.T*r_0_prime)/(r.T*r_0_prime))

        p = r_p1+beta*(p - omega*A*p)

        r = r_p1


    return x, error_its


def residual_callback(pr_norm):
    """Callback function to append the preconditioned residual norm to a list."""
    global residual_norms
    residual_norms.append(pr_norm)




#%% 
s = 100
# ------------------------ 
# Defining the system of equations 
# ------------------------

A = np.matrix([[3, 2], [-2, 6]])
b = np.matrix([[2], [-8]])
c = 0

x1 = np.linspace(-8,8, s)
x2 = np.linspace(-8, 8, s)
x1, x2 = np.meshgrid(x1, x2)
f = np.zeros_like(x1)

zs = np.zeros((s, s))
for i in range(s):
    for j in range(s):
        x = np.matrix([[x1[i,j]], [x2[i,j]]])
        zs[i,j] = quad(x, A, b, c)


x_sol, error_sd, time_sd = steepest_descent(A, b, np.matrix([[-400], [100]]), eps = 1e-8)

x_sol_gc, error_cg, time_cg = conjugate_gradients(A, b, np.matrix([[-400], [100]]), eps = 1e-8)

x_sol_BCG, error_bcg = BCG(A, b, np.matrix([[-400], [100]]), eps = 1e-8)
print(x_sol_BCG, x_sol_gc, x_sol)

residual_norms = []
x, info = gmres(A, b, x0 = [-400, 100], callback=residual_callback, rtol=1e-8, M = None, restart = 1, maxiter = 100)
print(x)
#%% 

plt.figure()
plt.plot(error_sd, label = 'Steepest-Descent')
plt.plot(error_cg, label = 'Conjugate-Gradients')
plt.plot(error_bcg, label = 'BCG')
plt.plot(residual_norms, label = 'GMRES')
plt.legend()
plt.yscale('log')
# plt.xscale('log')
plt.xlabel('Iterations')
plt.ylabel(r'$||r_i||$')
plt.savefig('convergence.png')




#----------------------------
# plotting the system of equations
#----------------------------
xl = -4
xr = 4

yl_1 = (b[0,0] - xl*A[0,0])/A[0,1]
yr_1 = (b[0,0] - xr*A[0,0])/A[0,1]

yl_2 = (b[1,0] - xl*A[1,0])/A[1,1]
yr_2 = (b[1,0] - xr*A[1,0])/A[1,1]

plt.figure()
plt.plot([xl, xr], [yl_2, yr_2])
plt.plot([xl, xr], [yl_1, yr_1])
plt.xlabel(r'$x_1$')
plt.ylabel(r'$x_2$')
plt.grid()
plt.savefig('system.png')
# %%


fig = plt.figure(figsize = (6, 5))
ax = plt.axes()

px = ax.contourf(x1, x2, zs)
fig.colorbar(px)
ax.set_xlabel(r'$x_1$')
ax.set_ylabel(r'$x_2$')

plt.savefig('contours.png')
