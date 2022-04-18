import simplex_solver as ss
import numpy as np

A = np.mat([2,1],[1,1],[1,0])
b = np.mat([100],[80],[40])
c = np.mat([3,2])

ss.solve_simplex(A,b,c)

#x1  = 20, x2 = 60 @ optimal solution 