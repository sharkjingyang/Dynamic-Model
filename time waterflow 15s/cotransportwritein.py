from defs import *
from values import *
import numpy as np
solute = ['Na', 'K', 'Cl', 'HCO3', 'H2CO3', 'CO2', 'HPO4', 'H2PO4', 'urea', 'NH3', 'NH4', 'H', 'HCO2', 'H2CO2', 'glu']

def compute_cotransport (cell,delmu,jsol):

    numLA = len(cell.dLA)
    flux = np.zeros(numLA)
    for i in range(numLA):
        
        sid = list(cell.dLA[i].solute_id)
        # print(sid)
        mid = cell.dLA[i].membrane_id
        # print(mid)
        this_delmu = list(delmu[i][mid[0]][mid[1]] for i in sid)
        flux = cell.area[mid[0]][mid[1]] * cell.dLA[i].perm * sum(np.array(cell.dLA[i].coef) * this_delmu)

        ind = 0
        # print(sid)
        for k in sid:
            jsol[k][mid[0]][mid[1]] = cell.dLA[i].coef[ind]*flux
            ind += 1
            file = open('male_PT_' +str(sid)+ '_cotransporter_' + solute[
                k] +'_'+ str(mid[0]) + str(mid[1]) + '.txt', 'a')
            file.write(str(jsol[k][mid[0]][mid[1]]) + '\n')
    return jsol
