# This file is used to check individual segment. Type 'python computation.py' in the terminal to run.

from driver import compute
from values import *
from defs import *
import electrochemical
import water
import glucose
import cotransport
import cotransportwritein
import NHE3
import ATPase
import NKCC
import KCC
import NCC
import ENaC
import Pendrin
import AE1
import NHE1
import NaKCl2
import flux

solute = ['Na', 'K', 'Cl', 'HCO3', 'H2CO3', 'CO2', 'HPO4', 'H2PO4', 'urea', 'NH3', 'NH4', 'H', 'HCO2', 'H2CO2', 'glu']
compart = ['Lumen', 'Cell', 'ICA', 'ICB', 'LIS', 'Bath']
cw = Vref * 60e6

N = input('Choose how many time step u want: ')
N = int(N)
N = N + 1

Ncell = input('How many cell do you want: ')
Ncell = int(Ncell)
Ncell = Ncell + 1

gender = "Male"

method = "Broyden"

segment = 'PT'

diabete = 'N'

if gender == 'Male':
    filename = segment + 'params_M.dat'
elif gender == 'Female':
    filename = segment + 'params_F.dat'
else:
    print('This is a program to simulate sex-specific transport along segments of rat nephron!')

cell = compute(int(N), filename, method, int(Ncell), diabete)

# N=int(N)

# file=open(cell[0].sex+cell[0].segment+'_potential_gradient_Lumen_Cell.txt','w')
# for j in range(1,N):
# 	file.write(str(cell[j-1].ep[0]-cell[j-1].ep[1])+'\n')
# file.close()
#
# for i in range(NS):
# 	file=open(cell[0].sex+cell[0].segment+'_con_of_'+solute[i]+'_in_Lumen.txt','w')
# 	for j in range(1,N):
# 		file.write(str(cell[j-1].conc[i,0])+'\n')
# 	file.close()

for n in range(NS):
    file = open(cell[0][0].sex + cell[0][0].segment + '_con_of_' + solute[n] + '_in_cell.txt', 'w')
    for i in range(Ncell):

        for j in range(N):
            file.write(str(cell[i][j].conc[n, 1]) + ' ')
        file.write('\n')
    file.close()

for n in range(NS):
    file = open(cell[0][0].sex + cell[0][0].segment + '_con_of_' + solute[n] + '_in_lumen.txt', 'w')
    for i in range(Ncell):

        for j in range(N):
            file.write(str(cell[i][j].conc[n, 0]) + ' ')
        file.write('\n')
    file.close()

for n in range(NS):
    file = open(cell[0][0].sex + cell[0][0].segment + '_pressure' + '_in_cell.txt', 'w')
    for i in range(Ncell):

        for j in range(N):
            file.write(str(cell[i][j].pres[1]) + ' ')
        file.write('\n')
    file.close()

for n in range(NS):
    file = open(cell[0][0].sex + cell[0][0].segment + '_pressure' + '_in_lumen.txt', 'w')
    for i in range(Ncell):

        for j in range(N):
            file.write(str(cell[i][j].pres[0]) + ' ')
        file.write('\n')
    file.close()

file_cell = open(cell[0][0].sex + cell[0][0].segment + '_osmolality_in_Cell.txt', 'w')
file_lumen = open(cell[0][0].sex + cell[0][0].segment + '_osmolality_in_Lumen.txt', 'w')
for i in range(Ncell):

    for j in range(N):
        osm_l = 0
        osm_c = 0

        for n in range(NS):
            osm_l = osm_l + cell[i][j].conc[n, 0]
            osm_c = osm_c + cell[i][j].conc[n, 1]

        file_lumen.write(str(osm_l) + ' ')
        file_cell.write(str(osm_c) + ' ')
    file_lumen.write('\n')
    file_cell.write('\n')
file_lumen.close()
file_cell.close()

file = open(cell[0][0].sex + cell[0][0].segment + '_waterflow' + '_in_lumen.txt', 'w')
for i in range(Ncell):

    for j in range(N):
        file.write(str(cell[i][j].vol[0]) + ' ')
    file.write('\n')
file.close()

file = open(cell[0][0].sex + cell[0][0].segment + '_volume' + '_of_cell.txt', 'w')
for i in range(Ncell):

    for j in range(N):
        file.write(str(cell[i][j].vol[1]) + ' ')
    file.write('\n')
file.close()

for n in range(NS):
    filename1 = 'malePT_flux_of_' + solute[n] + '_lumen_cell.txt'
    file1 = open(filename1, 'w')
    filename2 = 'malePT_flux_of_water_lumen_cell.txt'
    file2 = open(filename2, 'w')
    filename3 = 'malePT_flux_of_' + solute[n] + '_cell_bath.txt'
    file3 = open(filename3, 'w')
    filename4 = 'malePT_flux_of_water_cell_bath.txt'
    file4 = open(filename4, 'w')
    filename5 = 'malePT_flux_of_' + solute[n] + '_cell_LIS.txt'
    file5 = open(filename5, 'w')
    filename6 = 'malePT_flux_of_water_cell_LIS.txt'
    file6 = open(filename6, 'w')
    for i in range(Ncell):
        for j in range(N):
            Jvol1, Jsol1 = flux.compute_fluxes(cell[i][j], i)
            file1.write(str(Jsol1[n][0][1]) + ' ')
            file2.write(str(Jvol1[0][1]) + ' ')
            file3.write(str(Jsol1[n][1][5]) + ' ')
            file4.write(str(Jvol1[1][5]) + ' ')
            file5.write(str(Jsol1[n][1][4]) + ' ')
            file6.write(str(Jvol1[1][4]) + ' ')
        file1.write('\n')
        file2.write('\n')
        file3.write('\n')
        file4.write('\n')
        file5.write('\n')
        file6.write('\n')
    file1.close
    file2.close
    file3.close
    file4.close
    file5.close
    file6.close
for i in range(Ncell):
    for j in range(N):
        cell[i][j].area[4][5] = 0.02 * max(cell[i][j].vol[4] / cell[i][j].volref[4], 1.0)
        cell[i][j].area[5][4] = cell[i][j].area[4][5]

        jvol = water.compute_water_fluxes(cell[i][j])
        jsol, delmu = electrochemical.compute_ecd_fluxes(cell[i][j], jvol)

        for t in range(len(cell[i][j].trans)):
            transporter_type = cell[i][j].trans[t].type
            memb_id = cell[i][j].trans[t].membrane_id

            if transporter_type == 'SGLT1':
                solute_id, fluxs = glucose.sglt1(cell[i][j], cell[i][j].ep, memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]]+str(memb_id[0]) + str(memb_id[1]) + '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'SGLT2':
                solute_id, fluxs = glucose.sglt2(cell[i][j], cell[i][j].ep, memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]]+str(memb_id[0]) + str(memb_id[1]) + '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'GLUT1':
                solute_id, fluxs = glucose.glut1(cell[i][j], cell[i][j].ep, memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len([solute_id])):
                    file = open(
                        cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[solute_id] + str(
                            memb_id[0]) + str(memb_id[1]) +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs) + '\n')
            elif transporter_type == 'GLUT2':
                solute_id, fluxs = glucose.glut2(cell[i][j], cell[i][j].ep, memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len([solute_id])):
                    file = open(
                        cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[solute_id] + str(
                            memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs) + '\n')
            elif transporter_type == 'NHE3':
                solute_id, fluxs = NHE3.nhe3(cell[i][j], cell[i][j].ep, memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]]+str(memb_id[0]) + str(memb_id[1]) + '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'NaKATPase':
                solute_id, fluxs = ATPase.nakatpase(cell[i][j], cell[i][j].ep, memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(
                        cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[solute_id[k]] + str(
                            memb_id[0]) + str(memb_id[1]) + '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')

            elif transporter_type == 'HATPase':
                solute_id, fluxs = ATPase.hatpase(cell[i][j], cell[i][j].ep, memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]]+str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'NKCC2A':
                solute_id, fluxs = NKCC.nkcc2(cell[i][j], memb_id, cell[i][j].trans[t].act, cell[i][j].area, 'A')
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]]+str(memb_id[0]) + str(memb_id[1]) + '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'NKCC2B':
                solute_id, fluxs = NKCC.nkcc2(cell[i][j], memb_id, cell[i][j].trans[t].act, cell[i][j].area, 'B')
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'NKCC2F':
                solute_id, fluxs = NKCC.nkcc2(cell[i][j], memb_id, cell[i][j].trans[t].act, cell[i][j].area, 'F')
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'KCC4':
                solute_id, fluxs = KCC.kcc4(cell[i][j].conc, memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'ENaC':
                solute_id, fluxs = ENaC.ENaC(cell[i][j], j, memb_id, cell[i][j].trans[t].act, cell[i][j].area, jvol)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'NCC':
                solute_id, fluxs = NCC.NCC(cell[i][j], j, memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'Pendrin':
                solute_id, fluxs = Pendrin.Pendrin(cell[i][j], memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'AE1':
                solute_id, fluxs = AE1.AE1(cell[i][j], memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'HKATPase':
                solute_id, fluxs = ATPase.hkatpase(cell[i][j], memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'NHE1':
                solute_id, fluxs = NHE1.NHE1(cell[i][j], memb_id, cell[i][j].trans[t].act, cell[i][j].area)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            elif transporter_type == 'NKCC1':
                solute_id, fluxs = NKCC.nkcc1(cell[i][j], memb_id, cell[i][j].trans[t].act, delmu)
                for k in range(len(solute_id)):
                    file = open(cell[i][j].sex + '_' + cell[i][j].segment + '_' + transporter_type + '_' + solute[
                        solute_id[k]] +str(memb_id[0]) + str(memb_id[1])+ '.txt', 'a')
                    file.write(str(fluxs[k]) + '\n')
            else:
                print('What is this?', transporter_type)


for i in range(Ncell):
    for j in range(N):
        cell[i][j].area[4][5] = 0.02 * max(cell[i][j].vol[4] / cell[i][j].volref[4], 1.0)
        cell[i][j].area[5][4] = cell[i][j].area[4][5]

        jvol = water.compute_water_fluxes(cell[i][j])
        jsol, delmu = electrochemical.compute_ecd_fluxes(cell[i][j], jvol)

        jsol = cotransportwritein.compute_cotransport(cell[i][j], delmu, jsol)



                # for n in range(NS):
# 	file = open(cell[0][0].sex + cell[0][0].segment + '_flux_of_' + solute[n] + '_lumen_cell.txt', 'w')
# 	for i in range(Ncell):
# 		for j in range(N):
# 			Jvol1, Jsol1 = flux.compute_fluxes(cell[i][j], i)
# 			file.write(str(Jsol1[n][0][1])+',')
# 		file.write('\n')
# 	file.close()
#
#
# file = open(cell[0][0].sex + cell[0][0].segment + '_flux_of_water_lumen_cell.txt', 'w')
# for i in range(Ncell):
# 	for j in range(N):
# 		Jvol1, Jsol1 = flux.compute_fluxes(cell[i][j], i)
# 		file.write(str(Jvol1[0][1])+',')
# 	file.write('\n')
# file.close()
#
#
# for n in range(NS):
# 	file = open(cell[0][0].sex + cell[0][0].segment + '_flux_of_' + solute[n] + '_cell_bath.txt', 'w')
# 	for i in range(Ncell):
# 		for j in range(N):
# 			Jvol1, Jsol1 = flux.compute_fluxes(cell[i][j], i)
# 			file.write(str(Jsol1[n][1][5])+',')
# 		file.write('\n')
# 	file.close()
#
#
# file = open(cell[0][0].sex + cell[0][0].segment + '_flux_of_water_cell_bath.txt', 'w')
# for i in range(Ncell):
# 	for j in range(N):
# 		Jvol1, Jsol1 = flux.compute_fluxes(cell[i][j], i)
# 		file.write(str(Jvol1[1][5])+',')
# 	file.write('\n')
# file.close()
#
# for n in range(NS):
# 	file = open(cell[0][0].sex + cell[0][0].segment + '_flux_of_' + solute[n] + '_cell_LIS.txt', 'w')
# 	for i in range(Ncell):
# 		for j in range(N):
# 			Jvol1, Jsol1 = flux.compute_fluxes(cell[i][j], i)
# 			file.write(str(Jsol1[n][1][4])+',')
# 		file.write('\n')
# 	file.close()
#
#
# file = open(cell[0][0].sex + cell[0][0].segment + '_flux_of_water_cell_LIS.txt', 'w')
# for i in range(Ncell):
# 	for j in range(N):
# 		Jvol1, Jsol1 = flux.compute_fluxes(cell[i][j], i)
# 		file.write(str(Jvol1[1][4])+',')
# 	file.write('\n')
# file.close()

# for i in range(NS):
# 	file=open(cell[0].sex+cell[0].segment+'_con_of_'+solute[i]+'_in_Cell.txt','w')
# 	for j in range(1,N):
# 		file.write(str(cell[j-1].conc[i,1])+','+'\n')
# 	file.close()
# for i in range(NS):
# 	file=open(cell[0].sex+cell[0].segment+'_con_of_'+solute[i]+'_in_Bath.txt','w')
# 	for j in range(1,N):
# 		file.write(str(cell[j-1].conc[i,5])+'\n')
# 	file.close()
#
# file=open(cell[0].sex+cell[0].segment+'_water_volume_in_Lumen.txt','w')
# for j in range(1,N):
# 	file.write(str(cell[j-1].vol[0]*cw)+'\n')
# file.close()
# file=open(cell[0].sex+cell[0].segment+'_water_volume_in_Cell.txt','w')
# for j in range(1,N):
# 	file.write(str(cell[j-1].vol[1]*cw)+'\n')
# file.close()
#
# file=open(cell[0].sex+cell[0].segment+'_pH_in_Lumen.txt','w')
# for j in range(1,N):
# 	file.write(str(-np.log(cell[j-1].conc[11,0]/1000)/np.log(10))+'\n')
# file.close()
#
# file=open(cell[0].sex+cell[0].segment+'_pressure_in_cell.txt','w')
# for j in range(1,N):
# 	file.write(str(cell[j-1].pres[1])+'\n')
# file.close()
#
# for i in range(NS):
# 	file=open(cell[0].sex+cell[0].segment+'_flow_of_'+solute[i]+'_in_Lumen.txt','w')
# 	for j in range(1,N):
# 		file.write(str(cell[j-1].conc[i,0]*cell[j-1].vol[0]*cw)+'\n')
# 	file.close()
# for i in range(NS):
# 	file=open(cell[0].sex+cell[0].segment+'_flow_of_'+solute[i]+'_in_Cell.txt','w')
# 	for j in range(1,N):
# 		file.write(str(cell[j-1].conc[i,1]*cell[j-1].vol[1]*cw)+'\n')
# 	file.close()
#
# file_lumen = open(cell[0].sex+cell[0].segment+'_osmolality_in_Lumen.txt','w')
# file_cell = open(cell[0].sex+cell[0].segment+'_osmolality_in_Cell.txt','w')
# file_bath = open(cell[0].sex+cell[0].segment+'_osmolality_in_Bath.txt','w')
# for j in range(1,N):
# 	osm_l = 0
# 	osm_c = 0
# 	osm_b = 0
# 	for i in range(NS):
# 		osm_l = osm_l +cell[j-1].conc[i,0]
# 		osm_c = osm_c +cell[j-1].conc[i,1]
# 		osm_b = osm_b +cell[j-1].conc[i,5]
#
# 	file_lumen.write(str(osm_l)+'\n')
# 	file_cell.write(str(osm_c)+'\n')
# 	file_bath.write(str(osm_b)+'\n')
# file_lumen.close()
# file_cell.close()
# file_bath.close()
#
# for j in range(1,N):
# 	cell[i][j].area[4][5] = 0.02*max(cell[i][j].vol[4]/cell[i][j].volref[4],1.0)
# 	cell[i][j].area[5][4] = cell[i][j].area[4][5]
#
# 	jvol = water.compute_water_fluxes(cell[i][j])
# 	jsol,delmu = electrochemical.compute_ecd_fluxes(cell[i][j],jvol)
#
#
# 	for i in range(len(cell[i][j].trans)):
# 		transporter_type = cell[i][j].trans[i].type
# 		memb_id = cell[i][j].trans[i].membrane_id
#
# 		if transporter_type == 'SGLT1':
# 			solute_id,fluxs = glucose.sglt1(cell[i][j],cell[i][j].ep,memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'SGLT2':
# 			solute_id,fluxs = glucose.sglt2(cell[i][j],cell[i][j].ep,memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'GLUT1':
# 			solute_id,fluxs=glucose.glut1(cell[i][j],cell[i][j].ep,memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len([solute_id])):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id]+str(memb_id[0])+str(memb_id[1])+'.txt','a')
# 				file.write(str(fluxs)+'\n')
# 		elif transporter_type == 'GLUT2':
# 			solute_id,fluxs=glucose.glut2(cell[i][j],cell[i][j].ep,memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len([solute_id])):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id]+str(memb_id[0])+str(memb_id[1])+'.txt','a')
# 				file.write(str(fluxs)+'\n')
# 		elif transporter_type == 'NHE3':
# 			solute_id,fluxs=NHE3.nhe3(cell[i][j],cell[i][j].ep,memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'NaKATPase':
# 			solute_id,fluxs=ATPase.nakatpase(cell[i][j],cell[i][j].ep,memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+str(memb_id[0])+str(memb_id[1])+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
#
# 		elif transporter_type == 'HATPase':
# 			solute_id,fluxs=ATPase.hatpase(cell[i][j],cell[i][j].ep,memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'NKCC2A':
# 			solute_id,fluxs=NKCC.nkcc2(cell[i][j],memb_id,cell[i][j].trans[i].act,cell[i][j].area,'A')
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'NKCC2B':
# 			solute_id,fluxs=NKCC.nkcc2(cell[i][j],memb_id,cell[i][j].trans[i].act,cell[i][j].area,'B')
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'NKCC2F':
# 			solute_id,fluxs=NKCC.nkcc2(cell[i][j],memb_id,cell[i][j].trans[i].act,cell[i][j].area,'F')
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'KCC4':
# 			solute_id,fluxs=KCC.kcc4(cell[i][j].conc,memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'ENaC':
# 			solute_id,fluxs=ENaC.ENaC(cell[i][j],j,memb_id,cell[i][j].trans[i].act,cell[i][j].area,jvol)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'NCC':
# 			solute_id,fluxs=NCC.NCC(cell[i][j],j,memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'Pendrin':
# 			solute_id,fluxs=Pendrin.Pendrin(cell[i][j],memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type =='AE1':
# 			solute_id,fluxs=AE1.AE1(cell[i][j],memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'HKATPase':
# 			solute_id,fluxs=ATPase.hkatpase(cell[i][j],memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'NHE1':
# 			solute_id,fluxs=NHE1.NHE1(cell[i][j],memb_id,cell[i][j].trans[i].act,cell[i][j].area)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		elif transporter_type == 'NKCC1':
# 			solute_id,fluxs=NKCC.nkcc1(cell[i][j],memb_id,cell[i][j].trans[i].act,delmu)
# 			for k in range(len(solute_id)):
# 				file = open(cell[i][j].sex+'_'+cell[i][j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'.txt','a')
# 				file.write(str(fluxs[k])+'\n')
# 		else:
# 			print('What is this?',transporter_type)
#
#
# file_Na_flux = open(cell[0].sex+'_'+cell[0].segment+'_Na_apical_flux.txt','w')
# file_K_flux = open(cell[0].sex+'_'+cell[0].segment+'_K_apical_flux.txt','w')
# file_NH4_flux = open(cell[0].sex+'_'+cell[0].segment+'_NH4_apical_flux.txt','w')
# file_H_flux = open(cell[0].sex+'_'+cell[0].segment+'_H_apical_flux.txt','w')
# file_Cl_flux = open(cell[0].sex+'_'+cell[0].segment+'_Cl_apical_flux.txt','w')
# file_HCO3_flux = open(cell[0].sex+'_'+cell[0].segment+'_HCO3_apical_flux.txt','w')
# file_HPO4_flux = open(cell[0].sex+'_'+cell[0].segment+'_HPO4_apical_flux.txt','w')
# file_H2PO4_flux = open(cell[0].sex+'_'+cell[0].segment+'_H2PO4_apical_flux.txt','w')
# file_HCO2_flux = open(cell[0].sex+'_'+cell[0].segment+'_HCO2_apical_flux.txt','w')
# file_Na_flux_para = open(cell[0].sex+'_'+cell[0].segment+'_Na_para_flux.txt','w')
# file_K_flux_para = open(cell[0].sex+'_'+cell[0].segment+'_K_para_flux.txt','w')
# file_NH4_flux_para = open(cell[0].sex+'_'+cell[0].segment+'_NH4_para_flux.txt','w')
# file_H_flux_para = open(cell[0].sex+'_'+cell[0].segment+'_H_para_flux.txt','w')
# file_Cl_flux_para = open(cell[0].sex+'_'+cell[0].segment+'_Cl_para_flux.txt','w')
# file_HCO3_flux_para = open(cell[0].sex+'_'+cell[0].segment+'_HCO3_para_flux.txt','w')
# file_HPO4_flux_para = open(cell[0].sex+'_'+cell[0].segment+'_HPO4_para_flux.txt','w')
# file_H2PO4_flux_para = open(cell[0].sex+'_'+cell[0].segment+'_H2PO4_para_flux.txt','w')
# file_HCO2_flux_para = open(cell[0].sex+'_'+cell[0].segment+'_HCO2_para_flux.txt','w')
# file_Na_flux_alpha = open(cell[0].sex+'_'+cell[0].segment+'_Na_alpha_flux.txt','w')
# file_K_flux_alpha = open(cell[0].sex+'_'+cell[0].segment+'_K_alpha_flux.txt','w')
# file_NH4_flux_alpha = open(cell[0].sex+'_'+cell[0].segment+'_NH4_alpha_flux.txt','w')
# file_H_flux_alpha = open(cell[0].sex+'_'+cell[0].segment+'_H_alpha_flux.txt','w')
# file_Cl_flux_alpha = open(cell[0].sex+'_'+cell[0].segment+'_Cl_alpha_flux.txt','w')
# file_HCO3_flux_alpha = open(cell[0].sex+'_'+cell[0].segment+'_HCO3_alpha_flux.txt','w')
# file_HPO4_flux_alpha = open(cell[0].sex+'_'+cell[0].segment+'_HPO4_alpha_flux.txt','w')
# file_H2PO4_flux_alpha = open(cell[0].sex+'_'+cell[0].segment+'_H2PO4_alpha_flux.txt','w')
# file_HCO2_flux_alpha = open(cell[0].sex+'_'+cell[0].segment+'_HCO2_alpha_flux.txt','w')
# file_Na_flux_beta = open(cell[0].sex+'_'+cell[0].segment+'_Na_beta_flux.txt','w')
# file_K_flux_beta = open(cell[0].sex+'_'+cell[0].segment+'_K_beta_flux.txt','w')
# file_NH4_flux_beta = open(cell[0].sex+'_'+cell[0].segment+'_NH4_beta_flux.txt','w')
# file_H_flux_beta = open(cell[0].sex+'_'+cell[0].segment+'_H_beta_flux.txt','w')
# file_Cl_flux_beta = open(cell[0].sex+'_'+cell[0].segment+'_Cl_beta_flux.txt','w')
# file_HCO3_flux_beta = open(cell[0].sex+'_'+cell[0].segment+'_HCO3_beta_flux.txt','w')
# file_HPO4_flux_beta = open(cell[0].sex+'_'+cell[0].segment+'_HPO4_beta_flux.txt','w')
# file_H2PO4_flux_beta = open(cell[0].sex+'_'+cell[0].segment+'_H2PO4_beta_flux.txt','w')
# file_HCO2_flux_beta = open(cell[0].sex+'_'+cell[0].segment+'_HCO2_beta_flux.txt','w')
#
# file_K_flux_total = open(cell[0].sex+'_'+cell[0].segment+'_K_total_flux.txt','w')
#
# for j in range(1,N):
# 	jsol=np.zeros([15,6,6])
# 	jvol,jsol = flux.compute_fluxes(cell[i][j],j)
# 	file_Na_flux.write(str(jsol[0,0,1])+'\n')
# 	file_K_flux.write(str(jsol[1,0,1])+'\n')
# 	file_NH4_flux.write(str(jsol[10,0,1])+'\n')
# 	file_H_flux.write(str(jsol[11,0,1])+'\n')
# 	file_Cl_flux.write(str(jsol[2,0,1])+'\n')
# 	file_HCO3_flux.write(str(jsol[3,0,1])+'\n')
# 	file_HPO4_flux.write(str(jsol[6,0,1])+'\n')
# 	file_H2PO4_flux.write(str(jsol[7,0,1])+'\n')
# 	file_HCO2_flux.write(str(jsol[12,0,1])+'\n')
# 	file_Na_flux_para.write(str(jsol[0,0,4])+'\n')
# 	file_K_flux_para.write(str(jsol[1,0,4])+'\n')
# 	file_NH4_flux_para.write(str(jsol[10,0,4])+'\n')
# 	file_H_flux_para.write(str(jsol[11,0,4])+'\n')
# 	file_Cl_flux_para.write(str(jsol[2,0,4])+'\n')
# 	file_HCO3_flux_para.write(str(jsol[3,0,4])+'\n')
# 	file_HPO4_flux_para.write(str(jsol[6,0,4])+'\n')
# 	file_H2PO4_flux_para.write(str(jsol[7,0,4])+'\n')
# 	file_HCO2_flux_para.write(str(jsol[12,0,4])+'\n')
# 	file_Na_flux_alpha.write(str(jsol[0,0,2])+'\n')
# 	file_K_flux_alpha.write(str(jsol[1,0,2])+'\n')
# 	file_NH4_flux_alpha.write(str(jsol[10,0,2])+'\n')
# 	file_H_flux_alpha.write(str(jsol[11,0,2])+'\n')
# 	file_Cl_flux_alpha.write(str(jsol[2,0,2])+'\n')
# 	file_HCO3_flux_alpha.write(str(jsol[3,0,2])+'\n')
# 	file_HPO4_flux_alpha.write(str(jsol[6,0,2])+'\n')
# 	file_H2PO4_flux_alpha.write(str(jsol[7,0,2])+'\n')
# 	file_HCO2_flux_alpha.write(str(jsol[12,0,2])+'\n')
# 	file_Na_flux_beta.write(str(jsol[0,0,3])+'\n')
# 	file_K_flux_beta.write(str(jsol[1,0,3])+'\n')
# 	file_NH4_flux_beta.write(str(jsol[10,0,3])+'\n')
# 	file_H_flux_beta.write(str(jsol[11,0,3])+'\n')
# 	file_Cl_flux_beta.write(str(jsol[2,0,3])+'\n')
# 	file_HCO3_flux_beta.write(str(jsol[3,0,3])+'\n')
# 	file_HPO4_flux_beta.write(str(jsol[6,0,3])+'\n')
# 	file_H2PO4_flux_beta.write(str(jsol[7,0,3])+'\n')
# 	file_HCO2_flux_beta.write(str(jsol[12,0,3])+'\n')
# 	file_K_flux_total.write(str(jsol[1,0,1]+jsol[1,0,2]+jsol[1,0,3]+jsol[1,0,4])+'\n')
# file_Na_flux.close()
# file_K_flux.close()
# file_NH4_flux.close()
# file_H_flux.close()
# file_Cl_flux.close()
# file_HCO3_flux.close()
# file_HPO4_flux.close()
# file_H2PO4_flux.close()
# file_HCO2_flux.close()
# file_Na_flux_para.close()
# file_K_flux_para.close()
# file_NH4_flux_para.close()
# file_H_flux_para.close()
# file_Cl_flux_para.close()
# file_HCO3_flux_para.close()
# file_HPO4_flux_para.close()
# file_H2PO4_flux_para.close()
# file_HCO2_flux_para.close()
# file_Na_flux_alpha.close()
#
# file_K_flux_alpha.close()
# file_NH4_flux_alpha.close()
# file_H_flux_alpha.close()
# file_Cl_flux_alpha.close()
# file_HCO3_flux_alpha.close()
# file_HPO4_flux_alpha.close()
# file_H2PO4_flux_alpha.close()
# file_HCO2_flux_alpha.close()
# file_Na_flux_beta.close()
# file_K_flux_beta.close()
# file_NH4_flux_beta.close()
# file_H_flux_beta.close()
# file_Cl_flux_beta.close()
# file_HCO3_flux_beta.close()
# file_HPO4_flux_beta.close()
# file_H2PO4_flux_beta.close()
# file_HCO2_flux_beta.close()
# file_K_flux_total.close()
