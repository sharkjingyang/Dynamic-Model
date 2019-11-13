from defs import *
import copy
import set_params 
import flux
import numpy as np
import equations
import electrochemical
import water
from values import *
import Newton
import matplotlib.pyplot as plt
from scipy.optimize import newton_krylov, broyden1, anderson, fsolve, newton
import timeit
import boundaryBath

def compute(N,filename,method, diabete='N'):

	start=timeit.default_timer()
	#N=200

	cell = [membrane() for i in range(N)]

	if diabete == 'N':
		for i in range(N):
			cell[i].diabete = 'No'
	elif diabete == 'Y':
		for i in range(N):
			cell[i].diabete = 'Yes'
	else:
		print('What is diabete status?')

	water_trans = 0
	na_trans = 0
	water_para = 0
	na_para = 0

	#filename=input('Choose a data file: ')

	#method = input('Choose a method: Newton or Broyden: ')

	for i in range(N):
		set_params.read_params(cell[i],filename,i)
		#cell[i].area_init[4][5] = 0.02
		#cell[i].area[4][5] = cell[i].area_init[4][5]*max(cell[i].vol[4]/cell[i].volref[4],1.0)
		#cell[i].area[5][4] = cell[i].area[4][5]
	

		boundaryBath.boundaryBath(cell[i],i)
	cell[0].vol[0]=cell[0].vol[0]*1.1
	K=cell[0].conc[14][0]*cell[0].vol[0]*6000

	if cell[0].segment == 'PT':
		if cell[0].diabete == 'Yes':
			cell[0].vol[0] = 0.0075

	if cell[0].segment == 'S3':
		inputfile = open('PToutlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
			cell[0].conc[i,1] = float(conclist[1])
			cell[0].conc[i,4] = float(conclist[2])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		cell[0].vol[1] = float(vollist[1])
		cell[0].vol[4] = float(vollist[2])
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		cell[0].ep[1] = float(eplist[1])
		cell[0].ep[4] = float(eplist[2])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])

	if cell[0].segment == 'SDL':
		inputfile = open('S3outlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])
		for i in range(N):
			cell[i].conc[:,1] = cell[i].conc[:,5]
			cell[i].conc[:,4] = cell[i].conc[:,5]

	if cell[0].segment == 'mTAL':
		inputfile = open('SDLoutlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])

	if cell[0].segment == 'cTAL':
		inputfile = open('mTALoutlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])

	if cell[0].segment == 'MD':
		inputfile = open('cTALoutlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])	

	if cell[0].segment == 'DCT':
		inputfile = open('cTALoutlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])

	if cell[0].segment == 'CNT':
		inputfile = open('DCToutlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		for k in range(N):
			cell[k].vol_init[0] = cell[0].vol[0]
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])

	if cell[0].segment == 'CCD':
		inputfile = open('CNToutlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		for k in range(N):
			cell[k].vol_init[0] = cell[0].vol[0]
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])

	if cell[0].segment == 'OMCD':
		inputfile = open('CCDoutlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		for k in range(N):
			cell[k].vol_init[0] = cell[0].vol[0]
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])

	if cell[0].segment == 'IMCD':
		inputfile = open('OMCDoutlet'+cell[0].sex+'.txt','r')
		for i in range(NS):
			line = inputfile.readline()
			conclist = line.split(' ')
			cell[0].conc[i,0] = float(conclist[0])
		line_vol = inputfile.readline()
		vollist = line_vol.split(' ')
		cell[0].vol[0] = float(vollist[0])
		line_ep = inputfile.readline()
		eplist = line_ep.split(' ')
		cell[0].ep[0] = float(eplist[0])
		line_pres = inputfile.readline()
		preslist = line_pres.split(' ')
		cell[0].pres[0] = float(preslist[0])

	for i in range(N-1):
		print(i+1)
		celln = copy.deepcopy(cell[i+1])
		dx = 1.0e-3
		if cell[0].segment == 'PT' or cell[0].segment == 'S3' or cell[0].segment =='SDL' or cell[0].segment == 'mTAL' or cell[0].segment == 'cTAL' or cell[0].segment == 'MD' or cell[0].segment == 'DCT' or cell[0].segment == 'IMCD':
			x = np.zeros(3*NS+7)

			x[0:NS] = cell[i].conc[:,0]
			x[NS:2*NS] = cell[i].conc[:,1]
			x[2*NS:3*NS] = cell[i].conc[:,4]
	
			x[3*NS] = cell[i].vol[0]
			x[3*NS+1] = cell[i].vol[1]
			x[3*NS+2] = cell[i].vol[4]
 
			x[3*NS+3] = cell[i].ep[0]
			x[3*NS+4] = cell[i].ep[1]
			x[3*NS+5] = cell[i].ep[4]
	
			x[3*NS+6] = cell[i].pres[0]

		elif cell[0].segment == 'CNT' or cell[0].segment == 'CCD' or cell[0].segment == 'OMCD':
			x=np.zeros(5*NS+11)
			for j in range(15):
				x[5*j]=cell[i].conc[j,0]
				x[5*j+1]=cell[i].conc[j,1]
				x[5*j+2]=cell[i].conc[j,2]
				x[5*j+3]=cell[i].conc[j,3]
				x[5*j+4]=cell[i].conc[j,4]
			for j in range(NC-1):
				x[5*NS+j]=cell[i].vol[j]
				x[5*NS+5+j]=cell[i].ep[j]
			x[5*NS+10]=cell[i].pres[0]
	
		else:#if cell[0].segment == 'SDL':
			x = np.zeros(NS+3)
			x[0:NS] = cell[i].conc[:,0]
			x[NS] = cell[i].vol[0]
			x[NS+1] = cell[i].pres[0]
			x[NS+2] = -1 
	
	
		equations.conservation_init (cell[i],cell[i+1],celln,dx)
		fvec = equations.conservation_eqs (x,i)
		#print(fvec)

		if method == 'Newton':
			sol = Newton.newton(equations.conservation_eqs,x,i,cell[i].segment)
		if method == 'Broyden':
			sol = Newton.broyden(equations.conservation_eqs,x,i,cell[i].segment)
	
		if cell[0].segment == 'PT' or cell[0].segment == 'S3' or cell[0].segment =='SDL' or cell[0].segment == 'mTAL' or cell[0].segment == 'cTAL' or cell[0].segment == 'MD' or cell[0].segment == 'DCT' or cell[0].segment == 'IMCD':
			cell[i+1].conc[:,0] = sol[0:NS]
			cell[i+1].conc[:,1] = sol[NS:NS*2]
			cell[i+1].conc[:,4] = sol[NS*2:NS*3]

			cell[i+1].vol[0] = sol[3*NS]
			cell[i+1].vol[1] = sol[3*NS+1]
			cell[i+1].vol[4] = sol[3*NS+2]
	
			cell[i+1].ep[0] = sol[3*NS+3]
			cell[i+1].ep[1] = sol[3*NS+4]
			cell[i+1].ep[4] = sol[3*NS+5]
	
			cell[i+1].pres[0] = sol[3*NS+6]
		elif cell[0].segment == 'CNT' or cell[0].segment == 'CCD' or cell[0].segment == 'OMCD':
			for j in range(15):
				cell[i+1].conc[j,0] = sol[5*j]
				cell[i+1].conc[j,1] = sol[5*j+1] 
				cell[i+1].conc[j,2] = sol[5*j+2]
				cell[i+1].conc[j,3] = sol[5*j+3]
				cell[i+1].conc[j,4] = sol[5*j+4]

			for j in range(NC-1):
				cell[i+1].vol[j] = sol[5*NS+j]
				cell[i+1].ep[j] = sol[5*NS+5+j]
	
			cell[i+1].pres[0] = sol[5*NS+10]		
	
		print('\n')

#================================OUTPUT IN TO FILE================================

	if cell[0].segment == 'PT':
		file=open('PToutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4],cell[N-1].conc[j,5]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))
		file.close()

	elif cell[0].segment == 'S3':
		file=open('S3outlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))
		file.close()
	elif cell[0].segment == 'SDL':
		file=open('SDLoutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))
		file.close()
	elif cell[0].segment == 'mTAL':
		file=open('mTALoutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))
		file.close()
	elif cell[0].segment == 'cTAL':
		file=open('cTALoutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4],cell[N-1].conc[j,5]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))
		file.close()
	elif cell[0].segment == 'MD':
		file=open('MDoutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))
		file.close()
	elif cell[0].segment == 'DCT':
		file=open('DCToutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))
		file.close()
	elif cell[0].segment == 'CNT':
		file=open('CNToutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,2],cell[N-1].conc[j,3],cell[N-1].conc[j,4]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[2],cell[N-1].vol[3],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[2],cell[N-1].ep[3],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))		
		file.close()
	elif cell[0].segment == 'CCD':
		file=open('CCDoutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,2],cell[N-1].conc[j,3],cell[N-1].conc[j,4]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[2],cell[N-1].vol[3],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[2],cell[N-1].ep[3],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))	
		file.close()
	elif cell[0].segment == 'OMCD':
		file=open('OMCDoutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,2],cell[N-1].conc[j,3],cell[N-1].conc[j,4]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[2],cell[N-1].vol[3],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[2],cell[N-1].ep[3],cell[N-1].ep[4]))		
		file.write(str(cell[N-1].pres[0]))
		file.close()
	elif cell[0].segment == 'IMCD':
		file=open('IMCDoutlet'+cell[0].sex+'.txt','w')
		for j in range(NS):
			file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
		file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
		file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
		file.write(str(cell[N-1].pres[0]))
		file.close()
	

	number_of_cell = [i for i in range(1,200)]
	solute = ['Na','K','Cl','HCO3','H2CO3','CO2','HPO4','H2PO4','urea','NH3','NH4','H','HCO2','H2CO2','glu']
	compart = ['Lumen','Cell','ICA','ICB','LIS','Bath']
# 	for j in [0,1,4]:
# 		for k in range(NS):
# 			conc = [cell[i].conc[k,j] for i in range(1,200)]
# 			plt.figure(figsize=[10,10])
# 			plt.scatter(number_of_cell,conc)
# 			plt.hold(False)
# 			plt.savefig(solute[k]+'_'+'in'+'_'+compart[j])

# 	for j in [0,1,4]:
# 		for k in range(NS):
# 			flow = [cell[i].conc[k,j]*cell[i].vol[j] for i in range(1,200)]
# 			plt.plot(number_of_cell,flow)
# 			plt.hold(False)
# 			plt.savefig('flow_of'+'_'+solute[k]+'_'+'in'+'_'+compart[j])

# 	file = open('lastcellfromnewton.txt','a')
# 	for j in range(15):
# 		file.write(str(cell[199].conc[j][1]))
# 		file.write('\t')  
# 	for j in range(15):  
# 		file.write(str(cell[199].conc[j][4]))
# 		file.write('\t')
# 	file.close()
# 	plt.figure('cell',figsize=[10,4.8])
# 	dct_conc_cell_fortran = [11.02917,139.45103,6.64162,5.26464,0.00425,1.4987,9.05223,12.39641,10.74043,0.00491,1.50648,0.00022,0.00937,0.00007,1.14458]
# 	dct_conc_cell_python = [cell[199].conc[s,1] for s in range(NS)]
# 	plt.scatter(solute,dct_conc_cell_fortran)
# 	plt.scatter(solute,dct_conc_cell_python)
# 	plt.savefig('result_of_conc_in_cell_comparison_between_fortran_and_python')

# 	plt.figure('LIS',figsize=[10,4.8])
# 	dct_conc_lis_fortran = [142.92546,3.41531,113.76378,25.88607,0.00497,1.49894,2.86911,0.93458,8.50801,0.0025,0.18233,0.00005,0.20052,0.00006,0.86277]
# 	dct_conc_lis_python = [cell[199].conc[s,4] for s in range(NS)]
# 	plt.scatter(solute,dct_conc_lis_fortran)
# 	plt.scatter(solute,dct_conc_lis_python)
# 	plt.savefig('result_of_conc_in_LIS_comparison_between_fortran_and_python')

	stop=timeit.default_timer()
	print(stop-start)
	print('\n')

	return cell