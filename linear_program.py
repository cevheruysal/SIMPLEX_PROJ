import expression as exp
import numpy as np

class LP():
    def __init__(self, objective, equations):
        self.obj = objective
        self.sto = equations
        self.distinct_vars = None

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

        self.distinct_vars = distinct_vars

        std_form_cA = np.zeros((len(self.sto) + 1, len(self.distinct_vars)))
        for j in range(len(self.distinct_vars)):
            for i in range(len(self.sto)+1):
                if distinct_vars[j] in cnn[i]:
                    std_form_cA[i,j] = cnn[i][distinct_vars[j]]

        std_form_0b = np.transpose(np.asmatrix(b))

        return std_form_cA, std_form_0b