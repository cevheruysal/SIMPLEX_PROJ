import expression as exp
import numpy as np

class LP():
    def __init__(self, objective, equations):
        self.obj = objective
        self.sto = equations
        self.distinct_vars = None
        self.std_tableau = None

    def parseEqs(self, b=[], cnn=[], id = 0, phs_2 = False):
        for eq in self.sto:
            eq.parse2mono()
            id = id + 1
            eq.id = id
            
            if not phs_2:
                cnn_i, b_i = eq.canon_row()
            else:
                cnn_i, b_i = eq.canon_row_2phs()

            cnn.append(cnn_i)
            b.append(b_i)
        return cnn, b

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

        cnn, b = self.parseEqs(b, cnn, id)
    
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
                if self.distinct_vars[j] in cnn[i]:
                    std_form_cA[i,j] = cnn[i][self.distinct_vars[j]]

        std_form_0b = np.transpose(np.asmatrix(b))
        self.std_tableau = np.concatenate((std_form_cA, std_form_0b), axis = -1)

        return True

    def constructPhs1str(self, id = 0):
        phs1str = "w :="
        for eq in self.sto:
            print(eq.rhs_monos)
            for mono in eq.lhs_monos:
                print(mono['type'])
                if mono['type'] == "ARTF":
                    phs1str = phs1str + " " + str(mono['coef']) + mono['vName']
        return exp.expr(phs1str, id)

    def constructPhs1(self):
        distinct_vars = {}

        b = []
        cnn = []

        id = 0

        cnn, b = self.parseEqs(b, cnn, id, phs_2 = True)

        phs1obj = self.constructPhs1str()
        phs1obj.parse2mono()
        cnn_0, b_0 = phs1obj.canon_row_2phs()
        b.insert(0, b_0)
        cnn.insert(0, cnn_0)

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
                if self.distinct_vars[j] in cnn[i]:
                    std_form_cA[i,j] = cnn[i][self.distinct_vars[j]]

        std_form_0b = np.transpose(np.asmatrix(b))
        self.std_tableau = np.concatenate((std_form_cA, std_form_0b), axis = -1)

        return True


    def constructPhs2(self):
        pass