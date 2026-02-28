import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

'''
Small script to compute the eigenvalues of the matrix A for the 
discretized divergence for curvilinear coordinates. 

The system of equations is given by 

A_Dd x = b

In this case, 

x = [u11,u12,u21,u22] and b = [D11,D12,D21,D22]. We assumed v = 0. 
'''


h11, h22, h33, h44 = sp.symbols('h11, h22, h33, h44', 
                                real = True, 
                                positive = False)

h13, h24, h31, h42 = sp.symbols('h13, h24, h31, h42', 
                                real = True, 
                                positive = True)

m = sp.Matrix([[h11, 0, h13, 0], 
               [0, h22, 0, h24], 
               [h31, 0, h33, 0], 
               [0, h42, 0, h44]])

eigenvalues = m.eigenvals()

for i, eig in enumerate(list(eigenvalues.keys())):
    print('eigenvalue: ',i, eig)
