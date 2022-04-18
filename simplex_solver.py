import numpy as np
np.set_printoptions(suppress=True, precision=2)

def solve_simplex(A,b,c):
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

  print(step)

  while not check_opt(step):
    step = iterate(step)
    if input("Press Enter to continue...") == "c"
        return print("run aborted!")
    print(step)

  print("optimal solution is found to be:{}\nwith basic variable values: {}".format(step[0,-1], step[1:,-1].flatten()))

def check_opt(step) -> bool:
  return not np.any(step[0,1:]<0)

def pivot(step):
  v = np.argmin(step[0,1:])+1
  p = np.argmin(step[1:,-1]/step[1:,v])
  return p+1,v

def iterate(step):
  i,j = pivot(step)
  new_step = np.zeros(step.shape)

  new_step[i,:] = step[i,:] / step[i,j]
  for k in range(step.shape[0]):
    if k != i:
      new_step[k,:] = step[k,:] - step[k,j]*new_step[i,:]

  return np.asmatrix(new_step)
