import expression as exp
import numpy as np
import simplex_solver as ss

class LP():
    # TO DO: some way to handle urs (unrestricted in sign) variables
           # goal programming
    
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
        d_vs = []

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
                if v in d_vs:
                    pass

                else:
                    appended = False

                    for idx in range(len(d_vs)):
                        if alph[v[0]] < alph[d_vs[idx][0]]:
                            appended = True
                            d_vs.insert(idx, v)
                            
                            break

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

    def constructPhs1str(self, id = 0):
        phs1str = "w_0 :="

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

                            break

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


    def constructPhs2(self, phs1_output):
        std_tableau_phs2 = phs1_output
        temp_distincvars = self.distinct_vars.copy()
        phs1_bv, nbv = ss.bv_nbv(phs1_output, temp_distincvars)
        
        j = 0
        while j < std_tableau_phs2.shape[1]-1:
            if std_tableau_phs2[0, j] < -1e-10:
                std_tableau_phs2 = np.delete(std_tableau_phs2, j, 1)
                temp_distincvars.pop(j)
        
            else:
                j = j+1
        
        self.obj.parse2mono()
        old_cnn_row = self.obj.canon_row()[0]

        for i, vars in enumerate(temp_distincvars):
            if vars in old_cnn_row.keys():
                std_tableau_phs2[0, i] = old_cnn_row[vars]

        for j, v in zip(range(std_tableau_phs2.shape[1]-1), temp_distincvars):
            if std_tableau_phs2[0, j] < -1e-10 and v in phs1_bv.keys():
                for i in range(std_tableau_phs2.shape[0]-1):
                    if std_tableau_phs2[i+1, j] == 1:
                        std_tableau_phs2[0, :] = std_tableau_phs2[0, :] - std_tableau_phs2[0, j] * std_tableau_phs2[i+1, :]

        return std_tableau_phs2