import simplex_solver as ss
import linear_program as linp
import expression as ex
import numpy as np

eq1 = ex.expr("2x_1 +x_2 <= 16")
# eq2 = ex.expr("x_1 +3x_2 >= 20")
# eq3 = ex.expr("x_1 +x_2 = 10")
eq2 = ex.expr("x_1 +3x_2 <= 20")
eq3 = ex.expr("x_1 +x_2 <= 10")
obj = ex.expr("z_0 := 2x_1 +3x_2")

eqs = (eq1, eq2, eq3)

lp = linp.LP(obj, eqs)

# lp.constructAbc()
# lp.constructPhs1()
# print(lp.std_tableau)

ss.solve_lp(lp, "max", True)

# print(ss.solve_lp(lp, "max", False))
# lp.obj.parse2mono()
# print(lp.obj.canon_row())