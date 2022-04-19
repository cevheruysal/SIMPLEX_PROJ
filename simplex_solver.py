import numpy as np
import numpy.ma as ma

np.set_printoptions(suppress=True, precision=2)

def solve_simplex(std_form, var_names=None):
  step = std_form

  print(step)

  while not check_opt(step):
    step = iterate(step)
    """ if input("Press Enter to continue...") == "c":
        return print("run aborted!") """
    print(step)

  bv, nbv, bv_values = bv_nbv(step)
  print("optimal solution is found to be:{}\nwith basic variables valued at: {}".format(step[0,-1], bv_values[1:]))

"""def solve_simplex(A,b,c):
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

def check_opt(step) -> bool:
  return not np.any(step[0,1:]<0)

def pivot(step):
  v = np.argmin(step[0,1:]) + 1 #+1 is used to skip over the coefficient of the objective variable z in the 0th row
  
  temp_col = step[1:,-1]/step[1:,v]
  p = np.argmin(ma.array(temp_col, mask = temp_col < 0, fill_value = np.inf))
  return p+1,v

def iterate(step):
  i,j = pivot(step)
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