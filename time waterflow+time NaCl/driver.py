from defs import *
import copy
import set_params 
import flux
import numpy as np
import equations
import steadyequations
import electrochemical
import water
from values import *
import Newton
import matplotlib.pyplot as plt
from scipy.optimize import newton_krylov, broyden1, anderson, fsolve, newton
import timeit
import math
import boundaryBath

def compute(N, filename, method,Ncell,diabete='N'):

    # cell = [[]]
    # for i in range(Ncell):
    # 	for j in range(N):
    # 		cell[i,j].append(membrane())
    cell=[[membrane() for i in range(N)] for j in range(Ncell)]


    if diabete == 'N':
        for i in range(Ncell):
            for j in range(N):
                cell[i][j].diabete = 'No'
    elif diabete == 'Y':
        for i in range(Ncell):
            for j in range (N):
                cell[i][j].diabete = 'Yes'
    else:
        print('What is diabete status?')

    water_trans = 0
    na_trans = 0
    water_para = 0
    na_para = 0

    #filename=input('Choose a data file: ')

    #method = input('Choose a method: Newton or Broyden: ')

    for i in range(Ncell):
        for j in range(N):
            set_params.read_params(cell[i][j],filename,0)
        #cell[i].area_init[4][5] = 0.02
        #cell[i].area[4][5] = cell[i].area_init[4][5]*max(cell[i].vol[4]/cell[i].volref[4],1.0)
        #cell[i].area[5][4] = cell[i].area[4][5]


            boundaryBath.boundaryBath(cell[i][j],i)

    for i in range(Ncell-1):
        celln = copy.deepcopy(cell[i+1][0])
        dx = 1.0e-3
        if cell[0][0].segment == 'PT' :
            x = np.zeros(3 * NS + 7)

            x[0:NS] = cell[i][0].conc[:, 0]
            x[NS:2 * NS] = cell[i][0].conc[:, 1]
            x[2 * NS:3 * NS] = cell[i][0].conc[:, 4]

            x[3 * NS] = cell[i][0].vol[0]
            x[3*NS+1]=cell[i][0].vol[1]
            x[3 * NS + 2] = cell[i][0].vol[4]

            x[3 * NS + 3] = cell[i][0].ep[0]
            x[3 * NS + 4] = cell[i][0].ep[1]
            x[3 * NS + 5] = cell[i][0].ep[4]

            x[3 * NS + 6] = cell[i][0].pres[0]
            # x[3 * NS + 6] = cell[i][0].pres[1]

            steadyequations.steadyconservation_init(cell[i][0], cell[i + 1][0], celln, dx)
            fvec = steadyequations.steadyconservation_eqs(x, i)
            # print(fvec)

            if method == 'Newton':
                sol = Newton.newton(steadyequations.steadyconservation_eqs, x, i, cell[i][0].segment)

            if method == 'Broyden':
                sol = Newton.broyden(steadyequations.steadyconservation_eqs, x, i, cell[i][0].segment)

            if cell[0][0].segment == 'PT' :
                cell[i + 1][0].conc[:, 0] = sol[0:NS]
                cell[i + 1][0].conc[:, 1] = sol[NS:NS * 2]
                cell[i + 1][0].conc[:, 4] = sol[NS * 2:NS * 3]

                cell[i + 1][0].vol[0] = sol[3*NS]
                cell[i + 1][0].vol[1] = sol[3 * NS+1]
                cell[i + 1][0].vol[4] = sol[3 * NS + 2]

                cell[i + 1][0].ep[0] = sol[3*NS+3]
                cell[i + 1][0].ep[1] = sol[3 * NS + 4]
                cell[i + 1][0].ep[4] = sol[3 * NS + 5]

                cell[i + 1][0].pres[0] = sol[3*NS+6]
                # cell[i + 1][0].pres[1] = sol[3 * NS + 6]


    # to make mdel works we should do something different
    # to simulate sudden change, we need to change first cell's condition
    # do change as below (change cell[0]'s lumen condition means change boundary condition)

    for j in range(N):
        cell[0][j].vol[0] = cell[0][j].vol[0] * (1 + 0.1 * math.sin(2 * math.pi * j / 30))
        cell[0][j].conc[0,0]=cell[0][j].conc[0,0]+20 * math.sin(2 * math.pi * j / 30)
        cell[0][j].conc[2, 0] = cell[0][j].conc[2, 0] + 20 * math.sin(2 * math.pi * j / 30)


    # update in time
    for j in range(1,N):
        print('This is time '+str(0.1*j)+'s')
        for i in range(1,Ncell):
            print("   ")
            print('Calculating '+str(i)+'th Cell')
            celln = copy.deepcopy(cell[i-1][j])
            dx = 1.0e-3
            if cell[0][0].segment == 'PT' :
                x = np.zeros(3*NS+7)

                x[0:NS] = cell[i][j-1].conc[:,0]
                x[NS:2*NS] = cell[i][j-1].conc[:,1]
                x[2*NS:3*NS] = cell[i][j-1].conc[:,4]

                x[3*NS] = cell[i][j-1].vol[0]
                x[3*NS+1]=cell[i][j-1].vol[1]
                x[3*NS+2] = cell[i][j-1].vol[4]
 
                x[3*NS+3] = cell[i][j-1].ep[0]
                x[3*NS+4] = cell[i][j-1].ep[1]
                x[3*NS+5] = cell[i][j-1].ep[4]

                x[3*NS+6] = cell[i][j-1].pres[0]
                # x[3*NS+6]=cell[i-1][j+1].pres[1]






                equations.conservation_init (cell[i][j-1],cell[i][j],celln,dx)
                fvec = equations.conservation_eqs (x,j)
        #print(fvec)

                if method == 'Newton':
                    sol = Newton.newton(equations.conservation_eqs,x,i,cell[i][j].segment)

                if method == 'Broyden':
                    sol = Newton.broyden(equations.conservation_eqs, x, i, cell[i][j].segment)


                if cell[0][0].segment == 'PT' :
                    cell[i][j].conc[:,0] = sol[0:NS]
                    cell[i][j].conc[:,1] = sol[NS:NS*2]
                    cell[i][j].conc[:,4] = sol[NS*2:NS*3]

                    cell[i][j].vol[0] = sol[3*NS]
                    cell[i][j].vol[1]=sol[3*NS+1]
                    cell[i][j].vol[4] = sol[3*NS+2]

                    cell[i][j].ep[0] = sol[3*NS+3]
                    cell[i][j].ep[1] = sol[3*NS+4]
                    cell[i][j].ep[4] = sol[3*NS+5]

                    cell[i][j].pres[0] = sol[3*NS+6]
                    # cell[i][j+1].pres[1] = sol[3*NS+6]
            #
            # print("KKKKKKK")
            # print(sol[3*NS+5])
            # print(sol[3 * NS + 6])
            # print(sol[0:NS])
            # print( sol[3*NS+2])
            # print(sol[3*NS+5])
            # print("cell concentration")
            # print(sol[3*NS+4])
            # print(sol[3*NS+1])

        # check1=0
        # check2=0
        # stepdiff=np.zeros(3*NS+7)
        # stepdiff[0:NS]=cell[i+1].conc[:,0]-cell[i].conc[:,0]
        # stepdiff[NS:2*NS] = cell[i + 1].conc[:, 1] - cell[i ].conc[:, 1]
        # stepdiff[2*NS:NS*3] = cell[i + 1].conc[:, 4] - cell[i ].conc[:, 4]
        # stepdiff[3*NS]=cell[i+1].vol[0]-cell[i].vol[0]
        # stepdiff[3 * NS+1]=cell[i+1].vol[4]-cell[i].vol[4]
        # stepdiff[3 * NS+2]=cell[i+1].ep[0]-cell[i].ep[0]
        # stepdiff[3 * NS+3]=cell[i+1].ep[1]-cell[i].ep[1]
        # stepdiff[3 * NS+4]=cell[i+1].ep[4]-cell[i].ep[4]
        # stepdiff[3 * NS+5]=cell[i+1].pres[0]-cell[i].pres[0]
        # stepdiff[3 * NS+6]=cell[i+1].pres[1]-cell[i].pres[1]
        #
        # diffrelative=np.zeros(3*NS+7)
        # diffrelative[0:NS] = (cell[i + 1].conc[:, 0] - cell[i ].conc[:, 0])/ cell[i ].conc[:, 0]
        # diffrelative[NS:2 * NS] =( cell[i + 1].conc[:, 1] - cell[i ].conc[:,1])/cell[i].conc[:, 1]
        # diffrelative[2 * NS:NS * 3] =( cell[i + 1].conc[:, 4] - cell[i ].conc[:, 4])/ cell[i ].conc[:, 4]
        # diffrelative[3 * NS] = (cell[i + 1].vol[0] - cell[i].vol[0])/cell[i].vol[0]
        # diffrelative[3 * NS + 1] =( cell[i + 1].vol[4] - cell[i].vol[4])/cell[i].vol[4]
        # diffrelative[3 * NS + 2] = (cell[i + 1].ep[0] - cell[i].ep[0])/cell[i].ep[0]
        # diffrelative[3 * NS + 3] = (cell[i + 1].ep[1] - cell[i].ep[1])/cell[i].ep[1]
        # diffrelative[3 * NS + 4] = (cell[i + 1].ep[4] - cell[i].ep[4])/cell[i].ep[4]
        # diffrelative[3 * NS + 5] = (cell[i + 1].pres[0] - cell[i].pres[0])/cell[i].pres[0]
        # diffrelative[3 * NS + 6] = (cell[i + 1].pres[1] - cell[i].pres[1])/cell[i].pres[1]
        # check1=0
        # # check difference on x should be small enough
        # check1=max(abs(stepdiff))
        # check2=max(abs(diffrelative))
        # if check1<0.001 and check2<0.001:
        # 	N=i+1
        # 	break
        # else:
        # 	print("check1 and check2")
        # 	print(check1)
        # 	print(check2)
        print('\n')

#================================OUTPUT IN TO FILE================================

    # if cell[0].segment == 'PT':
    # 	file=open('PToutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4],cell[N-1].conc[j,5]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    #
    # elif cell[0].segment == 'S3':
    # 	file=open('S3outlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    # elif cell[0].segment == 'SDL':
    # 	file=open('SDLoutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    # elif cell[0].segment == 'mTAL':
    # 	file=open('mTALoutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    # elif cell[0].segment == 'cTAL':
    # 	file=open('cTALoutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4],cell[N-1].conc[j,5]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    # elif cell[0].segment == 'MD':
    # 	file=open('MDoutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    # elif cell[0].segment == 'DCT':
    # 	file=open('DCToutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    # elif cell[0].segment == 'CNT':
    # 	file=open('CNToutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,2],cell[N-1].conc[j,3],cell[N-1].conc[j,4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[2],cell[N-1].vol[3],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[2],cell[N-1].ep[3],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    # elif cell[0].segment == 'CCD':
    # 	file=open('CCDoutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,2],cell[N-1].conc[j,3],cell[N-1].conc[j,4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[2],cell[N-1].vol[3],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[2],cell[N-1].ep[3],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    # elif cell[0].segment == 'OMCD':
    # 	file=open('OMCDoutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,2],cell[N-1].conc[j,3],cell[N-1].conc[j,4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[2],cell[N-1].vol[3],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[2],cell[N-1].ep[3],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()
    # elif cell[0].segment == 'IMCD':
    # 	file=open('IMCDoutlet'+cell[0].sex+'.txt','w')
    # 	for j in range(NS):
    # 		file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
    # 	file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
    # 	file.write(str(cell[N-1].pres[0]))
    # 	file.close()


    number_of_cell = [i for i in range(1,200)]
    solute = ['Na','K','Cl','HCO3','H2CO3','CO2','HPO4','H2PO4','urea','NH3','NH4','H','HCO2','H2CO2','glu']
    compart = ['Lumen','Cell','ICA','ICB','LIS','Bath']

    return cell