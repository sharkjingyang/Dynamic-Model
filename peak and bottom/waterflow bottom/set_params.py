import re
from defs import *
from values import *

# pick out compartment IDs. E.g. given label=Area_Lumen_Cell, it would return
# (0,1) for (lumen, cell)
def get_interface_id(label):
	tmp = (label).split('_')
	if len(tmp)==3:  # only have two compartment IDs
		ind1,ind2 = compart_id[tmp[1]],compart_id[tmp[2]]
		return ind1, ind2
	elif len(tmp)==4:  # solute ID, followed by two compartment IDs
		sid,ind1,ind2 = solute_id[tmp[1]],compart_id[tmp[2]],compart_id[tmp[3]]
		return sid,ind1,ind2

# for coupled transpoters
# pick out solute IDs, compartment IDs, and coefficients
def get_coupled_id(label):
	tmp = (label).split('_')
#    print(tmp)
	sid1,sid2 = solute_id[tmp[3]],solute_id[tmp[4]]
	ind1,ind2 = compart_id[tmp[1]],compart_id[tmp[2]]
	if len(tmp)==5:  # only involves 2 solutes
		return ind1,ind2,sid1,sid2
	elif len(tmp)==6:  # involves 3 solutes
		sid3 = solute_id[tmp[5]]
		return ind1,ind2,sid1,sid2,sid3
	else:
		print("Wrong label",tmp)

# is str_short at the beginning of str_long?
# case insensitive
def compare_string_prefix(str_long,str_short):
	return (str_long.lower())[:len(str_short)] == str_short.lower()

def compare_sex(sex, cell):
	if sex.lower() == 'male' or sex.lower() == 'female':
		return cell.sex.lower() == sex.lower()
	else:
		return True

def read_params(cell,filename,j):
#    cell = membrane()
	#filename=input('Choose a file')
	#filename='cTALparams.dat'
	file = open(filename,'r')
	cell.segment=filename[0:-12]
	data = []
	line = file.readline()
	while (line):
		line = line.replace('\t',' ')
		terms = line.split(' ')
		if line[0][0]!='#':
			id = terms[0] #re.findall(r'[A-Za-z_]+', line)
			sex = id.split('_')[-1].lower()
			if compare_sex(sex, cell):
				id = id.replace('_male', '')
				id = id.replace('_female', '')
			else:
				line = file.readline()
				continue;
			# skip over the label, which may contain numbers like in HCO3
			first_space_pos = line.index(' ')
			num = re.findall(r'-?\d+\.?\d*[Ee]?[+-]?\d*', line[first_space_pos:len(line)])
			if num: # if this line is numerical param
				value = float(num[0])


			if id.lower() == "Sex".lower():
				find = re.findall("Female".lower(), terms[-1].lower())
				if find:
					cell.sex = "Female".lower()
			
			elif compare_string_prefix(id,"Diameter"):
				if cell.diabete == 'No':
					cell.diam = value
				elif cell.diabete == 'Yes':
					if cell.segment == 'PT' or cell.segment == 'S3':
						cell.diam = value*32/25
					elif cell.segment == 'SDL' or cell.segment == 'mTAL' or cell.segment == 'cTAL' or cell.segment == 'DCT' or cell.segment == 'CNT' or cell.segment == 'CCD' or cell.segment == 'OMCD':
						cell.diam = value*1.42
					else:
						cell.diam = value
				else:
					print('What is the diabete status?')
			elif compare_string_prefix(id,"Length"):
				if cell.diabete == 'No':
					cell.len = value
				elif cell.diabete == 'Yes':
					if cell.segment == 'PT' or cell.segment == 'S3':
						cell.len = value*1.28
					elif cell.segment == 'SDL' or cell.segment == 'mTAL' or cell.segment == 'cTAL' or cell.segment == 'DCT' or cell.segment == 'CNT' or cell.segment == 'CCD' or cell.segment == 'OMCD':
						cell.len = value*1.07
					else:
						cell.len = value
				else:
					print('What is the diabete status?')
			#elif compare_string_prefix(id,"Total"):
			#    cell.total = value
			elif compare_string_prefix(id,"Pressure"):
				cell.pres[0] = value

			elif compare_string_prefix(id,"pH"):
				for i in range(6):
					cell.pH[i] = num[i]
			elif compare_string_prefix(id,"total"):
				cell.total = value
			# surface area
			elif compare_string_prefix(id,"Area"):
				ind1,ind2 = get_interface_id(id)
				cell.area[ind1][ind2] = value
				cell.area[ind2][ind1] = value  # symmetry
				cell.area_init[ind1][ind2] = value
				cell.area_init[ind2][ind1] = value

			# water permeabilities
			elif compare_string_prefix(id,"Pf"):
				ind1,ind2 = get_interface_id(id)
				# Units of dimensional water flux (in 'value'): cm3/s/cm2 epith
				# Non-dimensional factor for water flux: (Pfref)*Vwbar*Cref
				# Calculate non-dimensional dLPV = Pf*Vwbar*Cref / (Pfref*Vwbar*Cref)
				# dLPV = Pf/Pfref
				cell.dLPV[ind1][ind2] = value/Pfref
				# symmetry
				cell.dLPV[ind2][ind1] = value/Pfref
				if cell.segment == 'SDL':
					if j>=0.46*cell.total:
						cell.dLPV[0,1]=0.00*cell.dLPV[0,1]
						cell.dLPV[0,4]=0.00*cell.dLPV[0,4]

				if cell.diabete == 'Yes':
					if cell.segment == 'CCD' or cell.segment == 'IMCD':
						cell.dLPV[0,1] = cell.dLPV[0,1]*1.4
						cell.dLPV[1,5] = cell.dLPV[1,5]*1.4
			
			# reflective coefficients
			elif compare_string_prefix(id,"sig"):
				sid,ind1,ind2 = get_interface_id(id)
				cell.sig[sid][ind1][ind2] = value
#                if sid==0 and ind1==0 and ind2==1:
#                    print('got sig[0][0][1]]',cell.sig[0][0][1])
				# symmetry
				cell.sig[sid][ind2][ind1] = value

			# membrane solute permeabilities
			elif compare_string_prefix(id,"perm"):
				sid,ind1,ind2 = get_interface_id(id)
				cell.h[sid][ind1][ind2] = value*1.0e-5/href
				# symmetry
				cell.h[sid][ind2][ind1] = value*1.0e-5/href
				# same basolateral around bath or LIS
				if ind1==1 and ind2==5:
					cell.h[sid][ind1][4] = value*1.0e-5/href
					cell.h[sid][4][ind1] = value*1.0e-5/href
				elif ind1==1 and ind2==4:
					cell.h[sid][ind1][5] = value*1.0e-5/href
					cell.h[sid][5][ind1] = value*1.0e-5/href
				elif ind1==2 and ind2==4:
					cell.h[sid][ind1][5] = value*1.0e-5/href
				elif ind1==3 and ind2==4:
					cell.h[sid][ind1][5] = value*1.0e-5/href
				if cell.segment == 'OMCD':
					cell.h[sid][0][3] = 0.0
					cell.h[sid][3][4] = 0.0
					cell.h[sid][3][5] = 0.0
				if cell.segment == 'IMCD':
					if cell.sex == 'male':
						if j>3*cell.total/4-1:
							cell.h[8,0,1] = 300.0*1.0e-5/href
					elif cell.sex == 'female':
						if j>2*cell.total/3-1:
							cell.h[8,0,1] = 300.0*1.0e-5/href
			# coupled transporters
			elif compare_string_prefix(id,"coupled"):
				# retrieve interface and solute id
				vals = get_coupled_id(id)
				newdLA = coupled_transport()
				newdLA.perm = value / (href*Cref)
				newdLA.membrane_id = [vals[0],vals[1]]
				coef = []  # retrieve coupling coefficients
#                print(num)
				for i in range(1,len(num)):
					coef.append(int(num[i]))
				newdLA.coef = coef
				newdLA.solute_id = vals[2:len(vals)]
				cell.dLA.append(newdLA)
				# same basolateral around bath or LIS
				#if vals[0]==1 and vals[1]==5:
				#    newdLA2 = coupled_transport()
				#    newdLA2.perm = newdLA.perm
				#    newdLA2.membrane_id = [1,4]
				#    newdLA2.coef = coef
				#    newdLA2.solute_id = vals[2:len(vals)]
				#    cell.dLA.append(newdLA2)
				#elif vals[0]==1 and vals[1]==4: 
				#    newdLA2 = coupled_transport()
				#    newdLA2.perm = newdLA.perm
				#    newdLA2.membrane_id = [1,5]
				#    newdLA2.coef = coef
				#    newdLA2.solute_id = vals[2:len(vals)]
				#    cell.dLA.append(newdLA2)

			# specific transporters
			elif compare_string_prefix(id,"transport"):
				tmp = (id).split('_')
				ind1,ind2 = compart_id[tmp[1]],compart_id[tmp[2]]
				newTransp = transporter()
				newTransp.membrane_id = [ind1,ind2]
				newTransp.type = tmp[3]
				if newTransp.type == 'Pendrin':
					newTransp.act = value/1400.0/(href*Cref)
				else:
					newTransp.act = value/(href*Cref)
				#print('transporter')
				#print(newTransp.membrane_id,newTransp.type,newTransp.act)
				cell.trans.append(newTransp)
				#if ind1==1 and ind2==5:
				#    newTransp2 = transporter()
				#    newTransp2.membrane_id = [ind1,4]
				#    newTransp2.type = tmp[3]
				#    newTransp2.act = newTransp.act
				#    cell.trans.append(newTransp2)
				#elif ind1==1 and ind2==4:
				#    newTransp2 = transporter()
				#    newTransp2.membrane_id = [ind1,5]
				#    newTransp2.type = tmp[3]
				#    newTransp2.act = newTransp.act
				#    cell.trans.append(newTransp2)
				
			# solute concentrations
			elif compare_string_prefix(id,"conc"):
				tmp = (id).split('_')
				cell.conc[solute_id[tmp[1]]][0] = float(num[0])
				cell.conc[solute_id[tmp[1]]][1] = float(num[1])
				cell.conc[solute_id[tmp[1]]][4] = float(num[2])
				cell.conc[solute_id[tmp[1]]][5] = float(num[3])
				if len(num) > 4:
					cell.conc[solute_id[tmp[1]]][2] = float(num[4])
					if len(num) > 5:
						cell.conc[solute_id[tmp[1]]][3] = float(num[5])
				if cell.diabete == 'Yes':
					if cell.segment == 'PT':
						cell.conc[14,0] = 25.0

			# reference impermeat concnetration (for cell)
			# or oncotic pressure for lumen/LIS/bath
			elif compare_string_prefix(id,"cimpref"):
				tmp = (id).split('_')
				cell.cimpref[compart_id[tmp[1]]] = float(num[0])

			# reference volumes
			elif compare_string_prefix(id,"volref"):
				tmp = (id).split('_')
				cell.volref[compart_id[tmp[1]]] = float(num[0])

			# actual volumes
			elif compare_string_prefix(id,"vol"):
				tmp = (id).split('_')  
				cell.vol[compart_id[tmp[1]]] = float(num[0])
				cell.vol_init[compart_id[tmp[1]]] = float(num[0])

			# membrane potential
			elif compare_string_prefix(id,"ep"):
				tmp = (id).split('_')
				cell.ep[compart_id[tmp[1]]] = float(num[0])
						
			# invalue keyword
#            else:
#                print("Wrong id",id)
				# if not a comment line
		
		line = file.readline()

		for i in range(NS):
			cell.sig[i,4,5] = 0
			cell.sig[i,5,4] = 0

		if cell.segment=='cTAL' or cell.segment=='mTAL':
			cell.dkd[2]=0
			cell.dkd[3]=0
			cell.dkd[5]=0
			cell.dkh[2]=0
			cell.dkh[3]=0
			cell.dkh[5]=0
		elif cell.segment=='DCT':
			cell.dkd = np.zeros(6)
			cell.dkh = np.zeros(6)
			cell.dkd[0]=496
			cell.dkh[0]=1.45
			cell.dkd[1]=49600
			cell.dkh[1]=145
			cell.dkd[4]=49600
			cell.dkh[4]=145
		elif cell.segment=='PT':
			cell.dkd = 496000 * np.ones(NC)
			cell.dkh = 1450 * np.ones(NC)
		elif cell.segment=='S3':
			cell.dkd = 4960 * np.ones(NC)
			cell.dkh = 14.5 * np.ones(NC)
		elif cell.segment=='CNT' or cell.segment == 'CCD':
			cell.dkd = np.zeros(6)
			cell.dkh = np.zeros(6)
			cell.dkd[0]=496
			cell.dkh[0]=1.45
			cell.dkd[1]=496
			cell.dkh[1]=1.45
			cell.dkd[2]=496000
			cell.dkh[2]=1450
			cell.dkd[3]=496000
			cell.dkh[3]=1450
			cell.dkd[4]=49600
			cell.dkh[4]=145
		elif cell.segment=='OMCD':
			cell.dkd = np.zeros(6)
			cell.dkh = np.zeros(6)
			cell.dkd[0]=49.6
			cell.dkh[0]=0.145
			cell.dkd[1]=496
			cell.dkh[1]=1.45
			cell.dkd[2]=496000
			cell.dkh[2]=1450
			cell.dkd[3]=496000
			cell.dkh[3]=1450
			cell.dkd[4]=49.6
			cell.dkh[4]=0.145			
		elif cell.segment == 'IMCD':
			cell.dkd = np.zeros(6)
			cell.dkh = np.zeros(6)
			cell.dkd[0]=49.6
			cell.dkh[0]=0.145
			cell.dkd[1]=4960
			cell.dkh[1]=14.5
			cell.dkd[2]=4960
			cell.dkh[2]=14.5
			cell.dkd[3]=4960
			cell.dkh[3]=14.5
			cell.dkd[4]=49.6
			cell.dkh[4]=0.145
	file.close()
