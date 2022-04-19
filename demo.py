import simplex_solver as ss
import linear_program as linp
import expression as expre
import numpy as np

"""A = np.mat([[2,1],[1,1],[1,0]])
b = np.mat([[100],[80],[40]])
c = np.mat([3,2])
"""
#ss.solve_simplex(A,b,c)

""" st = ss.std_form(A,b,c)
print(st)
bv, nbv = ss.bv_nbv(st)

print(bv,nbv) """

""" print(ss.pivot(st))
st1 = ss.iterate(st)
print(st1)
bv, nbv = ss.bv_nbv(st1)

print(bv,nbv) """
#x1  = 20, x2 = 60 @ optimal solution 

eq1 = expre.expr("2x_1 +x_2 <= 5")
eq2 = expre.expr("x_1 >= 1.5")
obj = expre.expr("z_0 := x_1 +x_2")

eqs = (eq1, eq2)

lp = linp.LP(obj, eqs)

print(lp.constructAbc())