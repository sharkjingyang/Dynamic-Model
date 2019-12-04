from driver import compute
from values import *
from defs import *
import electrochemical 
import water
import glucose
import cotransport
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

solute = ['Na','K','Cl','HCO3','H2CO3','CO2','HPO4','H2PO4','urea','NH3','NH4','H','HCO2','H2CO2','glu']
compart = ['Lumen','Cell','ICA','ICB','LIS','Bath']
cw=Vref*60e6

segments=['PT','S3','SDL','mTAL','cTAL','MD','DCT','CNT','CCD','OMCD','IMCD']

gender=input('Which gender do you want to simulate? (Male or Female) ')
begin=input('Which segment do you want to start with? ')
end=input('Which segment do you want to stop with? ')
diabete=input('Dose it have diabete? (Y/N) ')

begin_index=segments.index(begin)
end_index=segments.index(end)

for segment in segments[begin_index:end_index+1]:
	if gender == 'Male':
		filename = segment+'params_M.dat'
	elif gender == 'Female':
		filename = segment+'params_F.dat'
	else:
		print('Did you choose correct segments?')

	if segment == 'PT':
		N = 176
	elif segment == 'S3':
		N = 25
	elif segment == 'MD':
		N = 2
	else:
		N = 200

	if segment == 'PT' or segment == 'SDL' or segment == 'mTAL' or segment == 'DCT':
		method = 'Broyden'
	else:
		method = 'Newton'
	cell = compute(N,filename,method,diabete)
	for i in range(NS):
		file=open(cell[0].sex+cell[0].segment+'_con_of_'+solute[i]+'_in_Lumen.txt','w')
		for j in range(1,N):
			file.write(str(cell[j-1].conc[i,0])+'\n')
		file.close()
	for i in range(NS):
		file=open(cell[0].sex+cell[0].segment+'_con_of_'+solute[i]+'_in_Cell.txt','w')
		for j in range(1,N):
			file.write(str(cell[j-1].conc[i,1])+'\n')
		file.close()
	for i in range(NS):
		file=open(cell[0].sex+cell[0].segment+'_con_of_'+solute[i]+'_in_Bath.txt','w')
		for j in range(1,N):
			file.write(str(cell[j-1].conc[i,5])+'\n')
		file.close()

	file=open(cell[0].sex+cell[0].segment+'_water_volume_in_Lumen.txt','w')
	for j in range(1,N):
		file.write(str(cell[j-1].vol[0]*cw)+'\n')
	file.close()
	file=open(cell[0].sex+cell[0].segment+'_water_volume_in_Cell.txt','w')
	for j in range(1,N):
		file.write(str(cell[j-1].vol[1]*cw)+'\n')
	file.close()

	for i in range(NS):
		file=open(cell[0].sex+cell[0].segment+'_flow_of_'+solute[i]+'_in_Lumen.txt','w')
		for j in range(1,N):
			file.write(str(cell[j-1].conc[i,0]*cell[j-1].vol[0]*cw)+'\n')
		file.close()
	for i in range(NS):
		file=open(cell[0].sex+cell[0].segment+'_flow_of_'+solute[i]+'_in_Cell.txt','w')
		for j in range(1,N):
			file.write(str(cell[j-1].conc[i,1]*cell[j-1].vol[1]*cw)+'\n')
		file.close()

	file=open(cell[0].sex+cell[0].segment+'_pH_in_Lumen.txt','w')
	for j in range(1,N):
		file.write(str(-np.log(cell[j-1].conc[11,0]/1000)/np.log(10))+'\n')
	file.close()

	print(segment+' finished')