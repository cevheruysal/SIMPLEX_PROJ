class LP():
  def __init__(self, objective, equations):
    self.obj = objective
    self.sto = equations

  def constructAbc(self):
    distinct_vars = {}

    b = []
    cnn = []

    id = 0
    self.obj.id = id
    self.obj.parse2mono()
    cnn_0, b_0 = self.obj.canon_row()
    b.append(b_0)
    cnn.append(cnn_0)

    for eq in self.sto:
      eq.parse2mono()
      id = id + 1
      eq.id = id
      cnn_i, b_i = eq.canon_row()
      cnn.append(cnn_i)
      b.append(b_i)

    for item in cnn:
      for v in item.keys():
        if v in distinct_vars.values():
          pass
        else:
          distinct_vars[len(distinct_vars)] = v
    
    return distinct_vars