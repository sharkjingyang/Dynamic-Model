import matplotlib.pyplot as plt
import numpy as np
Ncell=200
solute = ['Na', 'K', 'Cl', 'HCO3', 'H2CO3', 'CO2', 'HPO4', 'H2PO4', 'urea', 'NH3', 'NH4', 'H', 'HCO2', 'H2CO2', 'glu']

cell1=np.loadtxt('malePT_potential_gradient_Lumen_Cell.txt')
cell2=np.loadtxt('malePT_potential_gradient_Lumen_Cell1.txt')
plt.figure()
plt.plot(cell1,label='ep dif bottom')
plt.plot(cell2,label='ep dif peak')
plt.legend(loc="upper left")
plt.title('ep dif lumen cell bottom')

plt.show()
