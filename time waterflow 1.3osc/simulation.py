# This is used to simulate the whole superficial nephron. Type 'python simulation.py' in terminal to run. If you want to run individual segment, use computation.py.

from driver import compute
from values import *
from defs import *

solute = ['Na','K','Cl','HCO3','H2CO3','CO2','HPO4','H2PO4','urea','NH3','NH4','H','HCO2','H2CO2','glu']
compart = ['Lumen','Cell','ICA','ICB','LIS','Bath']
cw=Vref*60e6

gender = input('Which gender do you want to simulate? (Male/Female) ')
diabete = input('Does this kidney have diabete? (Y/N) ')
#========================================================
# Proximal convolute tubule
#========================================================
NPT = 176
if gender == 'Male':
	filename = 'PTparams_M.dat'
elif gender == 'Female':
	filename = 'PTparams_F.dat'
else:
	filename ='PTparams_F.dat'
pt=compute(NPT,filename,'Broyden',diabete)
#========================================================
# output PT Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(pt[0].sex+'pt_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NPT):
		file.write(str(pt[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(pt[0].sex+'pt_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NPT):
		file.write(str(pt[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(pt[0].sex+'pt_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NPT):
		file.write(str(pt[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output PT Water volume in Lumen and Cell
#========================================================
file=open(pt[0].sex+'pt_water_volume_in_Lumen.txt','w')
for j in range(1,NPT):
	file.write(str(pt[j-1].vol[0]*cw)+'\n')
file.close()
file=open(pt[0].sex+'pt_water_volume_in_Cell.txt','w')
for j in range(1,NPT):
	file.write(str(pt[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output PT solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(pt[0].sex+'pt_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NPT):
		file.write(str(pt[j-1].conc[i,0]*pt[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(pt[0].sex+'pt_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NPT):
		file.write(str(pt[j-1].conc[i,1]*pt[j-1].vol[1]*cw)+'\n')
	file.close()

print('PCT finished.')
#========================================================
# S3
#========================================================
NS3 = 25
if gender == 'Male':
	filename = 'S3params_M.dat'
elif gender == 'Female':
	filename = 'S3params_F.dat'
else:
	filename ='S3params_F.dat'
s3=compute(NS3,filename,'Newton',diabete)
#========================================================
# output S3 Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(s3[0].sex+'s3_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NS3):
		file.write(str(s3[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(s3[0].sex+'s3_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NS3):
		file.write(str(s3[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(s3[0].sex+'s3_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NS3):
		file.write(str(s3[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output S3 Water volume in Lumen and Cell
#========================================================
file=open(s3[0].sex+'s3_water_volume_in_Lumen.txt','w')
for j in range(1,NS3):
	file.write(str(s3[j-1].vol[0]*cw)+'\n')
file.close()
file=open(s3[0].sex+'s3_water_volume_in_Cell.txt','w')
for j in range(1,NS3):
	file.write(str(s3[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output S3 solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(s3[0].sex+'s3_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NS3):
		file.write(str(s3[j-1].conc[i,0]*s3[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(s3[0].sex+'s3_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NS3):
		file.write(str(s3[j-1].conc[i,1]*s3[j-1].vol[1]*cw)+'\n')
	file.close()

print('S3 finished.')
#========================================================
# Short descending limb
#========================================================
NSDL = 200
if gender == 'Male':
	filename = 'SDLparams_M.dat'
elif gender == 'Female':
	filename = 'SDLparams_F.dat'
else:
	filename ='SDLparams_F.dat'
sdl=compute(NSDL,filename,'Broyden',diabete)
#========================================================
# output SDL Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(sdl[0].sex+'sdl_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NSDL):
		file.write(str(sdl[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(sdl[0].sex+'sdl_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NSDL):
		file.write(str(sdl[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(sdl[0].sex+'sdl_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NSDL):
		file.write(str(sdl[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output SDL Water volume in Lumen and Cell
#========================================================
file=open(sdl[0].sex+'sdl_water_volume_in_Lumen.txt','w')
for j in range(1,NSDL):
	file.write(str(sdl[j-1].vol[0]*cw)+'\n')
file.close()
file=open(sdl[0].sex+'sdl_water_volume_in_Cell.txt','w')
for j in range(1,NSDL):
	file.write(str(sdl[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output SDL solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(sdl[0].sex+'sdl_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NSDL):
		file.write(str(sdl[j-1].conc[i,0]*sdl[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(sdl[0].sex+'sdl_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NSDL):
		file.write(str(sdl[j-1].conc[i,1]*sdl[j-1].vol[1]*cw)+'\n')
	file.close()

print('SDL finished.')
#========================================================
# Medulla thick ascending limb
#========================================================
NmTAL = 200
if gender == 'Male':
	filename = 'mTALparams_M.dat'
elif gender == 'Female':
	filename = 'mTALparams_F.dat'
else:
	filename ='mTALparams_F.dat'
mtal=compute(NmTAL,filename,'Newton',diabete)
#========================================================
# output mTAL Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(mtal[0].sex+'mtal_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NmTAL):
		file.write(str(mtal[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(mtal[0].sex+'mtal_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NmTAL):
		file.write(str(mtal[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(mtal[0].sex+'mtal_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NmTAL):
		file.write(str(mtal[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output mTAL Water volume in Lumen and Cell
#========================================================
file=open(mtal[0].sex+'mtal_water_volume_in_Lumen.txt','w')
for j in range(1,NmTAL):
	file.write(str(mtal[j-1].vol[0]*cw)+'\n')
file.close()
file=open(mtal[0].sex+'mtal_water_volume_in_Cell.txt','w')
for j in range(1,NmTAL):
	file.write(str(mtal[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output mTAL solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(mtal[0].sex+'mtal_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NmTAL):
		file.write(str(mtal[j-1].conc[i,0]*mtal[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(mtal[0].sex+'mtal_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NmTAL):
		file.write(str(mtal[j-1].conc[i,1]*mtal[j-1].vol[1]*cw)+'\n')
	file.close()

print('mTAL finished.')
#========================================================
# Cortex thick ascending limb
#========================================================
NcTAL = 200
if gender == 'Male':
	filename = 'cTALparams_M.dat'
elif gender == 'Female':
	filename = 'cTALparams_F.dat'
else:
	filename ='cTALparams_F.dat'
ctal=compute(NcTAL,filename,'Newton',diabete)
#========================================================
# output cTAL Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(ctal[0].sex+'ctal_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NcTAL):
		file.write(str(ctal[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(ctal[0].sex+'ctal_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NcTAL):
		file.write(str(ctal[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(ctal[0].sex+'ctal_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NcTAL):
		file.write(str(ctal[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output cTAL Water volume in Lumen and Cell
#========================================================
file=open(ctal[0].sex+'ctal_water_volume_in_Lumen.txt','w')
for j in range(1,NcTAL):
	file.write(str(ctal[j-1].vol[0]*cw)+'\n')
file.close()
file=open(ctal[0].sex+'ctal_water_volume_in_Cell.txt','w')
for j in range(1,NcTAL):
	file.write(str(ctal[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output cTAL solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(ctal[0].sex+'ctal_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NcTAL):
		file.write(str(ctal[j-1].conc[i,0]*ctal[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(ctal[0].sex+'ctal_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NcTAL):
		file.write(str(ctal[j-1].conc[i,1]*ctal[j-1].vol[1]*cw)+'\n')
	file.close()

print('cTAL finished.')
#========================================================
# Macula densa
#========================================================
NMD = 2
if gender == 'Male':
	filename = 'MDparams_M.dat'
elif gender == 'Female':
	filename = 'MDparams_F.dat'
else:
	filename ='MDparams_F.dat'
md=compute(NMD,filename,'Newton',diabete)
#========================================================
# output Concentrations of Macula densa in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(md[0].sex+'md_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NMD):
		file.write(str(md[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(md[0].sex+'md_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NMD):
		file.write(str(md[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(md[0].sex+'md_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NMD):
		file.write(str(md[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output Water volume of Macula densa in Lumen and Cell
#========================================================
file=open(md[0].sex+'md_water_volume_in_Lumen.txt','w')
for j in range(1,NMD):
	file.write(str(md[j-1].vol[0]*cw)+'\n')
file.close()
file=open(md[0].sex+'md_water_volume_in_Cell.txt','w')
for j in range(1,NMD):
	file.write(str(md[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output solute flows of Macula densa in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(md[0].sex+'md_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NMD):
		file.write(str(md[j-1].conc[i,0]*md[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(md[0].sex+'md_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NMD):
		file.write(str(md[j-1].conc[i,1]*md[j-1].vol[1]*cw)+'\n')
	file.close()

print('Macula densa finished.')
#========================================================
# Distal convoluted tubule
#========================================================
NDCT = 200
if gender == 'Male':
	filename = 'DCTparams_M.dat'
elif gender == 'Female':
	filename = 'DCTparams_F.dat'
else:
	filename ='DCTparams_F.dat'
dct=compute(NDCT,filename,'Newton',diabete) #female: Broyden
#========================================================
# output DCT Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(dct[0].sex+'dct_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NDCT):
		file.write(str(dct[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(dct[0].sex+'dct_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NDCT):
		file.write(str(dct[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(dct[0].sex+'dct_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NDCT):
		file.write(str(dct[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output DCT Water volume in Lumen and Cell
#========================================================
file=open(dct[0].sex+'dct_water_volume_in_Lumen.txt','w')
for j in range(1,NDCT):
	file.write(str(dct[j-1].vol[0]*cw)+'\n')
file.close()
file=open(dct[0].sex+'dct_water_volume_in_Cell.txt','w')
for j in range(1,NDCT):
	file.write(str(dct[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output DCT solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(dct[0].sex+'dct_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NDCT):
		file.write(str(dct[j-1].conc[i,0]*dct[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(dct[0].sex+'dct_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NDCT):
		file.write(str(dct[j-1].conc[i,1]*dct[j-1].vol[1]*cw)+'\n')
	file.close()

print('DCT finished.')
#========================================================
# Connecting tubule
#========================================================
NCNT = 200
if gender == 'Male':
	filename = 'CNTparams_M.dat'
elif gender == 'Female':
	filename = 'CNTparams_F.dat'
else:
	filename ='CNTparams_F.dat'
cnt=compute(NCNT,filename,'Newton',diabete)
#========================================================
# output CNT Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(cnt[0].sex+'cnt_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NCNT):
		file.write(str(cnt[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(cnt[0].sex+'cnt_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NCNT):
		file.write(str(cnt[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(cnt[0].sex+'cnt_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NCNT):
		file.write(str(cnt[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output CNT Water volume in Lumen and Cell
#========================================================
file=open(cnt[0].sex+'cnt_water_volume_in_Lumen.txt','w')
for j in range(1,NCNT):
	file.write(str(cnt[j-1].vol[0]*cw)+'\n')
file.close()
file=open(cnt[0].sex+'cnt_water_volume_in_Cell.txt','w')
for j in range(1,NCNT):
	file.write(str(cnt[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output CNT solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(cnt[0].sex+'cnt_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NCNT):
		file.write(str(cnt[j-1].conc[i,0]*cnt[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(cnt[0].sex+'cnt_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NCNT):
		file.write(str(cnt[j-1].conc[i,1]*cnt[j-1].vol[1]*cw)+'\n')
	file.close()

print('CNT finished.')
#========================================================
# Cortical collecting duct
#========================================================
NCCD = 200
if gender == 'Male':
	filename = 'CCDparams_M.dat'
elif gender == 'Female':
	filename = 'CCDparams_F.dat'
else:
	filename ='CCDparams_F.dat'
ccd=compute(NCCD,filename,'Newton',diabete)
#========================================================
# output CCD Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(ccd[0].sex+'ccd_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NCCD):
		file.write(str(ccd[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(ccd[0].sex+'ccd_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NCCD):
		file.write(str(ccd[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(ccd[0].sex+'ccd_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NCCD):
		file.write(str(ccd[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output CCD Water volume in Lumen and Cell
#========================================================
file=open(ccd[0].sex+'ccd_water_volume_in_Lumen.txt','w')
for j in range(1,NCCD):
	file.write(str(ccd[j-1].vol[0]*cw)+'\n')
file.close()
file=open(ccd[0].sex+'ccd_water_volume_in_Cell.txt','w')
for j in range(1,NCCD):
	file.write(str(ccd[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output CCD solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(ccd[0].sex+'ccd_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NCCD):
		file.write(str(ccd[j-1].conc[i,0]*ccd[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(ccd[0].sex+'ccd_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NCCD):
		file.write(str(ccd[j-1].conc[i,1]*ccd[j-1].vol[1]*cw)+'\n')
	file.close()

print('CCD finished.')
#========================================================
# Outer medullary collecting duct
#========================================================
NOMCD = 200
if gender == 'Male':
	filename = 'OMCDparams_M.dat'
elif gender == 'Female':
	filename = 'OMCDparams_F.dat'
else:
	filename ='OMCDparams_F.dat'
if ccd[0].sex == 'male':
	omcd=compute(NOMCD,filename,'Newton',diabete)
elif ccd[0].sex == 'female':
	omcd=compute(NOMCD,filename,'Newton',diabete)
#========================================================
# output OMCD Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(omcd[0].sex+'omcd_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NOMCD):
		file.write(str(omcd[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(omcd[0].sex+'omcd_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NOMCD):
		file.write(str(omcd[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(omcd[0].sex+'omcd_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NOMCD):
		file.write(str(omcd[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output OMCD Water volume in Lumen and Cell
#========================================================
file=open(omcd[0].sex+'omcd_water_volume_in_Lumen.txt','w')
for j in range(1,NOMCD):
	file.write(str(omcd[j-1].vol[0]*cw)+'\n')
file.close()
file=open(omcd[0].sex+'omcd_water_volume_in_Cell.txt','w')
for j in range(1,NOMCD):
	file.write(str(omcd[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output OMCD solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(omcd[0].sex+'omcd_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NOMCD):
		file.write(str(omcd[j-1].conc[i,0]*omcd[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(omcd[0].sex+'omcd_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NOMCD):
		file.write(str(omcd[j-1].conc[i,1]*omcd[j-1].vol[1]*cw)+'\n')
	file.close()

print('OMCD finished.')
#========================================================
# Inner medullary collecting duct
#========================================================
NIMCD = 200
if gender == 'Male':
	filename = 'IMCDparams_M.dat'
elif gender == 'Female':
	filename = 'IMCDparams_F.dat'
else:
	filename ='IMCDparams_F.dat'
imcd=compute(NIMCD,filename,'Newton',diabete)
#========================================================
# output IMCD Concentrations in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(imcd[0].sex+'imcd_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NIMCD):
		file.write(str(imcd[j-1].conc[i,0])+'\n')
	file.close()
for i in range(NS):
	file=open(imcd[0].sex+'imcd_con_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NIMCD):
		file.write(str(imcd[j-1].conc[i,1])+'\n')
	file.close()
for i in range(NS):
	file=open(imcd[0].sex+'imcd_con_of_'+solute[i]+'_in_Bath.txt','w')
	for j in range(1,NIMCD):
		file.write(str(imcd[j-1].conc[i,5])+'\n')
	file.close()
#========================================================
# output IMCD Water volume in Lumen and Cell
#========================================================
file=open(imcd[0].sex+'imcd_water_volume_in_Lumen.txt','w')
for j in range(1,NIMCD):
	file.write(str(imcd[j-1].vol[0]*cw)+'\n')
file.close()
file=open(imcd[0].sex+'imcd_water_volume_in_Cell.txt','w')
for j in range(1,NIMCD):
	file.write(str(imcd[j-1].vol[1]*cw)+'\n')
file.close()
#========================================================
# output IMCD solute flows in Lumen and Cell
#========================================================
for i in range(NS):
	file=open(imcd[0].sex+'imcd_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NIMCD):
		file.write(str(imcd[j-1].conc[i,0]*imcd[j-1].vol[0]*cw)+'\n')
	file.close()
for i in range(NS):
	file=open(imcd[0].sex+'imcd_flow_of_'+solute[i]+'_in_Cell.txt','w')
	for j in range(1,NIMCD):
		file.write(str(imcd[j-1].conc[i,1]*imcd[j-1].vol[1]*cw)+'\n')
	file.close()

print('IMCD finished.')

for i in range(NS):
	file=open(pt[0].sex+'_con_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NPT):
		file.write(str(pt[j-1].conc[i,0])+'\n')
	for j in range(1,NS3):
		file.write(str(s3[j-1].conc[i,0])+'\n')
	for j in range(1,NSDL):
		file.write(str(sdl[j-1].conc[i,0])+'\n')
	for j in range(1,NmTAL):
		file.write(str(mtal[j-1].conc[i,0])+'\n')
	for j in range(1,NcTAL):
		file.write(str(ctal[j-1].conc[i,0])+'\n')
	for j in range(1,NDCT):
		file.write(str(dct[j-1].conc[i,0])+'\n')
	for j in range(1,NCNT):
		file.write(str(cnt[j-1].conc[i,0])+'\n')
	for j in range(1,NCCD):
		file.write(str(ccd[j-1].conc[i,0])+'\n')
	for j in range(1,NOMCD):
		file.write(str(omcd[j-1].conc[i,0])+'\n')
	for j in range(1,NIMCD):
		file.write(str(imcd[j-1].conc[i,0])+'\n')
	file.close()

file=open(pt[0].sex+'_water_volume_in_Lumen.txt','w')
for j in range(1,NPT):
	file.write(str(pt[j-1].vol[0]*cw)+'\n')
for j in range(1,NS3):
	file.write(str(s3[j-1].vol[0]*cw)+'\n')
for j in range(1,NSDL):
	file.write(str(sdl[j-1].vol[0]*cw)+'\n')
for j in range(1,NmTAL):
	file.write(str(mtal[j-1].vol[0]*cw)+'\n')
for j in range(1,NcTAL):
	file.write(str(ctal[j-1].vol[0]*cw)+'\n')
for j in range(1,NDCT):
	file.write(str(dct[j-1].vol[0]*cw)+'\n')
for j in range(1,NCNT):
	file.write(str(cnt[j-1].vol[0]*cw)+'\n')
for j in range(1,NCCD):
	file.write(str(ccd[j-1].vol[0]*cw)+'\n')
for j in range(1,NOMCD):
	file.write(str(omcd[j-1].vol[0]*cw)+'\n')
for j in range(1,NIMCD):
	file.write(str(imcd[j-1].vol[0]*cw)+'\n')
file.close()

for i in range(NS):
	file=open(pt[0].sex+'_flow_of_'+solute[i]+'_in_Lumen.txt','w')
	for j in range(1,NPT):
		file.write(str(pt[j-1].conc[i,0]*pt[j-1].vol[0]*cw)+'\n')
	for j in range(1,NS3):
		file.write(str(s3[j-1].conc[i,0]*s3[j-1].vol[0]*cw)+'\n')
	for j in range(1,NSDL):
		file.write(str(sdl[j-1].conc[i,0]*sdl[j-1].vol[0]*cw)+'\n')
	for j in range(1,NmTAL):
		file.write(str(mtal[j-1].conc[i,0]*mtal[j-1].vol[0]*cw)+'\n')
	for j in range(1,NcTAL):
		file.write(str(ctal[j-1].conc[i,0]*ctal[j-1].vol[0]*cw)+'\n')
	for j in range(1,NDCT):
		file.write(str(dct[j-1].conc[i,0]*dct[j-1].vol[0]*cw)+'\n')
	for j in range(1,NCNT):
		file.write(str(cnt[j-1].conc[i,0]*cnt[j-1].vol[0]*cw)+'\n')
	for j in range(1,NCCD):
		file.write(str(ccd[j-1].conc[i,0]*ccd[j-1].vol[0]*cw)+'\n')
	for j in range(1,NOMCD):
		file.write(str(omcd[j-1].conc[i,0]*omcd[j-1].vol[0]*cw)+'\n')
	for j in range(1,NIMCD):
		file.write(str(imcd[j-1].conc[i,0]*imcd[j-1].vol[0]*cw)+'\n')							
	file.close()

file=open(pt[0].sex+'_pres_in_Lumen.txt','w')
for j in range(1,NPT):
	file.write(str(pt[j-1].pres[0])+'\n')
for j in range(1,NS3):
	file.write(str(s3[j-1].pres[0])+'\n')
for j in range(1,NSDL):
	file.write(str(sdl[j-1].pres[0])+'\n')
for j in range(1,NmTAL):
	file.write(str(mtal[j-1].pres[0])+'\n')
for j in range(1,NcTAL):
	file.write(str(ctal[j-1].pres[0])+'\n')
for j in range(1,NDCT):
	file.write(str(dct[j-1].pres[0])+'\n')
for j in range(1,NCNT):
	file.write(str(cnt[j-1].pres[0])+'\n')
for j in range(1,NCCD):
	file.write(str(ccd[j-1].pres[0])+'\n')
for j in range(1,NOMCD):
	file.write(str(omcd[j-1].pres[0])+'\n')
for j in range(1,NIMCD):
	file.write(str(imcd[j-1].pres[0])+'\n')
file.close()

file=open(pt[0].sex+'_ph_in_Lumen.txt','w')
for j in range(1,NPT):
	ph = -np.log(pt[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
for j in range(1,NS3):
	ph = -np.log(s3[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
for j in range(1,NSDL):
	ph = -np.log(sdl[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
for j in range(1,NmTAL):
	ph = -np.log(mtal[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
for j in range(1,NcTAL):
	ph = -np.log(ctal[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
for j in range(1,NDCT):
	ph = -np.log(dct[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
for j in range(1,NCNT):
	ph = -np.log(cnt[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
for j in range(1,NCCD):
	ph = -np.log(ccd[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
for j in range(1,NOMCD):
	ph = -np.log(omcd[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
for j in range(1,NIMCD):
	ph = -np.log(imcd[j-1].conc[11,0]/1000)/np.log(10)
	file.write(str(ph)+'\n')
file.close()