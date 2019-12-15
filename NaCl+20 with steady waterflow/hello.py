import matplotlib.pyplot as plt
import numpy as np
N = 101
Ncell = 201
solute = ['Na', 'K', 'Cl', 'HCO3', 'H2CO3', 'CO2', 'HPO4', 'H2PO4', 'urea', 'NH3', 'NH4', 'H', 'HCO2', 'H2CO2', 'glu']
###################### concentration
for s in range(15):
    filename = 'malePT_con_of_' + solute[s] + '_in_cell.txt'
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    cell=np.loadtxt(filename)
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('cellular ' + solute[s] + ' concentration')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("conc")
    plt.savefig('plot figure\jingyang\Conc of ' + solute[s] + ' in cell')