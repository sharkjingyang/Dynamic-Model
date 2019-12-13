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
    plt.savefig('plot figure\cellular concentration\conc of ' + solute[s] + ' in cell')
    plt.show()

for s in range(15):
    filename = 'malePT_con_of_' + solute[s] + '_in_LIS.txt'
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    cell=np.loadtxt(filename)
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('LIS ' + solute[s] + ' concentration')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("conc")
    plt.savefig('plot figure\LIS concentration\conc of ' + solute[s] + ' in LIS')
    plt.show()

for s in range(15):
    filename = 'malePT_con_of_' + solute[s] + '_in_lumen.txt'
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    cell = np.loadtxt(filename)
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('lumen ' + solute[s] + ' concentration')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("conc")
    plt.savefig('plot figure\lumen concentration\conc of ' + solute[s] + ' in lumen')
    plt.show()
###################### osmolality
filename ='malePT_osmolality_in_Cell.txt'
file='malePT_volume_of_cell.txt'
volref=10
cell = np.zeros(N * Ncell).reshape(Ncell, N)
vol=np.loadtxt(file)
cell=np.loadtxt(filename)
for i in range(Ncell):
    for j in range(N):
        cell[i][j]=cell[i][j]+60*volref/vol[i][j]
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('cellular osmolality')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("osm")
plt.savefig('plot figure\osm\cellular osmolatity')
plt.show()

filename = 'malePT_osmolality_in_lumen.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(filename)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('lumen osmolality')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("osm")
plt.savefig('plot figure\osm\lumen osmolatity')
plt.show()

file1 = open('malePT_osmolality_in_Cell.txt', 'r')
file2 = open('malePT_osmolality_in_lumen.txt', 'r')
cell1=np.loadtxt(file1)
cell2=np.loadtxt(file2)
cell = np.zeros(N * Ncell).reshape(Ncell, N)
for i in range(Ncell):
    for j in range(N):
        cell[i][j] = cell1[i][j]-cell2[i][j]
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('difference osmolality')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("osm diff (cell-lumen)")
plt.savefig('plot figure\osm\difference osmolatity')
plt.show()
###################### pressure
file = 'malePT_pressure_in_lumen.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('cellular pressure')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("pressure")
plt.savefig('plot figure\cellular pressure')
plt.show()
###################### waterflow
file = 'malePT_waterflow_in_lumen.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('lumen waterflow')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("lumen vol")
plt.savefig('plot figure\lumen flow\water flow')
plt.show()
###################### lumen solute flow
for s in range(15):
    file1 = 'malePT_waterflow_in_lumen.txt'
    file2 = 'malePT_con_of_' + solute[s] + '_in_lumen.txt'
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    cell1=np.loadtxt(file1)
    cell2 = np.loadtxt(file2)
    for i in range(Ncell):
        for j in range(N):
            cell[i][j] = cell1[i][j]*cell2[i][j]
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('lumen' + solute[s] + ' flow')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("solute amout")
    plt.savefig('plot figure\lumen flow\ ' + solute[s] + ' flow')
    plt.show()


for s in range(15):
    filename = 'malePT_con_of_' + solute[s] + '_in_lumen.txt'
    cell = np.loadtxt(filename).reshape(Ncell, N)
    plt.figure()
    plt.plot(cell[:, 0], label="time 0")
    plt.plot(cell[:,2], label="time 2")
    plt.plot(cell[:, 4], label="time 4")
    plt.plot(cell[:, 6], label="time 6")
    plt.plot(cell[:, 8], label="time 8")
    plt.title('lumen' + solute[s] + ' concentration')
    plt.legend(loc="upper left")
    plt.savefig('plot figure\cuttime\ ' + solute[s] + ' in lumen')
    plt.show()

for s in range(15):
    filename = 'malePT_con_of_' + solute[s] + '_in_cell.txt'
    cell = np.loadtxt(filename).reshape(Ncell, N)
    plt.figure()
    plt.plot(cell[:, 0], label="time 0")
    plt.plot(cell[:, 2], label="time 2")
    plt.plot(cell[:, 4], label="time 4")
    plt.plot(cell[:, 6], label="time 6")
    plt.plot(cell[:, 8], label="time 8")
    plt.title('cell' + solute[s] + ' concentration')
    plt.legend(loc="upper left")
    plt.savefig('plot figure\cuttime\ ' + solute[s] + ' in cell')
    plt.show()

###################### cellular volume
file = open('malePT_volume_of_cell.txt', 'r')
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('cellular volume')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("cellular vol")
plt.savefig('plot figure\cellular volume')
plt.show()
##############LIS volume
file = open('malePT_volume_of_LIS.txt', 'r')
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('LIS volume')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("LIS vol")
plt.savefig('plot figure\LIS volume')
plt.show()
###################### flux
for s in range(15):
    filename = 'malePT_flux_of_' + solute[s] + '_lumen_cell.txt'
    cell=np.loadtxt(filename)
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('flux of ' + solute[s] + ' between lumen and cell')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("flux")
    plt.savefig('plot figure\Flux lumen cell\ ' + solute[s] + ' flux_lumen_cell')
    plt.show()

for s in range(15):
    filename = 'malePT_flux_of_' + solute[s] + '_cell_bath.txt'
    cell=np.loadtxt(filename)
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('flux of ' + solute[s] + ' between cell and bath')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("flux")
    plt.savefig('plot figure\Flux cell bath\ ' + solute[s] + ' flux_cell_bath')
    plt.show()

for s in range(15):
    filename = 'malePT_flux_of_' + solute[s] + '_cell_LIS.txt'
    cell=np.loadtxt(filename)
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('flux of ' + solute[s] + ' between cell and LIS')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("flux")
    plt.savefig('plot figure\Flux cell LIS\ ' + solute[s] + ' flux_cell_LIS')
    plt.show()

for s in range(15):
    filename1 = 'malePT_flux_of_' + solute[s] + '_cell_LIS.txt'
    filename2 = 'malePT_flux_of_' + solute[s] + '_cell_bath.txt'
    filename3 = 'malePT_flux_of_' + solute[s] + '_lumen_cell.txt'
    cell1 = np.loadtxt(filename1)
    cell2 = np.loadtxt(filename2)
    cell3 = np.loadtxt(filename3)
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    for i in range(Ncell):
        for j in range(N):
            cell[i][j]=-cell1[i][j]-cell2[i][j]+cell3[i][j]
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('flux of ' + solute[s] + 'in cell whole')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("flux")
    plt.savefig('plot figure\Flux whole\ ' + solute[s] + ' flux_whole_in_cell')
    plt.show()
###################### cellular solute amount
for s in range(15):
    file1 = 'malePT_volume_of_cell.txt'
    file2 = 'malePT_con_of_' + solute[s] + '_in_cell.txt'
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    cell1=np.loadtxt(file1)
    cell2=np.loadtxt(file2)
    for i in range(Ncell):
        for j in range(N):
            cell[i][j] = cell1[i][j]*cell2[i][j]
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('cell ' + solute[s] + ' whole')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("solute amount")
    plt.savefig('plot figure\cellular solute\ ' + solute[s] + ' whole')
    plt.show()
#####################LIS amount
for s in range(15):
    file1 = 'malePT_volume_of_LIS.txt'
    file2 = 'malePT_con_of_' + solute[s] + '_in_LIS.txt'
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    cell1=np.loadtxt(file1)
    cell2=np.loadtxt(file2)
    for i in range(Ncell):
        for j in range(N):
            cell[i][j] = cell1[i][j]*cell2[i][j]
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('LIS ' + solute[s] + ' whole')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("LIS amount")
    plt.savefig('plot figure\LIS solute\ ' + solute[s] + ' whole')
    plt.show()
###################### water flux
file = 'malePT_flux_of_water_cell_bath.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('water flux cell-bath')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Flux cell bath\water flux')
plt.show()

file = 'malePT_flux_of_water_cell_LIS.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('water flux cell-LIS')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Flux cell LIS\water flux')
plt.show()

file = 'malePT_flux_of_water_lumen_cell.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('water flux lumen-cell')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Flux lumen cell\water flux')
plt.show()


filename1 = 'malePT_flux_of_water_cell_LIS.txt'
filename2 = 'malePT_flux_of_water_cell_bath.txt'
filename3 = 'malePT_flux_of_water_lumen_cell.txt'
cell1=np.loadtxt(filename1)
cell2 = np.loadtxt(filename2)
cell3 = np.loadtxt(filename3)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
cell = np.zeros(N * Ncell).reshape(Ncell, N)
for i in range(Ncell):
    for j in range(N):
        cell[i][j] = -cell1[i][j] - cell2[i][j] + cell3[i][j]
plt.title('flux of water in cell whole')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Flux whole\water_flux_whole_in_cell')
plt.show()
###################### solute difference
for s in range(15):
    file1 = 'malePT_con_of_' + solute[s] + '_in_cell.txt'
    file2 = 'malePT_con_of_' + solute[s] + '_in_lumen.txt'
    cell1=np.loadtxt(file1)
    cell2=np.loadtxt(file2)
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    for i in range(Ncell):
        for j in range(N):
            cell[i][j] = cell1[i][j]*cell2[i][j]
    plt.figure()
    plt.plot(cell[1], label="cell 1")
    plt.plot(cell[50], label="cell 50")
    plt.plot(cell[100], label="cell 100")
    plt.plot(cell[150], label="cell 150")
    plt.plot(cell[200], label="cell 200")
    plt.title('cell' + solute[s] + ' difference')
    plt.legend(loc="upper left")
    plt.xlabel("time")
    plt.ylabel("solute conc diff")
    plt.savefig('plot figure\cell lumen concentration difference\ ' + solute[s] + ' difference')
    plt.show()

###############################transporter flux
file = 'male_PT_GLUT2_glu14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('GLUT2_glu_cell_LIS')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ GLUT2_glu_cell_LIS')
plt.show()

file = 'male_PT_GLUT2_glu15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('GLUT2_glu_cell_bath')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ GLUT2_glu_cell_bath')
plt.show()

file = 'male_PT_HATPase_H01.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('HATPase_H_lumen_cell.txt')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ HATPase_H_lumen_cell')
plt.show()

file = 'male_PT_NaKATPase_K14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('NaKATPase_K_cell_LIS')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ NaKATPase_K_cell_LIS')
plt.show()

file = 'male_PT_NaKATPase_K15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('NaKATPase_K_cell_bath')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ NaKATPase_K_cell_bath')
plt.show()

file = 'male_PT_NaKATPase_Na14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('NaKATPase_Na_cell_LIS')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ NaKATPase_K_cell_LIS')
plt.show()

file = 'male_PT_NaKATPase_Na15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('NaKATPase_Na_cell_bath')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ NaKATPase_K_cell_bath')
plt.show()

file = 'male_PT_NaKATPase_NH414.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('NaKATPase_NH4_cell_LIS')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ NaKATPase_NH4_cell_LIS')
plt.show()

file = 'male_PT_NaKATPase_NH415.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('NaKATPase_NH4_cell_bath')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ NaKATPase_NH4_cell_bath')
plt.show()

file = 'male_PT_NHE3_H01.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('NHE3_H_lumen_cell')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ NHE3_H_lumen_cell')
plt.show()

file = 'male_PT_NHE3_Na01.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('NHE3_Na_lumen_cell')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ NHE3_Na_lumen_cell')
plt.show()

file = 'male_PT_NHE3_NH401.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('NHE3_NH4_lumen_cell')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ NHE3_NH4_lumen_cell')
plt.show()

file = 'male_PT_SGLT2_glu01.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('SGLT2_glu_lumen_cell')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ SGLT2_glu_lumen_cell')
plt.show()

file = 'male_PT_SGLT2_Na01.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('SGLT2_Na_lumen_cell')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\Transporter flux\ SGLT2_Na_lumen_cell')
plt.show()

######################################cotransporter flux
file = 'male_PT_[0, 3, 2]_cotransporter_Cl_14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3, 2]_cotransporter_Cl_14')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3, 2]_cotransporter_Cl_14')
plt.show()


file = 'male_PT_[0, 3, 2]_cotransporter_Cl_15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3, 2]_cotransporter_Cl_15')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3, 2]_cotransporter_Cl_15')
plt.show()

file = 'male_PT_[0, 3, 2]_cotransporter_HCO3_14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3, 2]_cotransporter_HCO3_14')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3, 2]_cotransporter_HCO3_14')
plt.show()

file = 'male_PT_[0, 3, 2]_cotransporter_HCO3_15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3, 2]_cotransporter_HCO3_15')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3, 2]_cotransporter_HCO3_15')
plt.show()

file = 'male_PT_[0, 3, 2]_cotransporter_Na_14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3, 2]_cotransporter_Na_14')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3, 2]_cotransporter_Na_14')
plt.show()

file = 'male_PT_[0, 3, 2]_cotransporter_Na_15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3, 2]_cotransporter_Na_15')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3, 2]_cotransporter_Na_15')
plt.show()
############

file = 'male_PT_[0, 3]_cotransporter_HCO3_14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3]_cotransporter_HCO3_14')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3]_cotransporter_HCO3_14')
plt.show()

file = 'male_PT_[0, 3]_cotransporter_HCO3_15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3]_cotransporter_HCO3_15')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3]_cotransporter_HCO3_15')
plt.show()

file = 'male_PT_[0, 3]_cotransporter_Na_14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3]_cotransporter_Na_14')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3]_cotransporter_Na_14')
plt.show()

file = 'male_PT_[0, 3]_cotransporter_Na_15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 3]_cotransporter_Na_15')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 3]_cotransporter_Na_15')
plt.show()

file = 'male_PT_[0, 7]_cotransporter_H2PO4_01.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 7]_cotransporter_H2PO4_01')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 7]_cotransporter_H2PO4_01')
plt.show()

file = 'male_PT_[0, 7]_cotransporter_Na_01.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[0, 7]_cotransporter_Na_01')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[0, 7]_cotransporter_Na_01')
plt.show()
##########
file = 'male_PT_[1, 2]_cotransporter_Cl_14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[1, 2]_cotransporter_Cl_14')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[1, 2]_cotransporter_Cl_14')
plt.show()

file = 'male_PT_[1, 2]_cotransporter_Cl_15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[1, 2]_cotransporter_Cl_15')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[1, 2]_cotransporter_Cl_15')
plt.show()

file = 'male_PT_[1, 2]_cotransporter_K_14.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[1, 2]_cotransporter_K_14')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[1, 2]_cotransporter_K_14')
plt.show()

file = 'male_PT_[1, 2]_cotransporter_K_15.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[1, 2]_cotransporter_K_15')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[1, 2]_cotransporter_K_15')
plt.show()

file = 'male_PT_[2, 12]_cotransporter_Cl_01.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[2, 12]_cotransporter_Cl_01')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[2, 12]_cotransporter_Cl_01')
plt.show()

file = 'male_PT_[2, 12]_cotransporter_HCO2_01.txt'
cell=np.loadtxt(file).reshape(Ncell,N)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('male_PT_[2, 12]_cotransporter_HCO2_01')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("flux")
plt.savefig('plot figure\cotransporter flux\male_PT_[2, 12]_cotransporter_HCO2_01')
plt.show()

####################reabsorb fraction
for s in range(15):
    file1 = 'malePT_waterflow_in_lumen.txt'
    file2 = 'malePT_con_of_' + solute[s] + '_in_lumen.txt'
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    cell1=np.loadtxt(file1)
    cell2 = np.loadtxt(file2)
    for i in range(Ncell):
        for j in range(N):
            cell[i][j] = cell1[i][j]*cell2[i][j]
    frac=np.zeros(N)
    for i in range(N):
        frac[i]=(1-cell[200][i]/cell[0][i])*100
    plt.figure()
    plt.plot(frac, label="reabsorb frac")
    plt.title(solute[s] + ' reabsorb frac')
    plt.legend(loc="upper left")
    plt.xlabel("time(s)")
    plt.ylabel("percent(%)")
    plt.savefig('plot figure\lumen reabsorb frac\whole tubal\lumen frac of ' + solute[s] )
    plt.show()

##############################water reabsorb
file = 'malePT_waterflow_in_lumen.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
frac=np.zeros(N)
for i in range(N):
    frac[i]=(1-cell[200][i]/cell[0][i])*100
plt.figure()
plt.plot(frac, label="reabsorb frac")
plt.title('lumen water reabsorb frac')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("percent")
plt.savefig('plot figure\lumen reabsorb frac\whole tubal\lumen frac of water' )
plt.show()

file1 = 'malePT_waterflow_in_lumen.txt'
file2 = 'malePT_con_of_urea_in_lumen.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell1=np.loadtxt(file1)
cell2 = np.loadtxt(file2)
for i in range(Ncell):
    for j in range(N):
        cell[i][j] = cell1[i][j]*cell2[i][j]
frac1=np.zeros(N)
frac2=np.zeros(N)
for i in range(N):
    frac1[i]=(1-cell[200][i]/cell[0][i])*100
for i in range(N):
    frac2[i]=(1-cell1[200][i]/cell1[0][i])*100
plt.figure()
plt.plot(frac1, label=" urea reabsorb frac")
plt.plot(frac2, label=" water reabsorb frac")
plt.title('urea and water reabsorb frac')
plt.legend(loc="upper right")
plt.xlabel("time(s)")
plt.ylabel("percent(%)")
plt.savefig('plot figure\lumen reabsorb frac\whole tubal\lumen frac of urea and water' )
plt.show()
###########################peak and bottom frac along the tubal
for s in range(15):
    file1 = 'malePT_waterflow_in_lumen.txt'
    file2 = 'malePT_con_of_' + solute[s] + '_in_lumen.txt'
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    cell1=np.loadtxt(file1)
    cell2 = np.loadtxt(file2)
    for i in range(Ncell):
        for j in range(N):
            cell[i][j] = cell1[i][j]*cell2[i][j]
    frac=np.zeros(Ncell)
    for i in range(Ncell):
        frac[i]=(1-cell[i][7]/cell[0][7])*100
    plt.figure()
    plt.plot(frac, label="reabsorb frac")
    plt.title('lumen' + solute[s] + ' reabsorb frac')
    plt.legend(loc="upper left")
    plt.xlabel("cell")
    plt.ylabel("percent")
    plt.savefig('plot figure\lumen reabsorb frac\cells peak\lumen frac of ' + solute[s] )
    plt.show()

file = 'malePT_waterflow_in_lumen.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
frac=np.zeros(Ncell)
for i in range(Ncell):
    frac[i]=(1-cell[i][7]/cell[0][7])*100
plt.figure()
plt.plot(frac, label="reabsorb frac")
plt.title('lumen water reabsorb frac')
plt.legend(loc="upper left")
plt.xlabel("cell")
plt.ylabel("percent")
plt.savefig('plot figure\lumen reabsorb frac\cells peak\lumen frac of water' )
plt.show()

for s in range(15):
    file1 = 'malePT_waterflow_in_lumen.txt'
    file2 = 'malePT_con_of_' + solute[s] + '_in_lumen.txt'
    cell = np.zeros(N * Ncell).reshape(Ncell, N)
    cell1=np.loadtxt(file1)
    cell2 = np.loadtxt(file2)
    for i in range(Ncell):
        for j in range(N):
            cell[i][j] = cell1[i][j]*cell2[i][j]
    frac=np.zeros(Ncell)
    for i in range(Ncell):
        frac[i]=(1-cell[i][22]/cell[0][22])*100
    plt.figure()
    plt.plot(frac, label="reabsorb frac")
    plt.title('lumen' + solute[s] + ' reabsorb frac')
    plt.legend(loc="upper left")
    plt.xlabel("cell")
    plt.ylabel("percent")
    plt.savefig('plot figure\lumen reabsorb frac\cells bottom\lumen frac of ' + solute[s] )
    plt.show()

file = 'malePT_waterflow_in_lumen.txt'
cell = np.zeros(N * Ncell).reshape(Ncell, N)
cell=np.loadtxt(file)
frac=np.zeros(Ncell)
for i in range(Ncell):
    frac[i]=(1-cell[i][22]/cell[0][22])*100
plt.figure()
plt.plot(frac, label="reabsorb frac")
plt.title('lumen water reabsorb frac')
plt.legend(loc="upper left")
plt.xlabel("cell")
plt.ylabel("percent")
plt.savefig('plot figure\lumen reabsorb frac\cells bottom\lumen frac of water' )
plt.show()

file="malePT_ep_in_cell.txt"
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('ep in cell')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("ep")
plt.savefig('plot figure\ep\ep in cell')
plt.show()

file="malePT_ep_in_lumen.txt"
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('ep in lumen')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("ep")
plt.savefig('plot figure\ep\ep in lumen')
plt.show()

file="malePT_ep_in_LIS.txt"
cell=np.loadtxt(file)
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('ep in LIS')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("ep")
plt.savefig('plot figure\ep\ep in LIS')
plt.show()

file1="malePT_ep_in_lumen.txt"
file2="malePT_ep_in_cell.txt"
cell1=np.loadtxt(file1)
cell2=np.loadtxt(file2)
cell=cell1-cell2
plt.figure()
plt.plot(cell[1], label="cell 1")
plt.plot(cell[50], label="cell 50")
plt.plot(cell[100], label="cell 100")
plt.plot(cell[150], label="cell 150")
plt.plot(cell[200], label="cell 200")
plt.title('ep diff lumen-cell')
plt.legend(loc="upper left")
plt.xlabel("time")
plt.ylabel("cell dif")
plt.savefig('plot figure\ep\ep diff lumen cell')
plt.show()