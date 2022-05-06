import numpy as np
import numpy.ma as ma
import linear_program as linp

np.set_printoptions(suppress=True, precision=2)

def solve_lp(lp:linp.LP, obj_type:str = "max", _2phs:bool = False):
	# TO DO: big M method

	msg = obj_type + "imizing " + lp.obj.exp
	print(msg) #muhakkak kalacak bir print
	print("subject to equations:")
	for eq in lp.sto:
		msg = "              " + eq.exp
		print(msg) #muhakkak kalacak bir print
	print("\n")

	if _2phs:
		return solve_2phs_simplex(lp, obj_type)

	else:
		lp.constructAbc()
		
		msg = "solve_simplex start:\n"
		print("solve_simplex start:" + (90-len(msg))*"-" + "\n", lp.std_tableau) #muhakkak kalacak bir print

		obj_val, fin_tabl = solve_simplex(lp.std_tableau, obj_type)
		bv, nbv = bv_nbv(fin_tabl, lp.distinct_vars)

		print(f"optimal solution is found to be:{obj_val}\nwith basic variables valued at: {bv}")

def solve_simplex(std_form, obj_type="max"):
	step = std_form

	while not check_opt(step, obj_type):
		i,j = pivot(step, obj_type)
		step = iterate(step, i,j)
		
	msg = "solve_simplex end:"
	print(msg + (90-len(msg))*"-" + "\n", step) #muhakkak kalacak bir print
	
	return step[0,-1], step

def solve_2phs_simplex(lp: linp.LP, obj_type):
	# todo : add the function that transforms the std_forms for the corresponding phases ,
			# add 3 of the cases that can happen after phase 1
	lp.constructPhs1()
	std_form_phs1 = lp.std_tableau

	msg = "solve_2phs_simplex phase 1 initial tableau:"
	print(msg + (90-len(msg))*"-" + "\n", std_form_phs1) #muhakkak kalacak bir print

	w_prime, phs1_output = solve_phs1(std_form_phs1)
	
	msg = "solve_2phs_simplex phase 1 output:"
	print(msg + (90-len(msg))*"-" + "\n", phs1_output) #muhakkak kalacak bir print

	if round(w_prime, 10) == 0:
		std_form_phs2 = lp.constructPhs2(phs1_output) 

		msg = "solve_2phs_simplex phase 2 input:"
		print(msg + (90-len(msg))*"-" + "\n", std_form_phs2) #muhakkak kalacak bir print

		return solve_phs2(std_form_phs2, obj_type)

	elif round(w_prime, 10) > 0: 
		print("there are no optimal feasible solutions available for this linear program")

		return False
	#elif
	
def solve_phs1(std_form):
	for j in range(std_form.shape[1]-2):
		if std_form[0, j+1] != 0:
			for i in range(std_form.shape[0]-1):
				if std_form[i+1, j+1] != 0:
					std_form[0,:] = std_form[0,:] + std_form[i+1,:]

	return solve_simplex(std_form, "min")

def solve_phs2(std_form, obj_type):
	return solve_simplex(std_form, obj_type)


def check_opt(step, obj_type) -> bool:
	if obj_type == "max":
		return not np.any(step[0,1:-1]<0)

	elif obj_type == "min":
		return not np.any(step[0,1:-1]>0)

def pivot(step, obj_type):
	if obj_type == "max":
		v = np.argmin(step[0,1:-1]) + 1 #+1 is used to skip over the coefficient of the objective variable z in the 0th row
		temp_col = ma.array(step[1:,-1]/step[1:,v], mask = step[1:,v] == 0, fill_value = np.inf)
		p = np.argmin(temp_col)
		
	elif obj_type == "min":
		v = np.argmax(step[0,1:-1]) + 1 #+1 is used to skip over the coefficient of the objective variable z in the 0th row
		temp_col = ma.array(step[1:,-1]/step[1:,v], mask = step[1:,v] == 0, fill_value = np.inf)
		p = np.argmin(temp_col)
		
	return p+1,v

def iterate(step, i,j):
	new_step = np.zeros(step.shape)

	new_step[i,:] = step[i,:] / step[i,j]

	for k in range(step.shape[0]):
		if k != i:
			new_step[k,:] = step[k,:] - step[k,j]*new_step[i,:]

	return np.asmatrix(new_step)

def bv_nbv(step, d_vs):
	bv = []
	bv_values = []
	nbv = []

	for j in range(step.shape[1]-1):
		isitbv = bool

		ones = 0
		one_idx = None
		zeros = 0
		other = 0

		for i in range(step.shape[0]):
			if step[i,j] == 1:
				ones = ones +1
				one_idx = i 

			elif step[i,j] == 0:
				zeros = zeros +1

			else:
				other = other +1
			
		isitbv = (ones == 1 and other == 0)

		if isitbv:
			bv.append(d_vs[j])
			bv_values.append(step[one_idx,-1])

		else:
			nbv.append(d_vs[j])

	return dict(zip(bv, bv_values)), nbv