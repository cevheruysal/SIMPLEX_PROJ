import simplex_solver as ss
import linear_program as linp
import expression as ex
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

eq1 = ex.expr("2x_1 +x_2 <= 100")
eq2 = ex.expr("x_1 +x_2 <= 80")
eq3 = ex.expr("x_1 <= 40")
obj = ex.expr("z_0 := 3x_1 +2x_2")

eqs = (eq1, eq2, eq3)

lp = linp.LP(obj, eqs)

lp.constructAbc()

ss.solve_simplex(lp.std_tableau)