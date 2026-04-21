import math
import numpy as np

def solve_C(A, B, D, L, tol=1e-10, max_iter=100):
    # Precompute constants
    U = math.sqrt(A / B)
    k = math.sqrt(A * B) * L / D

    # Function f(C) = 0
    def f(C):
        return C - 4 * U * math.tanh(k * C)

    # Derivative f'(C)
    def df(C):
        t = math.tanh(k * C)
        return 1 - 4 * U * k * (1 - t*t)

    # Initial guess (good default)
    C = 4 * U  # works well in most cases

    for i in range(max_iter):
        C_new = C - f(C) / df(C)

        if abs(C_new - C) < tol:
            return C_new

        C = C_new

    raise RuntimeError("Did not converge")

# Example usage
A = 1.0
B = 1.0
D = 1.0
L = 1.0

cw = 5.36e-3
cair = 1.2e-3
rhoair = 1.3
rhowater = 1026
uair = 10
tax = cair*rhoair*uair**2
Cw = rhowater*cw
Pstar = 27.5e3*np.exp(-20*(1-0.9))
# C = 4*0.01
C = 4*np.sqrt(tax/Cw)
L = 2000e3
x = np.linspace(1500e3, L, 10000)
A = (8/9)*(C/Pstar)

C = solve_C(tax, Cw, A, L)
print("C =", C)