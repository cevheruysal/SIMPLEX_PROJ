import numpy as np
import numpy.ma as ma

np.set_printoptions(suppress=True, precision=2)

def solve_simplex(std_form, obj_type="max"):
  step = std_form

  print(step)

  while not check_opt(step, obj_type):
    input("devam?: ")
    i,j = pivot(step, obj_type)
    print(i,j)
    step = iterate(step, i,j)
    print(step)

  bv, nbv, bv_values = bv_nbv(step)
  print(f"optimal solution is found to be:{step[0,-1]}\nwith basic variables valued at: {bv_values[1:]}")
  
  return step[0,-1]

""" more primitive simplex solver when A, b, c is explicitly given
def solve_simplex(A,b,c):
  step = std_tableau(A,b,c)

  print(step)

  while not check_opt(step):
    step = iterate(step)
    ''' if input("Press Enter to continue...") == "c":
        return print("run aborted!") '''
    print(step)

  bv_values = bv_nbv(step)[2]
  print("optimal solution is found to be:{}\nwith basic variable values: {}".format(step[0,-1], bv_values[1:]))

def std_tableau(A,b,c):
    assert c.shape[0] == 1
    assert c.shape[1] == A.shape[1]
    assert A.shape[0] == b.shape[0]
    assert b.shape[1] == 1

    I = np.identity(b.shape[0])

    temp = np.concatenate((np.mat([1]),np.zeros((b.shape[0], 1))))
    temp0 = np.concatenate((-c,A))
    temp1 = np.concatenate((np.zeros((1,b.shape[0])), I))
    temp2 = np.concatenate((np.mat([0]), b))

    step = np.concatenate((temp, temp0, temp1, temp2), axis = -1)
     
    return step"""

def solve_2phs_simplex(std_form, obj_type):
  # todo : add the function that transforms the std_forms for the corresponding phases ,
         # add 3 of the cases that can happen after phase 1
  #std_form_phs1 = somefunc(std_form)
  w_prime, phs1_output = solve_phs1(std_form_phs1)

  if round(w_prime, 10) == 0:
    std_form
    solve_phs2(, obj_type)
  #elif
   
def solve_phs1(std_form):
  obj_type = "min"

  for j in range(std_form.shape[1]-2):
    if std_form[0, j+1] != 0:
      for i in range(std_form.shape[0]-1):
        if std_form[i+1, j+1] != 0:
          std_form[0,:] = std_form[0,:] + std_form[i+1,:]
  
  return solve_simplex(std_form, obj_type), std_form

def solve_phs2(std_form):
  pass

def check_opt(step, obj_type) -> bool:
  if obj_type == "max":
    return not np.any(step[0,1:]<0)
  elif obj_type == "min":
    return not np.any(step[0,1:]>0)

def pivot(step, obj_type):
  if obj_type == "max":
    v = np.argmin(step[0,1:-1]) + 1 #+1 is used to skip over the coefficient of the objective variable z in the 0th row
    
    #temp_col = step[1:,-1]/step[1:,v]
    temp_col = ma.array(step[1:,-1]/step[1:,v], mask = step[1:,v] == 0, fill_value = np.inf)
    p = np.argmin(temp_col)
    #p = np.argmin(ma.array(temp_col, mask = temp_col < 0, fill_value = np.inf))

  elif obj_type == "min":
    v = np.argmax(step[0,1:-1]) + 1 #+1 is used to skip over the coefficient of the objective variable z in the 0th row
    
    #temp_col = step[1:,-1]/step[1:,v]
    temp_col = ma.array(step[1:,-1]/step[1:,v], mask = step[1:,v] == 0, fill_value = np.inf)
    p = np.argmin(temp_col)
    #p = np.argmin(ma.array(temp_col, mask = temp_col < 0, fill_value = np.inf))

  return p+1,v

def iterate(step, i,j):
  new_step = np.zeros(step.shape)

  new_step[i,:] = step[i,:] / step[i,j]
  for k in range(step.shape[0]):
    if k != i:
      new_step[k,:] = step[k,:] - step[k,j]*new_step[i,:]

  return np.asmatrix(new_step)

def bv_nbv(step):
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
            bv.append(j)
            bv_values.append(step[one_idx,-1])
        else:
            nbv.append(j)

    return bv, nbv, bv_values