from values import *
import numpy as np
from defs import *

def boundaryBath(cell,i):

	if cell.segment=='cTAL' or cell.segment == 'MD' or cell.segment=='DCT' or cell.segment=='PT' or cell.segment == 'CNT' or cell.segment == 'CCD':

		
		cell.pH[5] = pHplasma

		facbic = np.exp(np.log(10)*(cell.pH[5]-pKHCO3))
		facpho = np.exp(np.log(10)*(cell.pH[5]-pKHPO4))
		facamm = np.exp(np.log(10)*(cell.pH[5]-pKNH3))
		fachco2 = np.exp(np.log(10)*(cell.pH[5]-pKHCO2))

		cell.conc[0,5] = TotSodCM
		cell.conc[1,5] = TotPotCM
		cell.conc[2,5] = TotCloCM
		cell.conc[3,5] = TotBicCM
		cell.conc[4,5] = TotHcoCM
		cell.conc[5,5] = TotCo2CM

		cell.conc[4,5] = cell.conc[5,5]/342.07
		cell.conc[3,5] = cell.conc[4,5]*10**(cell.pH[5]-pKHCO3)
		cell.conc[6,5] = TotPhoCM*facpho/(1+facpho)
		cell.conc[7,5] = TotPhoCM/(1+facpho)

		cell.conc[8,5] = TotureaCM

		if cell.segment=='cTAL':
			TotAmmCT = 1.0
			TotAmmCM = 1.5
			pos = (cell.total-i)/cell.total
		elif cell.segment=='MD':
			TotAmmCT = 1.0
			TotAmmCM = 1.5
			pos = 1/200
		elif cell.segment=='DCT':
			TotAmmCT = 0.1
			TotAmmCM = 1.0
			pos = (cell.total-i)/cell.total
		elif cell.segment =='PT':
			TotAmmCT = 0.1
			TotAmmCM = 1.5
			total = cell.total*0.88 # need to change
			pos = i/total
		elif cell.segment == 'CNT':
			TotAmmCT = 0.1
			TotAmmCM = 1.5
			pos = (cell.total-i)/cell.total
		elif cell.segment == 'CCD':
			TotAmmCT = 0.1
			TotAmmCM = 1.5
			pos = i/cell.total			

		if cell.segment == 'CNT':
			Ammtotz = TotAmmCT
		else:
			Ammtotz = TotAmmCT+(TotAmmCM-TotAmmCT)*pos
		cell.conc[9,5] = Ammtotz*facamm/(1+facamm)
		cell.conc[10,5] = Ammtotz/(1+facamm)
		cell.conc[2,5] = TotCloCM+(Ammtotz/(1+facamm))
		# if i == 1:
		# 	print(TotAmmCT,TotAmmCM,pos)
		# 	print(facamm,TotCloCM)


		cell.conc[11,5] = np.exp(-np.log(10)*cell.pH[5])*1000

		cell.conc[12,5] = TotHco2CM*fachco2/(1+fachco2)
		cell.conc[13,5] = TotHco2CM/(1+fachco2)
		cell.conc[14,5] = TotGluCM

		elecS = 0
		for j in range(NS):
			elecS = elecS+zval[j]*cell.conc[j,5]

		cell.conc[2,5] = cell.conc[2,5]+elecS

		if cell.sex=='female':
			cell.conc[1,5]=cell.conc[1,5]-1
			cell.conc[2,5]=cell.conc[2,5]-1

	elif cell.segment=='mTAL' or cell.segment=='SDL' or cell.segment=='OMCD':

		if cell.segment == 'mTAL':
			pos = (cell.total-i)/cell.total
		elif cell.segment == 'SDL':
			pos = 0.3+0.7*i/cell.total
		elif cell.segment == 'OMCD':
			pos = i/cell.total

		cell.pH[5] = pHplasma-(pHplasma-phpap)*2/7*pos

		facbic = np.exp(np.log(10)*(cell.pH[5]-pKHCO3))
		facpho = np.exp(np.log(10)*(cell.pH[5]-pKHPO4))
		facamm = np.exp(np.log(10)*(cell.pH[5]-pKNH3))
		fachco2 = np.exp(np.log(10)*(cell.pH[5]-pKHCO2))

		cell.conc[0,5] = TotSodCM+(TotSodOI-TotSodCM)*pos
		cell.conc[1,5] = TotPotCM+(TotPotOI-TotPotCM)*pos
		cell.conc[2,5] = TotCloCM+(TotCloOI-TotCloCM)*pos
		cell.conc[3,5] = TotBicCM+(TotBicOI-TotBicCM)*pos
		cell.conc[4,5] = TotHcoCM+(TotHcoOI-TotHcoCM)*pos
		cell.conc[5,5] = TotCo2CM+(TotCo2OI-TotCo2CM)*pos

		cell.conc[4,5] = cell.conc[5,5]/342.07
		cell.conc[3,5] = cell.conc[4,5]*10**(cell.pH[5]-pKHCO3)
		cell.conc[5,5] = cell.conc[4,5]*342.07

		Phototz = (TotPhoCM+(TotPhoOI-TotPhoCM)*pos)

		cell.conc[6,5] = Phototz*facpho/(1+facpho)
		cell.conc[7,5] = Phototz/(1+facpho)
		cell.conc[8,5] = TotureaCM+(TotureaOI-TotureaCM)*pos

		TotAmmCM = 1.5
		Ammtotz = TotAmmCM+(TotAmmOI-TotAmmCM)*pos
		cell.conc[9,5] = Ammtotz*facamm/(1+facamm)
		cell.conc[10,5] = Ammtotz/(1+facamm)
		cell.conc[11,5] = np.exp(-np.log(10)*cell.pH[5])*1000

		Hco2totz = TotHco2CM+(TotHco2OI-TotHco2CM)*pos
		cell.conc[12,5] = Hco2totz*fachco2/(1+fachco2)
		cell.conc[13,5] = Hco2totz/(1+fachco2)
		cell.conc[14,5] = TotGluCM+(TotGluOI-TotGluCM)*pos

		elecS = 0
		for j in range(NS):
			elecS = elecS+zval[j]*cell.conc[j,5]

		cell.conc[2,5] = cell.conc[2,5]+elecS
		
		if cell.sex=='female':
			cell.conc[1,5]=cell.conc[1,5]-1
			cell.conc[2,5]=cell.conc[2,5]-1

	elif cell.segment=='S3':
		if i == 1:
			cell.pH[5] = pHplasma

			facbic = np.exp(np.log(10)*(cell.pH[5]-pKHCO3))
			facpho = np.exp(np.log(10)*(cell.pH[5]-pKHPO4))
			facamm = np.exp(np.log(10)*(cell.pH[5]-pKNH3))
			fachco2 = np.exp(np.log(10)*(cell.pH[5]-pKHCO2))

			cell.conc[0,5] = TotSodCM
			cell.conc[1,5] = TotPotCM
			cell.conc[2,5] = TotCloCM
			cell.conc[3,5] = TotBicCM
			cell.conc[4,5] = TotHcoCM
			cell.conc[5,5] = TotCo2CM

			cell.conc[4,5] = cell.conc[5,5]/342.07
			cell.conc[3,5] = cell.conc[4,5]*10**(cell.pH[5]-pKHCO3)
			cell.conc[6,5] = TotPhoCM*facpho/(1+facpho)
			cell.conc[7,5] = TotPhoCM/(1+facpho)

			cell.conc[8,5] = TotureaCM

			TotAmmCT = 0.1
			TotAmmCM = 1.5
			pos = 1

			Ammtotz = TotAmmCT+(TotAmmCM-TotAmmCT)*pos
			cell.conc[9,5] = Ammtotz*facamm/(1+facamm)
		
			cell.conc[10,5] = Ammtotz/(1+facamm)
			cell.conc[2,5] = TotCloCM+(Ammtotz/(1+facamm))

			cell.conc[11,5] = np.exp(-np.log(10)*cell.pH[5])*1000

			cell.conc[12,5] = TotHco2CM*fachco2/(1+fachco2)
			cell.conc[13,5] = TotHco2CM/(1+fachco2)
			cell.conc[14,5] = TotGluCM

			elecS = 0
			for j in range(NS):
				elecS = elecS+zval[j]*cell.conc[j,5]

			cell.conc[2,5] = cell.conc[2,5]+elecS

		else:
			NPT=0.88*cell.total
			pos = (0.3*(i))/(cell.total-NPT)
			cell.pH[5] = pHplasma-(pHplasma-phpap)*2/7*pos

			facbic = np.exp(np.log(10)*(cell.pH[5]-pKHCO3))
			facpho = np.exp(np.log(10)*(cell.pH[5]-pKHPO4))
			facamm = np.exp(np.log(10)*(cell.pH[5]-pKNH3))
			fachco2 = np.exp(np.log(10)*(cell.pH[5]-pKHCO2))

			cell.conc[0,5] = TotSodCM+(TotSodOI-TotSodCM)*pos
			cell.conc[1,5] = TotPotCM+(TotPotOI-TotPotCM)*pos
			cell.conc[2,5] = TotCloCM+(TotCloOI-TotCloCM)*pos
			cell.conc[3,5] = TotBicCM+(TotBicOI-TotBicCM)*pos
			cell.conc[4,5] = TotHcoCM+(TotHcoOI-TotHcoCM)*pos
			cell.conc[5,5] = TotCo2CM+(TotCo2OI-TotCo2CM)*pos

			cell.conc[4,5] = cell.conc[5,5]/342.07
			cell.conc[3,5] = cell.conc[4,5]*10**(cell.pH[5]-pKHCO3)
			cell.conc[5,5] = cell.conc[4,5]*342.07

			Phototz = TotPhoCM+(TotPhoOI-TotPhoCM)*pos

			cell.conc[6,5] = Phototz*facpho/(1+facpho)
			cell.conc[7,5] = Phototz/(1+facpho)
			cell.conc[8,5] = TotureaCM+(TotureaOI-TotureaCM)*pos

			TotAmmCM = 1.5
			Ammtotz = TotAmmCM+(TotAmmOI-TotAmmCM)*pos
			cell.conc[9,5] = Ammtotz*facamm/(1+facamm)
			cell.conc[10,5] = Ammtotz/(1+facamm)
			cell.conc[11,5] = np.exp(-np.log(10)*cell.pH[5])*1000

			Hco2totz = TotHco2CM+(TotHco2OI-TotHco2CM)*pos
			cell.conc[12,5] = Hco2totz*fachco2/(1+fachco2)
			cell.conc[13,5] = Hco2totz/(1+fachco2)
			cell.conc[14,5] = TotGluCM+(TotGluOI-TotGluCM)*pos

			elecS = 0
			for j in range(NS):
				elecS = elecS+zval[j]*cell.conc[j,5]

			cell.conc[2,5] = cell.conc[2,5]+elecS
		
		if cell.sex=='female':
			cell.conc[1,5]=cell.conc[1,5]-1
			cell.conc[2,5]=cell.conc[2,5]-1

	elif cell.segment == 'IMCD':

		pos = i/cell.total
		cell.ep[5]=-0.001e-3/EPref

		cell.pH[5] = pHplasma-(pHplasma-phpap)*((2/7)+(5/7)*pos)

		facbic = np.exp(np.log(10)*(cell.pH[5]-pKHCO3))
		facpho = np.exp(np.log(10)*(cell.pH[5]-pKHPO4))
		facamm = np.exp(np.log(10)*(cell.pH[5]-pKNH3))
		fachco2 = np.exp(np.log(10)*(cell.pH[5]-pKHCO2))

		cell.conc[0,5] = TotSodOI+(TotSodPap-TotSodOI)*pos
		cell.conc[1,5] = TotPotOI+(TotPotPap-TotPotOI)*pos
		cell.conc[2,5] = TotCloOI+(TotCloPap-TotCloOI)*pos
		cell.conc[3,5] = TotBicOI+(TotBicPap-TotBicOI)*pos
		cell.conc[4,5] = TotHcoOI+(TotHcoPap-TotHcoOI)*pos
		cell.conc[5,5] = TotCo2OI+(TotCo2Pap-TotCo2OI)*pos

		cell.conc[4,5] = cell.conc[5,5]/342.07
		cell.conc[3,5] = cell.conc[4,5]*10**(cell.pH[5]-pKHCO3)
		cell.conc[5,5] = cell.conc[4,5]*342.07

		Phototz = TotPhoOI+(TotPhoPap-TotPhoOI)*pos

		cell.conc[6,5] = Phototz*facpho/(1+facpho)
		cell.conc[7,5] = Phototz/(1+facpho)
		cell.conc[8,5] = TotureaOI+(TotureaPap-TotureaOI)*pos

		Ammtotz = TotAmmOI+(TotAmmPap-TotAmmOI)*pos
		cell.conc[9,5] = Ammtotz*facamm/(1+facamm)
		cell.conc[10,5] = Ammtotz/(1+facamm)
		cell.conc[11,5] = np.exp(-np.log(10)*cell.pH[5])*1000

		Hco2totz = TotHco2OI+(TotHco2Pap-TotHco2OI)*pos
		cell.conc[12,5] = Hco2totz*fachco2/(1+fachco2)
		cell.conc[13,5] = Hco2totz/(1+fachco2)
		cell.conc[14,5] = TotGluOI+(TotGluPap-TotGluOI)*pos

		elecS = 0
		for j in range(NS):
			elecS = elecS+zval[j]*cell.conc[j,5]

		cell.conc[2,5] = cell.conc[2,5]+elecS
		if cell.sex=='female':
			cell.conc[1,5]=cell.conc[1,5]-1
			cell.conc[2,5]=cell.conc[2,5]-1
	else:
		cell.conc[:,5] = cell.conc[:,5]

