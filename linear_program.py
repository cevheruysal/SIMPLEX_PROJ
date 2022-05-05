import expression as exp
import numpy as np

class LP():
    def __init__(self, objective:exp.expr, equations:tuple):
        self.obj = objective
        self.sto = equations
        self.distinct_vars = None
        self.std_tableau = None

    def parseEqs(self, b=[], cnn=[], id = 0, _2phs = False):
        for eq in self.sto:
            eq.parse2mono()
            id = id + 1
            eq.id = id
            
            if not _2phs:
                cnn_i, b_i = eq.canon_row()
            else:
                cnn_i, b_i = eq.canon_row_2phs()

            cnn.append(cnn_i)
            b.append(b_i)
        return cnn, b

    def constructAbc(self):
        distinct_vars = []

        b = []
        cnn = []

        id = 0
        self.obj.id = id
        self.obj.parse2mono()
        cnn_0, b_0 = self.obj.canon_row()
        b.append(b_0)
        cnn.append(cnn_0)

        cnn, b = self.parseEqs(b, cnn, id)
    
        alph = {"z":0, "w":1, "x":2, "s":3, "e":3, "a":4}
        for item in cnn:
            for v in item.keys():
                if v in distinct_vars.values():
                    pass
                else:
                    appended = False
                    for idx, vs in enumerate(distinct_vars):
                        if alph[vs[0]] > alph[v[0]]:
                            appended = True
                            distinct_vars.insert(idx, v)
                    if not appended:
                        distinct_vars.append(v)

        self.distinct_vars = distinct_vars

        std_form_cA = np.zeros((len(self.sto) + 1, len(self.distinct_vars)))
        for j in range(len(self.distinct_vars)):
            for i in range(len(self.sto)+1):
                if self.distinct_vars[j] in cnn[i]:
                    std_form_cA[i,j] = cnn[i][self.distinct_vars[j]]

        std_form_0b = np.asmatrix(b).T
        self.std_tableau = np.concatenate((std_form_cA, std_form_0b), axis = -1)

        return True

    def constructPhs1str(self, id = 0):
        phs1str = "w_0lin :="
        for eq in self.sto:
            for mono in eq.lhs_monos:
                if mono['type'] == "ARTF":
                    phs1str = phs1str + " " + str(mono['coef']) + mono['vName']
        return exp.expr(phs1str, id)

    def constructPhs1(self):
        d_vs = []

        b = []
        cnn = []

        id = 0

        cnn, b = self.parseEqs(b, cnn, id, _2phs = True)

        phs1obj = self.constructPhs1str()
        phs1obj.parse2mono()
        cnn_0, b_0 = phs1obj.canon_row_2phs()
        b.insert(0, b_0)
        cnn.insert(0, cnn_0)

        alph = {"z":0, "w":1, "x":2, "s":3, "e":3, "a":4}
        for item in cnn:
            for v in item.keys():
                if v in d_vs:
                    pass
                else:
                    appended = False
                    for idx in range(len(d_vs)):
                        if alph[v[0]] < alph[d_vs[idx][0]]:
                            appended = True
                            d_vs.insert(idx, v)
                    if not appended:
                        d_vs.append(v)

        self.distinct_vars = d_vs

        std_form_cA = np.zeros((len(self.sto) + 1, len(self.distinct_vars)))
        for j in range(len(self.distinct_vars)):
            for i in range(len(self.sto)+1):
                if self.distinct_vars[j] in cnn[i]:
                    std_form_cA[i,j] = cnn[i][self.distinct_vars[j]]

        std_form_0b = np.asmatrix(b).T
        self.std_tableau = np.concatenate((std_form_cA, std_form_0b), axis = -1)

        return True


    def constructPhs2(self):
        pass